from asgiref.sync import async_to_sync
from loguru import logger

from app.jobs.worker import celery
from app.utils.email import send_verification_email


@celery.task
def send_verification_email_task(email: str, token: str, username: str):
    logger.info(f"Sending verification email to {email}")
    async_to_sync(send_verification_email)(email, token, username)
    logger.info(f"Verification email sent to {email}")

