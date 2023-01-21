import logging

from CaCatHead.config import cacathead_config
from CaCatHead.contest.models import Team
from CaCatHead.core.celery import app
from CaCatHead.judge.services.payload import JudgeSubmissionPayload
from CaCatHead.judge.services.ping import handle_ping
from CaCatHead.judge.services.submission import SubmissionTask
from CaCatHead.problem.models import Problem
from CaCatHead.submission.models import ContestSubmission, ContestSubmissionType

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
def prepare_contest_problem_submission(payload: JudgeSubmissionPayload):
    try:
        logger.info(f'Prepare contest problem')
        problem = Problem.objects.get(id=payload.problem_id)
        owner = Team.objects.get(id=payload.owner_id)
        contest_submission = ContestSubmission(
            type=ContestSubmissionType.manager,
            repository=problem.repository,
            problem=problem,
            owner=owner,
            code=payload.code,
            code_length=len(payload.code),
            language=payload.language,
            relative_time=-1
        )
        contest_submission.save()
        payload.contest_submission_id = contest_submission.id
        task = SubmissionTask(payload=payload)
        task.run()
        contest_submission.delete()
        logger.info(f'Handle prepare contest problem OK')
        return {'ok': True}
    except Exception as ex:
        logger.info(f'Handle prepare contest problem fails: %r', ex)
        return {'ok': False}


@app.task()
def judge_repository_submission(payload: JudgeSubmissionPayload):
    logger.info(f'Receive a new repository submission #{payload.submission_id}.')
    task = SubmissionTask(payload)
    task.run()
    logger.info(f'Handle repository submission #{payload.submission_id}. OK')
    return {'ok': True}


@app.task()
def judge_contest_submission(payload: JudgeSubmissionPayload):
    logger.info(f'Receive a new contest submission #{payload.contest_submission_id}.')
    task = SubmissionTask(payload=payload)
    task.run()
    logger.info(f'Handle contest submission #{payload.contest_submission_id}. OK')
    return {'ok': True}


@app.task()
def judge_polygon_submission(payload: JudgeSubmissionPayload):
    logger.info(f'Receive a new polygon submission #{payload.submission_id}.')
    task = SubmissionTask(payload)
    task.run()
    logger.info(f'Handle polygon submission #{payload.submission_id}. OK')
    return {'ok': True}
