import os
import io
import json
import shutil
import logging
import subprocess
import tempfile
from pathlib import Path

from django.conf import settings
from django.utils import timezone

from CaCatHead.core.constants import Verdict
from CaCatHead.submission.models import Submission

logger = logging.getLogger('Judge.service')


class NoTestDataException(Exception):
    pass


class NoLanguageException(Exception):
    pass


class SubmissionTask:
    def __init__(self, message: bytes):
        data = json.loads(message)
        logger.info(data)

        self.submission = Submission.objects.get(id=data['submission_id'])
        self.code = data["code"]
        self.language = data["language"]
        self.problem_id = str(data["problem_id"])
        self.time_limit = str(data["time_limit"])
        self.memory_limit = str(data["memory_limit"])
        self.testcase_detail = data["testcase_detail"]

        self.compiler_output = None
        self.verdict = Verdict.Waiting
        self.score = 0
        self.results = []

        self.tmp_dir = Path(tempfile.mkdtemp())
        os.chmod(self.tmp_dir, 0o775)
        self.code_file = self.tmp_dir / ("Main." + self.language)

    def update_submission(self, judged=None, verdict=None, score=None, detail=None):
        if judged is not None:
            self.submission.judged = judged
        if verdict is not None:
            self.submission.verdict = verdict
        if score is not None:
            self.submission.score = score
        if detail is not None:
            self.submission.detail = detail
        self.submission.save()

    def run(self):
        logger.info(f'Run submission at {self.tmp_dir}')
        self.verdict = Verdict.Compiling
        self.update_submission(judged=timezone.now(), verdict=Verdict.Compiling)

        try:
            self.dump_code()

            self.compile_code()

            if self.verdict != Verdict.CompileError:
                self.verdict = Verdict.Running
                self.update_submission(verdict=Verdict.Running)
                self.judge()

            self.save_result()
        except NoTestDataException:
            self.verdict = Verdict.TestCaseError
        except NoLanguageException:
            self.verdict = Verdict.JudgeError
        finally:
            self.clean_temp()

    def dump_code(self):
        logger.info(f'Dump code to {self.code_file}')
        code_file = io.open(self.code_file, 'w', encoding='utf8')
        code_file.write(self.code)
        code_file.close()

    def compile_code(self):
        logger.info(f'Start compiling code {self.code_file}')
        if self.language == 'cpp':
            commands = ["g++", self.code_file, "-o", "Main", "-static", "-w",
                        "-lm", "-std=c++11", "-O2", "-DONLINE_JUDGE"]
        elif self.language == 'c':
            commands = ["gcc", self.code_file, "-o", "Main", "-static", "-w",
                        "-lm", "-std=c11", "-O2", "-DONLINE_JUDGE"]
        elif self.language == 'java':
            commands = ["javac", self.code_file, "-d", "."]
        else:
            raise NoLanguageException

        cwd = Path(tempfile.mkdtemp())
        os.chmod(cwd, 0o775)
        try:
            subprocess.check_output(commands, stderr=subprocess.STDOUT, cwd=cwd)
            self.prepare_exec_file(cwd)
        except subprocess.CalledProcessError as e:
            self.verdict = Verdict.CompileError
            self.compiler_output = e.output
        except OSError as e:
            self.verdict = Verdict.CompileError
            logger.error(e)
        finally:
            shutil.rmtree(cwd)

    def prepare_exec_file(self, tmp_dir: Path):
        if self.language in ['cpp', 'c']:
            exec_file_name_src = 'Main'
            exec_file_name_dst = 'a.out'
        else:
            exec_file_name_src = 'Main.class'
            exec_file_name_dst = 'Main.class'
        logger.info(f"Copy exec file {exec_file_name_src} -> {exec_file_name_dst}")
        exec_file_src = os.path.join(tmp_dir, exec_file_name_src)
        exec_file_dst = os.path.join(self.tmp_dir, exec_file_name_dst)
        shutil.copyfile(exec_file_src, exec_file_dst)
        os.chmod(exec_file_dst, 0o775)

    def judge(self):
        logger.info("Start Judge")
        for testcase in self.testcase_detail:
            self.prepare_testcase_file(in_file=testcase['in'], ans_file=testcase['ans'])
            self.run_sandbox()
            detail = self.read_result()
            if detail['verdict'] == Verdict.Accepted:
                self.score += testcase['score']
        logger.info("Finish Judge")

    def prepare_testcase_file(self, in_file: str, ans_file: str):
        logger.info(f'Prepare testcase (in = {in_file}, ans = {ans_file})')
        in_file_src = os.path.join(settings.TESTCASE_ROOT, self.problem_id, in_file)
        ans_file_src = os.path.join(settings.TESTCASE_ROOT, self.problem_id, ans_file)
        in_file_dst = os.path.join(self.tmp_dir, "in.in")
        ans_file_dst = os.path.join(self.tmp_dir, "out.out")
        if not os.path.exists(in_file_src) or not os.path.exists(ans_file_src):
            raise NoTestDataException
        shutil.copyfile(in_file_src, in_file_dst)
        shutil.copyfile(ans_file_src, ans_file_dst)

    def run_sandbox(self):
        logger.info("Run catj")
        commands = ["catj", "-t", self.time_limit, "-m", self.memory_limit, "-d", self.tmp_dir, "-l", self.language]
        subprocess.call(commands)

    def read_result(self):
        logger.info("Read one case result")
        result_file = open(os.path.join(self.tmp_dir, "result.txt"), 'r')
        verdict = Verdict.parse(result_file.readline().strip())
        run_time = int(result_file.readline().strip())
        run_memory = int(result_file.readline().strip())
        others = result_file.readline().strip()
        detail = {
            'verdict': verdict,
            'time': run_time,
            'memory': run_memory,
            'message': others
        }
        self.results.append(detail)
        return detail

    def save_result(self):
        logger.info("Save result, result is %s" % self.results)
        detail = {
            'verdict': Verdict.Accepted,
            'score': self.score,
            'compile': {
                'stdout': '',
                'stderr': ''
            },
            'results': self.results
        }

        if self.verdict == Verdict.CompileError:
            detail['verdict'] = Verdict.CompileError
            detail['compile']['stdout'] = self.compiler_output
        elif self.verdict in [Verdict.TestCaseError, Verdict.SystemError, Verdict.JudgeError]:
            detail['verdict'] = self.verdict
        else:
            other_verdicts = set()
            for result in self.results:
                cur_verdict = result['verdict']
                if cur_verdict != Verdict.Accepted:
                    other_verdicts.add(cur_verdict)
            if len(other_verdicts) == 0:
                # 所有测试用例返回 Accepted
                detail['verdict'] = Verdict.Accepted
            elif len(other_verdicts) == 1:
                # 所有测试用例返回 Accepted 或其他结果, 最终结果为此结果
                detail['verdict'] = other_verdicts.pop()
            else:
                # 返回了多种结果
                detail['verdict'] = Verdict.PartiallyCorrect

        self.update_submission(verdict=detail['verdict'], score=detail['score'], detail=detail)

    def clean_temp(self):
        logger.info(f'Clean submission running directory {self.tmp_dir}')
        shutil.rmtree(self.tmp_dir)
