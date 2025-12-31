from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from app.models import Order, User
from app.utils.dependency import get_current_user
from app.utils.email import send_confirmation_email
from app.services.payment_service import PaymentService
from fastapi.templating import Jinja2Templates  
import os
from dotenv import load_dotenv
load_dotenv()

PAYMENT_SECRET_KEY = os.getenv("PAYMENT_SECRET_KEY")

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_payment_service():
    return PaymentService()

@router.post("/create-payment-url/{order_id}")
async def create_payment_url (
    order_id: str,
    current_user: User = Depends(get_current_user),
    service: PaymentService = Depends(get_payment_service)
):
    payment_link = await service.create_payment_link(order_id, current_user)
    return {"payment_url": payment_link}

@router.get("/mock-gateway", response_class=HTMLResponse)
async def gateway_page(request: Request, order_id: str, amount: float):
    secret_key = os.getenv("PAYMENT_SECRET_KEY")
    return templates.TemplateResponse("payment/gateway.html", 
        {
            "request": request,
            "order_id": order_id,
            "amount": amount,
            "secret_key": secret_key
        }
    )

@router.post("/webhook")
async def payment_webhook(payload: dict, background_tasks: BackgroundTasks, service: PaymentService = Depends(get_payment_service)):
    result = await service.process_webhook(payload)

    if result.get("action") == "send_email":
        order = result.get("order")
        if order and order.user and order.user.email:
            background_tasks.add_task(
                send_confirmation_email,
                email=order.user.email,
                username=order.user.username,
                order_id=order.id,
                total_amount=order.total_amount
            )            
            
    return {"message": result.get("message")}