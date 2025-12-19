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

async def send_confirmation_email(email: EmailStr, username: str, order_id: str, total_amount: float):
    html = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px; border: 1px solid #ddd;">
        <h2 style="color: #28a745;">Payment Successful!</h2>
        <p>Greetings <strong>{username}</strong>,</p>
        <p>Your Order <strong>#{order_id}</strong> has been confirmed.</p>
        <hr/>
        <p>With total payment: <strong style="font-size: 18px;">{total_amount:,.0f} VND</strong></p>
        <p>We will soon finish the packaging and send the products to you.</p>
        <br/>
        <p>Thanks for buying!</p>
    </div>
    """

    message = MessageSchema(
        subject="Payment confirmation for Order {order_id}",
        recipients=[email],
        body=html,
        subtype="html",
    )
    fm = FastMail(conf)
    await fm.send_message(message)