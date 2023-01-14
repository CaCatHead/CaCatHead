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
from CaCatHead.contest.models import ContestRegistration
from CaCatHead.contest.services.standings import refresh_registration_standing
from CaCatHead.core.constants import Verdict
from CaCatHead.problem.models import ProblemTypes, DefaultCheckers
from CaCatHead.problem.views.upload import ProblemDirectory
from CaCatHead.submission.models import Submission, ContestSubmission

logger = logging.getLogger('Judge.submission')

MAX_COMPILE_OUTPUT_SIZE = 1024
MAX_OUTPUT_SIZE = 512


class NoTestDataException(Exception):
    pass


class NoCheckerException(Exception):
    pass


class NoLanguageException(Exception):
    pass


def get_checker_path(source_id):
    return Path(cacathead_config.judge.checker.root) / f'checker_{source_id}'


class SubmissionTask:
    def log(self, message, *args):
        logger.info(message, *args, extra={'type': self.type, 'submission': self.submission})

    def __init__(self, submission: Submission = None,
                 contest_submission: ContestSubmission = None,
                 registration: ContestRegistration = None):
        if submission is not None:
            self.type = 'Submission'
            self.submission = submission
        elif contest_submission is not None:
            self.type = 'Contest Submission'
            self.submission = contest_submission
        else:
            # This is unreachable
            assert False

        self.log('Start initializing SubmissionTask')

        if registration is not None:
            self.registration = registration
            self.log(
                f'Registration {{ id={self.registration.id}, team = {self.registration.team.id}, contest={self.registration.contest.id} }}')
        else:
            self.registration = None

        self.code = self.submission.code
        self.language = self.submission.language
        problem = self.submission.problem
        self.problem_id = str(problem.id)
        self.problem_judge_id = str(problem.problem_info.problem_judge.id)
        self.problem_type = problem.problem_info.problem_judge.problem_type
        self.time_limit = problem.time_limit
        self.memory_limit = problem.memory_limit
        self.checker = problem.problem_info.problem_judge.checker
        self.testcase_detail = problem.problem_info.problem_judge.testcase_detail

        self.log(f'Language: {self.language}')
        self.log(f'Problem ID: {self.problem_id}')
        self.log(f'Problem Judge ID: {self.problem_judge_id}')
        self.log(f'Problem type: {self.problem_type}')
        self.log(f'Time limit: {self.time_limit}')
        self.log(f'Memory limit: {self.memory_limit}')
        self.log(f'Extra info: {problem.problem_info.problem_judge.extra_info}')

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

    def run(self):
        if self.submission.verdict != Verdict.Waiting:
            self.log('Fail starting running SubmissionTask for the submission may have been judge')
            return
        else:
            self.log('Start running SubmissionTask')

        self.verdict = Verdict.Compiling
        self.update_submission(judged=timezone.now(), verdict=Verdict.Compiling,
                               detail={'node': cacathead_config.judge.name})

        try:
            self.prepare_checker()
            if self.verdict == Verdict.CompileError:
                # Checker 编译失败
                raise NoCheckerException

            self.dump_code()
            self.compile_code()

            if self.verdict != Verdict.CompileError:
                self.verdict = Verdict.Running
                self.update_submission(verdict=Verdict.Running)
                self.judge()
        except NoCheckerException:
            self.verdict = Verdict.SystemError
        except NoTestDataException:
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
            self.checker = get_checker_path(self.submission.problem.problem_info.problem_judge.custom_checker_id)
            if not self.checker.exists():
                self.log(f"Start preparing custom checker {self.checker}")

                custom_checker = self.submission.problem.problem_info.problem_judge.custom_checker
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
                self.prepare_testcase_file(index, in_file=testcase['input'], ans_file=testcase['answer'])
            except NoTestDataException:
                # Try downloading testcases from minio
                self.log(f'Downloading Problem Judge #{self.problem_judge_id}. testcases from minio')
                problem_directory = ProblemDirectory.make_from_id(problem_id=self.problem_id,
                                                                  problem_judge_id=self.problem_judge_id)
                # 处理 MinIO 下载失败
                download_ok = False
                try:
                    download_ok = problem_directory.download_testcases()
                except Exception as ex:
                    self.log(f'Download testcase error: %r', ex)
                    download_ok = False
                finally:
                    if download_ok:
                        self.prepare_testcase_file(index, in_file=testcase['input'], ans_file=testcase['answer'])
                    else:
                        raise NoTestDataException

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
        # TODO: extract these logic
        self.log(f'Prepare testcase #{index}. (in = {in_file}, ans = {ans_file})')
        in_file_src = os.path.join(settings.TESTCASE_ROOT, self.problem_judge_id, in_file)
        ans_file_src = os.path.join(settings.TESTCASE_ROOT, self.problem_judge_id, ans_file)
        in_file_dst = os.path.join(self.tmp_dir, "in.txt")
        ans_file_dst = os.path.join(self.tmp_dir, "ans.txt")
        if not os.path.exists(in_file_src) or not os.path.exists(ans_file_src):
            raise NoTestDataException
        shutil.copyfile(in_file_src, in_file_dst)
        shutil.copyfile(ans_file_src, ans_file_dst)

    def run_sandbox(self):
        commands = ["catj", "-t", str(self.time_limit), "-m", str(self.memory_limit),
                    "-d", self.tmp_dir, "-l", self.language, "-s", self.checker]
        subprocess.call(commands)

    def read_result(self, testcase):
        result_file = open(os.path.join(self.tmp_dir, "result.txt"), 'r')
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

    def update_submission(self, judged=None, verdict=None, score=None, detail=None):
        if judged is not None:
            self.submission.judged = judged
        if verdict is not None:
            self.submission.verdict = verdict
        if score is not None:
            self.submission.score = score
        if detail is not None:
            self.submission.detail = detail
        if len(self.results) > 0:
            self.submission.time_used = max([d['time'] for d in self.results])
            self.submission.memory_used = max([d['memory'] for d in self.results])
        self.submission.save()

    def save_contest_result(self, verdict: Verdict, score: int, detail: dict):
        if self.registration is None:
            return
        self.log(f"Start refreshing contest submission result of registration #{self.registration.id}")
        refresh_registration_standing(self.registration)
        self.log(f"Finish refreshing contest submission result of registration #{self.registration.id}")

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
        self.save_contest_result(verdict=detail['verdict'], score=detail['score'], detail=detail)

    def clean_temp(self):
        if not settings.DEBUG_JUDGE:
            self.log(f'Clean running directory')
            shutil.rmtree(self.tmp_dir)
