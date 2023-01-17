import logging

from CaCatHead.core.celery import app
from CaCatHead.judge.services.payload import JudgeResponsePayload

logger = logging.getLogger(__name__)


@app.task(ignore_result=True)
def refresh_registration_standing(payload: JudgeResponsePayload):
    logger.info(f'Receive a new refresh registration standing task')
    try:
        # handle_ping(timestamp)
        logger.info('Refresh registration standing OK')
    except Exception as ex:
        logger.info(f'Refresh registration standing fails: %r', ex)
