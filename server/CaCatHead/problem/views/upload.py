import json
import os
import shutil
import tempfile
from pathlib import Path

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone

from CaCatHead.problem.serializers import TestcaseInfoPayload


class ProblemDirectory:
    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.config = json.load(open(root / 'config.json'))

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


def find_config_root(root: Path) -> Path | None:
    # TODO: not init a list
    config_path = list(root.glob('**/config.json'))
    if len(config_path) != 1:
        return None
    config_path = config_path[0]
    return config_path.parent


def unzip_problem(problem_root: Path, file_name: str, zip_content: InMemoryUploadedFile):
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


def upload_problem_zip(pid: int, file: InMemoryUploadedFile):
    problem_root = settings.TESTCASE_ROOT / str(pid)
    problem_root.mkdir(parents=True, exist_ok=True)
    zip_file_name = 'p' + str(pid) + '_' + str(timezone.now().timestamp()) + '.zip'
    try:
        if unzip_problem(problem_root, zip_file_name, file):
            return json.load(open(problem_root / 'config.json'))
        else:
            return None
    except Exception:
        return None
