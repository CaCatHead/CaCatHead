import json
import logging
import os
import shutil
import tempfile
import zipfile
from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone

from CaCatHead.core.minio import upload_minio_testcase, download_minio_testcase
from CaCatHead.problem.models import Problem, DefaultCheckers
from CaCatHead.problem.serializers import TestcaseInfoPayload

logger = logging.getLogger(__name__)


def get_testcase_root(problem: Problem = None, problem_judge_id=None) -> Path:
    if problem is not None:
        problem_judge = problem.problem_info.problem_judge
        return settings.TESTCASE_ROOT / f'p{problem_judge.id}'
    else:
        return settings.TESTCASE_ROOT / f'p{problem_judge_id}'


def get_testcase_root_version(problem: Problem = None, problem_judge_id=None) -> Path:
    directory = get_testcase_root(problem=problem, problem_judge_id=problem_judge_id)
    return directory / 'version'


def read_testcase_root_version(problem: Problem = None, problem_judge_id=None) -> int:
    path = get_testcase_root_version(problem=problem, problem_judge_id=problem_judge_id)
    if path.exists():
        return int(path.read_text(encoding='UTF-8'))
    else:
        return -1


def write_testcase_root_version(problem: Problem = None, problem_judge_id=None):
    path = get_testcase_root_version(problem=problem, problem_judge_id=problem_judge_id)
    path.write_text(str(problem.problem_info.problem_judge.testcase_version), encoding='UTF-8')


class ProblemDirectory:
    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        config_path = self.root / 'config.json'
        if not config_path.exists():
            json.dump({'problem': {}, 'testcases': [], 'checker': {}}, open(config_path, 'w'))
        self.config = json.load(open(config_path, encoding='UTF-8'))

    @classmethod
    def make(cls, problem: Problem):
        return ProblemDirectory(root=get_testcase_root(problem))

    @classmethod
    def try_make(cls, problem: Problem):
        root = get_testcase_root(problem)
        if not root.exists():
            problem_directory = ProblemDirectory(root=root)
            problem_directory.config['testcases'] = problem.problem_info.problem_judge.testcase_detail
            problem_directory.save_config(problem)
            return problem_directory
        else:
            return ProblemDirectory(root=root)

    def check_valid(self):
        if 'testcases' not in self.config:
            # 必须包含 testcases
            return False

        testcases = self.config['testcases']
        if not isinstance(testcases, list):
            # testcases 必须是数组
            return False

        for testcase in testcases:
            serializer = TestcaseInfoPayload(data=testcase)
            if not serializer.is_valid(raise_exception=False):
                # 输入不合法
                return False
            input_file = self.root / testcase['input']
            answer_file = self.root / testcase['answer']
            if not input_file.exists() or not answer_file.exists():
                # 输入或输出文件不存在
                return False

        return True

    def save_config(self, problem: Problem):
        problem_info = self.config['problem']
        problem_info['title'] = problem.problem_info.problem_content.title
        problem_info['problem_type'] = problem.problem_info.problem_judge.problem_type
        problem_info['time_limit'] = problem.problem_info.problem_judge.time_limit
        problem_info['memory_limit'] = problem.problem_info.problem_judge.memory_limit
        problem_info['description'] = problem.problem_info.problem_content.description
        problem_info['input'] = problem.problem_info.problem_content.input
        problem_info['output'] = problem.problem_info.problem_content.output
        problem_info['sample'] = problem.problem_info.problem_content.sample
        problem_info['hint'] = problem.problem_info.problem_content.hint
        problem_info['source'] = problem.problem_info.problem_content.source
        problem_info['extra_content'] = problem.problem_info.problem_content.extra_content
        problem_info['extra_judge'] = problem.problem_info.problem_judge.extra_info

        if 'checker' in self.config:
            checker_info = self.config['checker']
        else:
            checker_info = {}
            self.config['checker'] = checker_info
        checker_info['type'] = problem.problem_info.problem_judge.checker
        if problem.problem_info.problem_judge.checker == DefaultCheckers.custom:
            checker_info['language'] = problem.problem_info.problem_judge.custom_checker.language
            checker_info['code'] = problem.problem_info.problem_judge.custom_checker.code

        json.dump(self.config, open(self.root / 'config.json', 'w', encoding='UTF-8'), indent=2, ensure_ascii=False)

    def upload_testcases(self) -> bool:
        directory = self.root.name
        for testcase in self.config['testcases']:
            if not upload_minio_testcase(directory, self.root / testcase['input']):
                return False
            if not upload_minio_testcase(directory, self.root / testcase['answer']):
                return False
        return True

    def download_testcases(self) -> bool:
        directory = self.root.name
        for testcase in self.config['testcases']:
            input_file = self.root / testcase['input']
            if not input_file.exists():
                if not download_minio_testcase(directory, input_file):
                    return False
            answer_file = self.root / testcase['answer']
            if not answer_file.exists():
                if not download_minio_testcase(directory, answer_file):
                    return False
        return True

    def generate_zip(self):
        mem_zip = BytesIO()
        with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            root_length = len(str(self.root))
            for root, dirs, files in os.walk(self.root):
                folder = root[root_length:]
                for file in files:
                    zf.write(os.path.join(root, file), os.path.join(folder, file))
        return mem_zip.getvalue()


def find_config_root(root: Path) -> Path | None:
    # TODO: not init a list
    config_path = list(root.glob('**/config.json'))
    if len(config_path) != 1:
        return None
    config_path = config_path[0]
    return config_path.parent


def try_unzip_problem_arch(problem_root: Path, file_name: str, zip_content: InMemoryUploadedFile) -> bool:
    zip_tmp = tempfile.mkdtemp()
    os.chmod(zip_tmp, 0o775)
    zip_path = Path(zip_tmp) / file_name

    # 指定文件的修改时间, 如果时间是 None, 则文件的访问和修改设为当前时间;
    # 否则, 时间是一个 2-tuple 数字, (atime, mtime) 用来分别作为访问和修改的时间.
    with open(zip_path, 'a'):
        os.utime(zip_path, None)

    with open(zip_path, 'wb+') as zip_file:
        for chunk in zip_content.chunks():
            zip_file.write(chunk)

    problem_temp = tempfile.mkdtemp()
    os.chmod(problem_temp, 0o775)
    shutil.unpack_archive(zip_path, problem_temp)
    root = find_config_root(Path(problem_temp))

    valid = False

    if root is not None:
        problem_dir = ProblemDirectory(root)
        if problem_dir.check_valid():
            valid = True
            # clear previous data
            shutil.rmtree(problem_root)
            problem_root.mkdir(parents=True)
            # move current data
            for f in root.iterdir():
                shutil.move(f, problem_root)

    shutil.rmtree(zip_tmp)
    shutil.rmtree(problem_temp)

    return valid


def upload_problem_arch(problem: Problem, file: InMemoryUploadedFile) -> ProblemDirectory:
    problem_judge_id = problem.problem_info.problem_judge.id
    problem_root = get_testcase_root(problem)
    problem_root.mkdir(parents=True, exist_ok=True)
    zip_file_name = 'p' + str(problem_judge_id) + '_' + str(timezone.now().timestamp()) + '.zip'
    try:
        if try_unzip_problem_arch(problem_root, zip_file_name, file):
            problem_directory = ProblemDirectory(problem_root)
            if problem_directory.upload_testcases():
                write_testcase_root_version(problem)
                return problem_directory
            else:
                logger.error("Upload testcases to MinIO fail")
                return None
        else:
            return None
    except Exception as ex:
        logger.error("Upload problem arch fail: %r", ex)
        return None
