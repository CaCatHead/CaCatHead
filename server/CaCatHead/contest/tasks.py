import logging

from CaCatHead.contest.models import ContestRegistration
from CaCatHead.contest.services.standings import refresh_registration_standing
from CaCatHead.core.celery import app

logger = logging.getLogger(__name__)


@app.task(ignore_result=True)
def refresh_standing(response, registration_id: int):
    try:
        logger.info(f'Receive a new refresh registration #{registration_id}. standing task')
        registration = ContestRegistration.objects.get(id=registration_id)
        if registration is not None:
            refresh_registration_standing(registration=registration)
        logger.info('Refresh registration standing OK')
    except Exception as ex:
        logger.info(f'Refresh registration standing fails: %r', ex)
