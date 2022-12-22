from pathlib import Path

from minio import Minio

from CaCatHead.config import cacathead_config

# MinIO
MINIO_PATH = f'{cacathead_config.testcase.minio.host}:{cacathead_config.testcase.minio.port}'
MINIO_CLIENT = Minio(MINIO_PATH,
                     access_key=cacathead_config.testcase.minio.username,
                     secret_key=cacathead_config.testcase.minio.password) if cacathead_config.testcase.minio.host != 'N/A' else None

if MINIO_CLIENT is not None:
    print(f'Connecting to MinIO at {MINIO_PATH}')
    if not MINIO_CLIENT.bucket_exists(cacathead_config.testcase.minio.bucket):
        MINIO_CLIENT.make_bucket(cacathead_config.testcase.minio.bucket)
else:
    print(f'Fail connecting MinIO')


def upload_minio_testcase(dir: str, file: Path):
    if MINIO_CLIENT is None:
        return False

    return True


def download_minio_testcase(dir: str, file: Path):
    if MINIO_CLIENT is None:
        return False

    return True
