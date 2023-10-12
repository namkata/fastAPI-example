from celery import Celery
from core.config import settings

celery = Celery(__name__)

celery.conf.broker_url = settings.celery_broker_url
celery.conf.result_backend = settings.celery_result_backend


@celery.task(name="create_task")
def create_task(task_type):
    return True
