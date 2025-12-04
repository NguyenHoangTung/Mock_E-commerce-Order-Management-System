from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from app.models import Order, User
from app.utils.dependency import get_current_user
from app.utils.email import send_confirmation_email
import uuid
from tortoise.transactions import in_transaction
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

PAYMENT_SECRET_KEY = os.getenv("PAYMENT_SECRET_KEY")

router = APIRouter()

@router.post("/create-payment-url/{order_id}")
async def create_payment_url (
    order_id: str,
    current_user: User = Depends(get_current_user)
):
    order = await Order.get_or_none(id=order_id, user=current_user)
    if not order:
        raise HTTPException(status_code=404, detail="The bill is not exist.")
    if order.status != "PENDING":
        raise HTTPException(status_code=400, detail="Payment for this bill can't be executed.")
    gateway_url = f"http://localhost:8000/payments/mock-gateway?order_id={order_id}&amount={order.total_amount}"

    return {"payment_url": gateway_url}

@router.get("/mock-gateway", response_class=HTMLResponse)
async def gateway_page(order_id: str, amount: float):
    html_content = f"""
    <html>
        <head>
            <title>FakeBank Payment Gateway</title>
            <style>
                body {{ font-family: sans-serif; text-align: center; padding: 50px; }}
                .card {{ border: 1px solid #ccc; padding: 20px; border-radius: 10px; max-width: 400px; margin: auto; }}
                .btn {{ padding: 10px 20px; cursor: pointer; border: none; border-radius: 5px; font-size: 16px; margin: 5px; }}
                .btn-success {{ background-color: #28a745; color: white; }}
                .btn-fail {{ background-color: #dc3545; color: white; }}
            </style>
        </head>
        <body>
            <div class="card">
                <h2>FakeBank Payment</h2>
                <p>Currently paying for Bill no.: <strong>{order_id}</strong></p>
                <p>Amount: <strong>{amount} VND</strong></p>
                <hr/>
                <p>Do you accept to pay for this bill?</p>
                
                <button class="btn btn-success" onclick="confirmPayment('SUCCESS')">YES</button>
                
                <button class="btn btn-fail" onclick="confirmPayment('FAILED')">NO</button>
            </div>

            <script>
                function confirmPayment(status) {{
                    fetch('/payments/webhook', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{
                            order_id: '{order_id}',
                            status: status,
                            transaction_id: 'TRANS_' + Math.floor(Math.random() * 1000000),
                            secret_key: '{PAYMENT_SECRET_KEY}' 
                        }})
                    }})
                    .then(response => response.json())
                    .then(data => {{
                        alert(data.message);
                        window.close(); 
                    }});
                }}
            </script>
        </body>
    </html>
    """
    return html_content

@router.post("/webhook")
async def payment_webhook(payload: dict, background_tasks: BackgroundTasks):
    if payload.get("secret_key") != PAYMENT_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid Signature.")
    
    order_id = payload.get("order_id")
    status_payment = payload.get("status")
    trans_id = payload.get("transaction_id")

    order = await Order.get_or_none(id=order_id).prefetch_related("user", "items__product")
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")
    if order.status == "PAID" or order.status == "CANCELLED":
        return {"message": "The payment has been executed before."}
    if status_payment == "SUCCESS":
        order.status = "PAID"
        order.transaction_id = trans_id
        order.paid_at = datetime.utcnow()
        await order.save()   
   
        if order.user and order.user.email:
            background_tasks.add_task(
                send_confirmation_email,
                email = order.user.email,
                username = order.user.username,
                order_id = order.id,
                total_amount = order.total_amount
            )
        return {"message": "The bill has been paid successfully! The confirmation email has been sent."}
    else:
        async with in_transaction() as connection:
            order.status = "CANCELLED"
            await order.save()
            for item in order.items:
                product = item.product
                product.stock += item.quantity
                await product.save(using_db=connection)
                print(f"LOG: Hoan {item.quantity} cho {product.name}")

        return {"message": "The payment has been cancelled!"}