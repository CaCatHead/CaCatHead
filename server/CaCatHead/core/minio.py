from pathlib import Path

from minio import Minio

from CaCatHead.config import cacathead_config

TESTCASE_BUCKET = cacathead_config.testcase.minio.bucket

# MinIO
MINIO_PATH = f'{cacathead_config.testcase.minio.host}:{cacathead_config.testcase.minio.port}'
MINIO_CLIENT = Minio(MINIO_PATH,
                     access_key=cacathead_config.testcase.minio.username,
                     secret_key=cacathead_config.testcase.minio.password,
                     secure=False) if cacathead_config.testcase.minio.host != 'N/A' else None

if MINIO_CLIENT is not None:
    print(f'Connecting to MinIO at {MINIO_PATH}...')
    if not MINIO_CLIENT.bucket_exists(TESTCASE_BUCKET):
        MINIO_CLIENT.make_bucket(TESTCASE_BUCKET)
else:
    print(f'Fail connecting MinIO')


def upload_minio_testcase(problem_dir: str, file: Path):
    if MINIO_CLIENT is None:
        return False
    result = MINIO_CLIENT.fput_object(TESTCASE_BUCKET, f'{problem_dir}/{file.name}', str(file))
    return result.bucket_name == TESTCASE_BUCKET


def download_minio_testcase(problem_dir: str, file: Path):
    if MINIO_CLIENT is None:
        return False
    result = MINIO_CLIENT.fget_object(TESTCASE_BUCKET, f'{problem_dir}/{file.name}', str(file))
    return result.bucket_name == TESTCASE_BUCKET
