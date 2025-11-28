from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional
from uuid import UUID

class ProductCreate(BaseModel):
    name: str = Field(..., example="Laptop")
    category: str = Field(..., example="Electronics")
    original_price: float = Field(..., example=999.99)
    discount_percentage: Optional[int] = Field(None, example=10)
    stock: int = Field(..., example=50)
    image: Optional[str] = Field(None, example="http://example.com/image.png")

class ProductResponse(BaseModel):
    id: UUID
    name: str
    category: str
    sale_price: Decimal
    stock: int
    image: Optional[str]
    created_at: str
    updated_at: str
    business_id: UUID

    class Config:
        from_attributes = True