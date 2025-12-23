import asyncio
from app.jobs.worker import celery
from app.utils.email import send_verification_email

@celery.task
def send_verification_email_task(email: str, token: str, username: str):
    print(f"Sending verification email to {email}")
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    loop.run_until_complete(send_verification_email(email, token, username))
    print(f"Verification email sent to {email}")