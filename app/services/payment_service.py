# app/services/payment_service.py
import os
from datetime import datetime

from fastapi import HTTPException
from tortoise.transactions import atomic

from app.constants import OrderStatus, PaymentStatus
from app.core.config import settings
from app.models import Order, User


class PaymentService:
    def __init__(self):
        self.secret_key = settings.PAYMENT_SECRET_KEY

    async def create_payment_link(self, order_id: str, user: User) -> str:
        order = await Order.get_or_none(id=order_id, user=user)
        if not order:
            raise HTTPException(status_code=404, detail="The bill is not exist.")
        if order.status != OrderStatus.PENDING:
            raise HTTPException(status_code=400, detail="Payment for this bill can't be executed.")      
        gateway_url = f"http://localhost:8000{settings.API_V1_STR}/payments/mock-gateway?order_id={order_id}&amount={order.total_amount}"
        return gateway_url

    @atomic() 
    async def process_webhook(self, payload: dict):
        if payload.get("secret_key") != self.secret_key:
            raise HTTPException(status_code=403, detail="Invalid Signature.")

        order_id = payload.get("order_id")
        status_payment = payload.get("status")
        trans_id = payload.get("transaction_id")

        order = await Order.get_or_none(id=order_id).select_for_update().prefetch_related("user", "items__product")      
        if not order:
            raise HTTPException(status_code=404, detail="Order not found.")
        if order.status in [OrderStatus.PAID, OrderStatus.CANCELLED]:
            return {"message": "The payment has been executed before.", "action": "none"}

        if status_payment == PaymentStatus.SUCCESS:
            order.status = OrderStatus.PAID
            order.transaction_id = trans_id
            order.paid_at = datetime.utcnow()
            await order.save()
            
            return {
                "message": "The bill has been paid successfully!", 
                "action": "send_email",
                "order": order 
            }
        else:
            order.status = OrderStatus.CANCELLED
            await order.save()

            for item in order.items:
                product = item.product
                product.stock += item.quantity
                await product.save()
                print(f"LOG: Restored {item.quantity} stock for {product.name}")

            return {"message": "The payment has been cancelled!", "action": "none"}