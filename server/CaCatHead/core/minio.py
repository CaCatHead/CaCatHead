from pathlib import Path

from minio import Minio

from CaCatHead.config import cacathead_config

TESTCASE_BUCKET = cacathead_config.testcase.minio.bucket


# Get MinIO Client
def get_minio_client():
    minio_url = f'{cacathead_config.testcase.minio.host}:{cacathead_config.testcase.minio.port}'
    minio_client = Minio(minio_url,
                         access_key=cacathead_config.testcase.minio.username,
                         secret_key=cacathead_config.testcase.minio.password,
                         secure=False) if cacathead_config.testcase.minio.host != 'N/A' else None

    if minio_client is not None:
        print(f'Connecting to MinIO at {minio_url}...')
        if not minio_client.bucket_exists(TESTCASE_BUCKET):
            minio_client.make_bucket(TESTCASE_BUCKET)
    else:
        print(f'Fail connecting MinIO')

    return minio_client


MINIO_CLIENT = get_minio_client()


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
