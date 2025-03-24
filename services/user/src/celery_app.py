import asyncio

from celery import Celery

import config

from src.auth import TokenManager

celery_app = Celery("tasks", broker=config.CELERY_BROKER_URL)


@celery_app.task
async def delete_refresh(user_id: int):
    await TokenManager().delete_refresh(user_id)


@celery_app.task
def delete_refresh_task(user_id: int):
    asyncio.run(delete_refresh(user_id))
