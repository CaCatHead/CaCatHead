import os
import io
import json
import shutil
import logging
import subprocess
import tempfile
from pathlib import Path

from django.conf import settings


logger = logging.getLogger('Judge.service')


class NoTestDataException(Exception):
    pass


class NoLanguageException(Exception):
    pass


class Submission:
    def __init__(self, message: bytes):
        data = json.loads(message)
        logger.info(data)

        self.status_id = data['status_id']
        self.code = data["code"]
        self.language = data["lang"]
        self.problem_id = str(data["problem_id"])
        self.time_limit = str(data["time_limit"])
        self.memory_limit = str(data["memory_limit"])
        self.testcase_detail = data["testcase_detail"]
        # self.case_count = int(data["casecount"])
        # self.case_score = data["casescore"]
        # self.pro_solved_rec_id = int(data["prosolvedrecid"])

        self.lang = 0
        self.compiler_output = None
        self.result = {"result": []}
        self.is_compile_error = False

        self.tmp_dir = Path(tempfile.mkdtemp())
        os.chmod(self.tmp_dir, 0o775)
        self.code_file = self.tmp_dir / ("Main." + self.language)

        # logging.info("data id is: %s" % self.status_id)

    def run(self):
        logger.info(f'Run submission at {self.tmp_dir}')

        try:
            self.dump_code()

            self.compile_code_exec()

            if not self.is_compile_error:
                self.judge()

            self._save_result()
        except NoTestDataException:
            self.result = 'NoTestDataError'
        except NoLanguageException:
            self.result = 'NoLanguageError'
        finally:
            self.clean_temp()

    def dump_code(self):
        logger.info(f'Dump code to {self.code_file}')
        code_file = io.open(self.code_file, 'w', encoding='utf8')
        code_file.write(self.code)
        code_file.close()

    def compile_code_exec(self):
        logger.info(f'Start compiling code {self.code_file}')
        if self.language == 'cpp':
            self.lang = '2'
            commands = ["g++", self.code_file, "-o", "Main", "-static", "-w",
                        "-lm", "-std=c++11", "-O2", "-DONLINE_JUDGE"]
        elif self.language == 'c':
            self.lang = '1'
            commands = ["gcc", self.code_file, "-o", "Main", "-static", "-w",
                        "-lm", "-std=c11", "-O2", "-DONLINE_JUDGE"]
        elif self.language == 'java':
            self.lang = '3'
            commands = ["javac", self.code_file, "-d", "."]
        else:
            raise NoLanguageException

        cwd = Path(tempfile.mkdtemp())
        os.chmod(cwd, 0o775)
        try:
            subprocess.check_output(commands, stderr=subprocess.STDOUT, cwd=cwd)
            self.prepare_exec_file(cwd)
        except subprocess.CalledProcessError as e:
            self.is_compile_error = True
            self.compiler_output = e.output
        except OSError as e:
            self.is_compile_error = True
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
            self.read_result()
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
        commands = ["catj", "-t", self.time_limit,
                    "-m", self.memory_limit, "-d", self.tmp_dir, "-l", self.lang]
        subprocess.call(commands)

    def read_result(self):
        logger.info("Read one case result")
        result_file = open(os.path.join(self.tmp_dir, "result.txt"), 'r')
        status = result_file.readline().strip()
        run_time = result_file.readline().strip()
        run_memory = result_file.readline().strip()
        others = result_file.readline().strip()
        one_case_result = dict((["status", status], ["runtime", run_time], ["runmemory", run_memory], ["message", others]))
        self.result["result"].append(one_case_result)

    def _save_result(self):
        logger.info("Save result, result is %s" % self.result)
        # self.save_result_callback(
        #     status_id = self.status_id,
        #     detail = self.result,
        #     case_score = self.case_score,
        #     compiler_output = self.compiler_output,
        #     is_compile_error = self.is_compile_error,
        #     pro_solved_rec_id = self.pro_solved_rec_id
        # )

    def clean_temp(self):
        logger.info("Clean submission running directory")
        shutil.rmtree(self.tmp_dir)
