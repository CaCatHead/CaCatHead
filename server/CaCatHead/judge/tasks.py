import logging

from CaCatHead.config import cacathead_config
from CaCatHead.core.celery import app
from CaCatHead.judge.services.payload import JudgeSubmissionPayload
from CaCatHead.judge.services.ping import handle_ping
from CaCatHead.judge.services.submission import SubmissionTask

logger = logging.getLogger(__name__)


@app.task(ignore_result=True)
def ping(timestamp: str):
    logger.info(f'Receive a new ping task')
    try:
        handle_ping(timestamp)
        logger.info(f'Judge node {cacathead_config.judge.name} handles ping task OK')
    except Exception as ex:
        logger.info(f'Judge node {cacathead_config.judge.name} fails handling ping task: %r', ex)


@app.task()
def judge_repository_submission(payload: JudgeSubmissionPayload):
    logger.info(f'Receive a new repository submission #{payload.submission_id}.')
    task = SubmissionTask(payload)
    task.run()
    logger.info(f'Handle repository submission #{payload.submission_id}. OK')


@app.task()
def judge_contest_submission(payload: JudgeSubmissionPayload):
    logger.info(f'Receive a new contest submission #{payload.contest_submission_id}.')
    task = SubmissionTask(payload=payload)
    task.run()
    logger.info(f'Handle contest submission #{payload.contest_submission_id}. OK')


@app.task()
def judge_polygon_submission(payload: JudgeSubmissionPayload):
    logger.info(f'Receive a new polygon submission #{payload.submission_id}.')
    task = SubmissionTask(payload)
    task.run()
    logger.info(f'Handle polygon submission #{payload.submission_id}. OK')
