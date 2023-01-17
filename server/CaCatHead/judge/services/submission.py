import io
import logging
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from django.conf import settings
from django.utils import timezone

from CaCatHead.config import cacathead_config
from CaCatHead.core.constants import Verdict
from CaCatHead.judge.services.payload import JudgeSubmissionPayload
from CaCatHead.problem.models import ProblemTypes, DefaultCheckers, SourceCode, Problem
from CaCatHead.problem.views.upload import ProblemDirectory, get_testcase_root, read_testcase_root_version, \
    write_testcase_root_version
from CaCatHead.submission.models import Submission, ContestSubmission

logger = logging.getLogger('Judge.submission')

MAX_COMPILE_OUTPUT_SIZE = 1024
MAX_OUTPUT_SIZE = 512


class NoTestcaseException(Exception):
    pass


class NoCheckerException(Exception):
    pass


class NoLanguageException(Exception):
    pass


def get_checker_path(source_id):
    return Path(cacathead_config.judge.checker.root) / f'checker_{source_id}'


class SubmissionTask:
    def log(self, message, *args):
        submission_id = self.submission_id if self.submission_id is not None else self.contest_submission_id
        logger.info(message, *args, extra={'type': self.type, 'submission_id': submission_id})

    def __init__(self, payload: JudgeSubmissionPayload):
        if payload.submission_id is not None:
            self.type = 'Submission'
            self.submission_id = payload.submission_id
            self.contest_submission_id = None
        elif payload.contest_submission_id is not None:
            self.type = 'Contest Submission'
            self.submission_id = None
            self.contest_submission_id = payload.contest_submission_id
        else:
            # This is unreachable
            assert False

        self.log('Start initializing SubmissionTask')

        if payload.registration_id is not None:
            self.registration_id = payload.registration_id
            self.log(f'Contest Registration {{ id={self.registration_id} }}')
        else:
            self.registration_id = None

        self.code = payload.code
        self.language = payload.language
        self.problem_id = payload.problem_id
        self.problem_judge_id = payload.problem_judge_id
        self.testcase_directory = get_testcase_root(problem_judge_id=self.problem_judge_id)
        self.problem_type = payload.problem_type
        self.time_limit = payload.time_limit
        self.memory_limit = payload.memory_limit
        self.checker = payload.checker
        self.custom_checker_id = payload.custom_checker_id
        self.testcase_version = payload.testcase_version
        self.testcase_detail = payload.testcase_detail

        self.log(f'Language: {self.language}')
        self.log(f'Problem ID: {self.problem_id}')
        self.log(f'Problem type: {self.problem_type}')
        self.log(f'Time limit: {self.time_limit}')
        self.log(f'Memory limit: {self.memory_limit}')
        self.log(f'Checker: {self.checker}')
        self.log(f'Testcase dir: {self.testcase_directory}')
        self.log(f'Extra info: {payload.judge_extra_info}')

        # 保存编译输出
        self.compile_stdout = None

        self.verdict = Verdict.Waiting
        self.score = 0
        self.results = []

        self.tmp_dir = Path(tempfile.mkdtemp())
        os.chmod(self.tmp_dir, 0o775)
        self.code_file = self.tmp_dir / ("Main." + self.language)

        if settings.DEBUG_JUDGE:
            self.log(f'Tmp dir: {self.tmp_dir}')
            self.log(f'Code file: {self.code_file}')

        self.log('SubmissionTask has been initialized')

    def update_submission(self, verdict, score, detail):
        if self.submission_id is not None:
            sub_id = self.submission_id
            manager = Submission.objects
        elif self.contest_submission_id is not None:
            sub_id = self.contest_submission_id
            manager = ContestSubmission.objects
        else:
            # This is unreachable
            assert False

        if len(self.results) > 0:
            time_used = max([d['time'] for d in self.results])
            memory_used = max([d['memory'] for d in self.results])
        else:
            time_used = 0
            memory_used = 0

        return manager.filter(id=sub_id).update(verdict=verdict, score=score, detail=detail,
                                                time_used=time_used, memory_used=memory_used) == 1

    def update_submission_verdict(self, verdict: Verdict):
        if self.submission_id is not None:
            sub_id = self.submission_id
            manager = Submission.objects
        elif self.contest_submission_id is not None:
            sub_id = self.contest_submission_id
            manager = ContestSubmission.objects
        else:
            # This is unreachable
            assert False

        if verdict == Verdict.Compiling:
            rows = manager.filter(id=sub_id, verdict=Verdict.Waiting).update(
                judged=timezone.now(),
                verdict=Verdict.Compiling,
                detail={'node': cacathead_config.judge.name}
            )
            return rows == 1
        elif verdict == Verdict.Running:
            rows = manager.filter(id=sub_id, verdict=Verdict.Compiling).update(
                verdict=Verdict.Running
            )
            return rows == 1
        else:
            rows = manager.filter(id=sub_id, verdict=Verdict.Running).update(
                verdict=verdict
            )
            return rows == 1

    def run(self):
        self.log('Start running SubmissionTask')

        self.verdict = Verdict.Compiling
        if not self.update_submission_verdict(Verdict.Compiling):
            self.log('This submission may have been judge')

        try:
            self.prepare_checker()
            if self.verdict == Verdict.CompileError:
                # Checker 编译失败
                raise NoCheckerException

            self.dump_code()
            self.compile_code()

            if self.verdict != Verdict.CompileError:
                self.verdict = Verdict.Running
                if not self.update_submission_verdict(Verdict.Running):
                    self.log('This submission may have been judge')
                self.judge()
        except NoCheckerException:
            self.verdict = Verdict.SystemError
        except NoTestcaseException:
            self.verdict = Verdict.TestCaseError
        except NoLanguageException:
            self.verdict = Verdict.JudgeError
        finally:
            self.save_final_result()
            self.clean_temp()

        self.log('Running SubmissionTask finished')

    def dump_code(self):
        self.log(f'Dump code to {self.code_file}')
        code_file = io.open(self.code_file, 'w', encoding='utf8')
        code_file.write(self.code)
        code_file.close()

    def compile_code(self):
        self.log(f'Compile code {self.code_file}')
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
            self.log(f'Compile Error')
            self.verdict = Verdict.CompileError
            self.compile_stdout = e.output.decode('utf-8')[:MAX_COMPILE_OUTPUT_SIZE]
        except OSError as e:
            self.verdict = Verdict.CompileError
            self.log(f'Compile OS Error {e}')
        finally:
            if not settings.DEBUG_JUDGE:
                shutil.rmtree(cwd)
            self.log(f'Compile code {self.code_file} OK')

    def prepare_exec_file(self, tmp_dir: Path):
        if self.language in ['cpp', 'c']:
            exec_file_name_src = 'Main'
            exec_file_name_dst = 'a.out'
        else:
            exec_file_name_src = 'Main.class'
            exec_file_name_dst = 'Main.class'
        self.log(f"Copy exec file {exec_file_name_src} -> {exec_file_name_dst}")
        exec_file_src = os.path.join(tmp_dir, exec_file_name_src)
        exec_file_dst = os.path.join(self.tmp_dir, exec_file_name_dst)
        shutil.copyfile(exec_file_src, exec_file_dst)
        os.chmod(exec_file_dst, 0o775)

    def prepare_checker(self):
        if self.checker == DefaultCheckers.custom:
            self.checker = get_checker_path(self.custom_checker_id)
            if not self.checker.exists():
                self.log(f"Start preparing custom checker {self.checker}")

                custom_checker = SourceCode.objects.get(id=self.custom_checker_id)
                if custom_checker is None:
                    raise NoCheckerException

                cwd = Path(tempfile.mkdtemp())
                os.chmod(cwd, 0o775)

                try:
                    if custom_checker.language == 'cpp':
                        checker_code_file = 'Checker.cpp'
                    elif custom_checker.language == 'c':
                        checker_code_file = 'Checker.c'
                    else:
                        raise NoLanguageException

                    file_handler = io.open(cwd / checker_code_file, 'w', encoding='utf8')
                    file_handler.write(custom_checker.code)
                    file_handler.close()

                    if custom_checker.language == 'cpp':
                        commands = ["g++", checker_code_file, "-o", self.checker.absolute(), "-static", "-w",
                                    "-lm", "-std=c++17", "-O2", "-DONLINE_JUDGE"]
                    elif custom_checker.language == 'c':
                        (cwd / checker_code_file).write_text(custom_checker.code, encoding='UTF-8')
                        commands = ["gcc", checker_code_file, "-o", self.checker.absolute(), "-static", "-w",
                                    "-lm", "-std=c11", "-O2", "-DONLINE_JUDGE"]
                    else:
                        raise NoLanguageException

                    self.log(f"Start compiling custom checker {self.checker}")
                    subprocess.check_output(commands, stderr=subprocess.STDOUT, cwd=cwd)
                    os.chmod(self.checker, 0o775)
                except subprocess.CalledProcessError as e:
                    self.log(f'Compile Checker Error')
                    self.verdict = Verdict.CompileError
                    self.compile_stdout = e.output.decode('utf-8')[:MAX_COMPILE_OUTPUT_SIZE]
                except OSError as e:
                    self.verdict = Verdict.CompileError
                    self.log(f'Compile checker OS Error {e}')
                finally:
                    shutil.rmtree(cwd)
                    self.log(f'Finish compiling checker {self.checker}')

    def judge(self):
        self.log(f"Start judging")

        verdict = Verdict.Accepted
        for (index, testcase) in enumerate(self.testcase_detail):
            try:
                version = read_testcase_root_version(problem_judge_id=self.problem_judge_id)
                if version == self.testcase_version:
                    # 测试用例版本号匹配
                    self.prepare_testcase_file(index, in_file=testcase['input'], ans_file=testcase['answer'])
                else:
                    shutil.rmtree(self.testcase_directory, ignore_errors=True)
                    # 测试用例过期
                    raise NoTestcaseException
            except NoTestcaseException:
                # Try downloading testcases from minio
                problem_judge_id = self.problem_judge_id
                testcase_version = self.testcase_version
                self.log(f'Downloading Problem Judge #{problem_judge_id}. (version: {testcase_version}) testcases')
                problem = Problem.objects.get(id=self.problem_id)
                problem_directory = ProblemDirectory.try_make(problem=problem)
                # 处理 MinIO 下载失败
                download_ok = False
                try:
                    download_ok = problem_directory.download_testcases()
                except Exception as ex:
                    self.log(f'Download testcase error: %r', ex)
                    download_ok = False
                finally:
                    if download_ok:
                        write_testcase_root_version(problem=problem)
                        self.prepare_testcase_file(index, in_file=testcase['input'], ans_file=testcase['answer'])
                    else:
                        raise NoTestcaseException

            self.log(f'Run code on the testcase #{index}. in the sandbox')
            self.run_sandbox()
            self.log(f'Read testcase #{index}. running result')
            detail = self.read_result(testcase)
            self.log(f'Run code on the testcase #{index}. finished')

            if detail['verdict'] == Verdict.Accepted:
                self.score += testcase['score']
            else:
                if self.problem_type == ProblemTypes.AC:
                    # XCPC 模式, 遇到非正确结果直接退出
                    verdict = detail['verdict']
                    break
                else:
                    # OI 模式, 遇到非正确结果继续判题
                    if verdict == detail['verdict']:
                        # OI 模式, 若错误结果一致, 则保持结果不变
                        pass
                    elif verdict == Verdict.Accepted:
                        # OI 模式, 第一次遇到错误结果, 记录此结果
                        verdict = detail['verdict']
                    else:
                        # OI 模式, 遇到了多种错误结果
                        verdict = Verdict.PartiallyCorrect

        self.verdict = verdict
        self.log(f'Finish judging, verdict is {self.verdict}')

    def prepare_testcase_file(self, index: int, in_file: str, ans_file: str):
        self.log(f'Prepare testcase #{index}. (in = {in_file}, ans = {ans_file})')
        in_file_src = self.testcase_directory / in_file
        ans_file_src = self.testcase_directory / ans_file
        in_file_dst = self.tmp_dir / "in.txt"
        ans_file_dst = self.tmp_dir / "ans.txt"
        if not in_file_src.exists() or not ans_file_src.exists():
            raise NoTestcaseException
        shutil.copyfile(in_file_src, in_file_dst)
        shutil.copyfile(ans_file_src, ans_file_dst)

    def run_sandbox(self):
        commands = ["catj", "-t", str(self.time_limit), "-m", str(self.memory_limit),
                    "-d", self.tmp_dir, "-l", self.language, "-s", self.checker]
        subprocess.call(commands)

    def read_result(self, testcase):
        result_file = open(self.tmp_dir / "result.txt", 'r')
        verdict = Verdict.parse(result_file.readline().strip().split()[1])
        run_time = int(result_file.readline().strip().split()[1])
        run_memory = int(result_file.readline().strip().split()[1])
        checker_time = int(result_file.readline().strip().split()[1])
        checker_memory = int(result_file.readline().strip().split()[1])
        others = result_file.read().strip()
        detail = {
            'verdict': verdict,
            'time': run_time,
            'memory': run_memory,
            'checker': {
                'time': checker_time,
                'memory': checker_memory
            },
            'message': others
        }
        if 'score' in testcase:
            if verdict == Verdict.Accepted:
                detail['score'] = testcase['score']
            else:
                detail['score'] = 0
        if 'sample' in testcase and testcase['sample']:
            detail['sample'] = True
        self.results.append(detail)
        return detail

    def save_contest_result(self, verdict: Verdict, score: int, detail: dict):
        pass
        # if self.registration is None:
        #     return
        # self.log(f"Start refreshing contest submission result of registration #{self.registration.id}")
        # refresh_registration_standing(self.registration)
        # self.log(f"Finish refreshing contest submission result of registration #{self.registration.id}")

    def save_final_result(self):
        self.log(f"Save submission final result")

        detail = {
            'verdict': Verdict.Accepted,
            'score': self.score,
            'compile': {
                'stdout': ''
            },
            'node': cacathead_config.judge.name,
            'results': self.results,
            'timestamp': timezone.now().isoformat()
        }

        if self.verdict == Verdict.CompileError:
            detail['verdict'] = Verdict.CompileError
        elif self.verdict in [Verdict.TestCaseError, Verdict.SystemError, Verdict.JudgeError]:
            detail['verdict'] = self.verdict
        else:
            detail['verdict'] = self.verdict

        # Source compile error / Checker compile error
        if self.compile_stdout is not None:
            detail['compile']['stdout'] = self.compile_stdout

        if settings.DEBUG_JUDGE:
            self.log(detail)

        self.update_submission(verdict=detail['verdict'], score=detail['score'], detail=detail)
        # self.save_contest_result(verdict=detail['verdict'], score=detail['score'], detail=detail)

    def clean_temp(self):
        if not settings.DEBUG_JUDGE:
            self.log(f'Clean running directory')
            shutil.rmtree(self.tmp_dir)
