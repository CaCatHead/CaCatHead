import logging

from CaCatHead.config import cacathead_config
from CaCatHead.contest.models import ContestRegistration
from CaCatHead.core.celery import app
from CaCatHead.judge.services.ping import handle_ping
from CaCatHead.judge.services.submission import SubmissionTask
from CaCatHead.submission.models import ContestSubmission, Submission

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
def judge_repository_submission(submission_id: int):
    logger.info(f'Receive a new repository submission')
    submission = Submission.objects.get(id=submission_id)
    task = SubmissionTask(submission=submission)
    task.run()


@app.task()
def judge_contest_submission(contest_submission_id: int, registration_id: int):
    logger.info(f'Receive a new contest submission')
    contest_submission = ContestSubmission.objects.get(id=contest_submission_id)
    registration = ContestRegistration.objects.get(id=registration_id) if registration_id >= 0 else None
    task = SubmissionTask(contest_submission=contest_submission, registration=registration)
    task.run()


@app.task()
def judge_polygon_submission(submission_id: int):
    logger.info(f'Receive a new polygon submission')
    submission = Submission.objects.get(id=submission_id)
    task = SubmissionTask(submission=submission)
    task.run()
