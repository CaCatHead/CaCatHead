import io
import json
import logging
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from django.conf import settings
from django.utils import timezone

from CaCatHead.config import cacathead_config
from CaCatHead.contest.models import ContestRegistration, ContestType
from CaCatHead.core.constants import Verdict
from CaCatHead.problem.models import ProblemTypes
from CaCatHead.problem.views.upload import ProblemDirectory
from CaCatHead.submission.models import Submission, ContestSubmission, ContestSubmissionType

logger = logging.getLogger('Judge.service')

MAX_COMPILE_OUTPUT_SIZE = 1024
MAX_OUTPUT_SIZE = 512


class NoTestDataException(Exception):
    pass


class NoLanguageException(Exception):
    pass


class SubmissionTask:
    def __init__(self, message: bytes):
        data = json.loads(message)

        if 'submission_id' in data:
            self.type = 'Submission'
            self.submission = Submission.objects.get(id=data['submission_id'])
        elif 'contest_submission_id' in data:
            self.type = 'Contest Submission'
            self.submission = ContestSubmission.objects.get(id=data['contest_submission_id'])
        else:
            # This is unreachable
            assert False

        if 'registration_id' in data:
            self.registration = ContestRegistration.objects.get(id=int(data['registration_id']))
        else:
            self.registration = None

        self.code = data["code"]
        self.language = data["language"]
        self.problem_id = str(data["problem_id"])
        self.problem_judge_id = str(data["problem_judge_id"])
        self.problem_type = data['problem_type']
        self.time_limit = str(data["time_limit"])
        self.memory_limit = str(data["memory_limit"])
        self.testcase_detail = data["testcase_detail"]

        logger.info(f'{self.type} ID: {self.submission.id}')
        logger.info(f'Language: {self.language}')
        logger.info(f'Problem ID: {self.problem_id}')
        logger.info(f'Problem Judge ID: {self.problem_judge_id}')
        logger.info(f'Problem type: {self.problem_type}')
        logger.info(f'Time limit: {self.time_limit}')
        logger.info(f'Memory limit: {self.memory_limit}')

        logger.info(self.testcase_detail)
        logger.info(data["extra_info"])

        # 保存编译输出
        self.compile_stdout = None

        self.verdict = Verdict.Waiting
        self.score = 0
        self.results = []

        self.tmp_dir = Path(tempfile.mkdtemp())
        os.chmod(self.tmp_dir, 0o775)
        self.code_file = self.tmp_dir / ("Main." + self.language)

        if settings.DEBUG_JUDGE:
            logger.info(f'Tmp dir        {self.tmp_dir}')
            logger.info(f'Code file      {self.code_file}')

    def run(self):
        logger.info(f'Run submission {self.submission.id}')

        self.verdict = Verdict.Compiling
        self.update_submission(judged=timezone.now(), verdict=Verdict.Compiling)

        try:
            self.dump_code()
            self.compile_code()

            if self.verdict != Verdict.CompileError:
                self.verdict = Verdict.Running
                self.update_submission(verdict=Verdict.Running)
                self.judge()
        except NoTestDataException:
            self.verdict = Verdict.TestCaseError
        except NoLanguageException:
            self.verdict = Verdict.JudgeError
        finally:
            self.save_final_result()
            self.clean_temp()

    def dump_code(self):
        logger.info(f'Dump code of submission {self.submission.id}')
        code_file = io.open(self.code_file, 'w', encoding='utf8')
        code_file.write(self.code)
        code_file.close()

    def compile_code(self):
        logger.info(f'Start compiling code of submission {self.submission.id}')
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
            self.compile_stdout = e.output.decode('utf-8')[:MAX_COMPILE_OUTPUT_SIZE]
        except OSError as e:
            self.verdict = Verdict.CompileError
            logger.error(e)
        finally:
            if not settings.DEBUG_JUDGE:
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
        logger.info(f"Start judging submission {self.submission.id}")

        verdict = Verdict.Accepted
        for testcase in self.testcase_detail:
            try:
                self.prepare_testcase_file(in_file=testcase['input'], ans_file=testcase['answer'])
            except NoTestDataException:
                # Try downloading testcases from minio
                problem_directory = ProblemDirectory.make_from_id(problem_id=self.problem_id,
                                                                  problem_judge_id=self.problem_judge_id)
                problem_directory.download_testcases()
                self.prepare_testcase_file(in_file=testcase['input'], ans_file=testcase['answer'])

            self.run_sandbox()
            detail = self.read_result()

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
        logger.info(f'Finish judging, verdict is {self.verdict}')

    def prepare_testcase_file(self, in_file: str, ans_file: str):
        # TODO: extract these logic
        logger.info(f'Prepare testcase (in = {in_file}, ans = {ans_file})')
        in_file_src = os.path.join(settings.TESTCASE_ROOT, self.problem_judge_id, in_file)
        ans_file_src = os.path.join(settings.TESTCASE_ROOT, self.problem_judge_id, ans_file)
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
        contest = self.registration.contest
        if contest.type == ContestType.icpc:
            submissions = ContestSubmission.objects.filter(repository=contest.problem_repository,
                                                           owner=self.registration.team,
                                                           type=ContestSubmissionType.contestant).all()
            score = 0
            dirty = 0  # 单位：秒
            standings = []
            accepted = set()
            penalty = dict()
            penalty_unit = 20 * 60  # 20 分钟
            for sub in submissions:
                if sub.verdict == Verdict.Accepted:
                    # 第一次通过
                    if sub.problem.id not in accepted:
                        accepted.add(sub.problem.id)
                        score += 1
                        dirty += sub.relative_time
                        if sub.problem.id in penalty:
                            dirty += penalty[sub.problem.id] * penalty_unit
                elif sub.verdict in [Verdict.WrongAnswer, Verdict.TimeLimitExceeded, Verdict.IdlenessLimitExceeded,
                                     Verdict.MemoryLimitExceeded, Verdict.OutputLimitExceeded, Verdict.RuntimeError]:
                    # 添加罚时次数
                    if sub.problem.id not in penalty:
                        penalty[sub.problem.id] = 1
                    else:
                        penalty[sub.problem.id] += 1
                standings.append({
                    'id': sub.id,
                    'problem': {
                        'display_id': sub.problem.display_id,
                        'title': sub.problem.title
                    },
                    'code_length': sub.code_length,
                    'language': sub.language,
                    'created': sub.created.isoformat(),
                    'judged': sub.judged.isoformat(),
                    'relative_time': sub.relative_time,
                    'verdict': sub.verdict,
                    'score': sub.score,
                    'time_used': sub.time_used,
                    'memory_used': sub.memory_used
                })
            self.registration.score = score
            self.registration.dirty = dirty
            self.registration.standings = {'submissions': standings}
        elif contest.type == ContestType.ioi:
            pass
        self.registration.save()

    def save_final_result(self):
        logger.info(f"Save result of submission {self.submission.id}")

        detail = {
            'verdict': Verdict.Accepted,
            'score': self.score,
            'compile': {
                'stdout': ''
            },
            'node': cacathead_config.judge.name,
            'results': self.results
        }

        if self.verdict == Verdict.CompileError:
            detail['verdict'] = Verdict.CompileError
            detail['compile']['stdout'] = self.compile_stdout
        elif self.verdict in [Verdict.TestCaseError, Verdict.SystemError, Verdict.JudgeError]:
            detail['verdict'] = self.verdict
        else:
            detail['verdict'] = self.verdict

        if settings.DEBUG_JUDGE:
            logger.info(detail)

        self.update_submission(verdict=detail['verdict'], score=detail['score'], detail=detail)
        self.save_contest_result(verdict=detail['verdict'], score=detail['score'], detail=detail)

    def clean_temp(self):
        if not settings.DEBUG_JUDGE:
            logger.info(f'Clean running directory of submission {self.submission.id}')
            shutil.rmtree(self.tmp_dir)
