from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from typing import List
from dotenv import load_dotenv
import os
load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME = os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD"),
    MAIL_FROM = os.getenv("MAIL_FROM"),
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

async def send_verification_email(email: EmailStr, token: str, username: str):
    verification_link = f"http://localhost:8000/users/verify?token={token}"
    html = f"""
    <h3>Hello {username},</h3>
    <p>Please verify your email by clicking on the following link:</p>
    <a href="{verification_link}">Verify Email</a>
    <p>Thank you!</p>
    """
    message = MessageSchema(
        subject="Email Verification",
        recipients=[email],
        body=html,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)