from pydantic import BaseModel, Field
from typing import List
from uuid import UUID
from datetime import datetime
from decimal import Decimal

class CartItem(BaseModel):
    product_id: UUID
    quantity: int = Field(..., gt=0)

class CartItemResponse(BaseModel):
    product_id: UUID
    product_name: str
    quantity: int
    price: Decimal


class OrderResponse(BaseModel):
    id: UUID
    status: str
    total_amount: Decimal
    shipping_address: str
    created_at: datetime
    items: List[CartItemResponse] = []

    class Config:
        from_attributes = True

class CreateOrder(BaseModel):
    items: List[CartItem]
    shipping_address: str

