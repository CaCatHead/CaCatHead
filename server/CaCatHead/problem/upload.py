import os
import shutil
import tempfile
from pathlib import Path

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone


def unzip_problem(problem_root: Path, file_name: str, zip_content):
    tmp_dir = tempfile.mkdtemp()
    os.chmod(tmp_dir, 0o775)
    file_path = Path(tmp_dir) / file_name

    # 指定文件的修改时间, 如果时间是 None, 则文件的访问和修改设为当前时间;
    # 否则, 时间是一个 2-tuple 数字, (atime, mtime) 用来分别作为访问和修改的时间.
    with open(file_path, 'a'):
        os.utime(file_path, None)

    with open(file_path, 'wb+') as zip_file:
        for chunk in zip_content.chunks():
            zip_file.write(chunk)

    shutil.unpack_archive(file_path, problem_root)
    shutil.rmtree(tmp_dir)


def upload_problem_zip(pid: int, file: InMemoryUploadedFile):
    problem_root = settings.TESTCASE_ROOT / str(pid)
    problem_root.mkdir(parents=True, exist_ok=True)
    zip_file_name = 'p' + str(pid) + '_' + str(timezone.now().timestamp()) + '.zip'
    try:
        unzip_problem(problem_root, zip_file_name, file)
    except Exception as ex:
        print(ex)
