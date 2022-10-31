import json
import os
import shutil
import tempfile
from pathlib import Path

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone


def find_config_root(root: Path) -> Path | None:
    # TODO: not init a list
    config_path = list(root.glob('**/config.json'))
    if len(config_path) != 1:
        return None
    config_path = config_path[0]
    # TODO: check testcases exist
    return config_path.parent


def unzip_problem(problem_root: Path, file_name: str, zip_content):
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

    if root is not None:
        # clear previous data
        shutil.rmtree(problem_root)
        problem_root.mkdir(parents=True)
        # move current data
        for f in root.iterdir():
            shutil.move(f, problem_root)

    shutil.rmtree(zip_tmp)
    shutil.rmtree(problem_temp)


def upload_problem_zip(pid: int, file: InMemoryUploadedFile):
    problem_root = settings.TESTCASE_ROOT / str(pid)
    problem_root.mkdir(parents=True, exist_ok=True)
    zip_file_name = 'p' + str(pid) + '_' + str(timezone.now().timestamp()) + '.zip'
    try:
        unzip_problem(problem_root, zip_file_name, file)
        return json.load(open(problem_root / 'config.json'))
    except Exception as ex:
        print(ex)
