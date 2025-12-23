import os
from celery import Celery
from dotenv import load_dotenv
load_dotenv()

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')

celery = Celery(__name__, include=['app.jobs.tasks'])

celery.conf.broker_url = CELERY_BROKER_URL
celery.conf.result_backend = CELERY_RESULT_BACKEND

celery.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)