import time

from celery import Celery
from settings.config import settings

celery = Celery(__name__)

celery.conf.broker_url = settings.celery_broker_url
celery.conf.result_backend = settings.celery_result_backend


@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(10)
    return True
