from pydantic import BaseModel, Field, computed_field, ConfigDict
from decimal import Decimal
from typing import Optional, Any
from datetime import datetime
from uuid import UUID
from app.models import Business

class ProductCreate(BaseModel):
    name: str = Field(..., example="Laptop")
    category: str = Field(..., example="Electronics")
    original_price: float = Field(..., example=999.99)
    discount_percentage: Optional[int] = Field(None, example=10)
    stock: int = Field(..., example=50)
    image: Optional[str] = Field(None, example="http://example.com/image.png")
    business_id: UUID = Field(..., example="123e4567-e89b-12d3-a456-426614174000")

class ProductResponse(BaseModel):
    id: UUID
    name: str
    category: str
    sale_price: Decimal
    stock: int
    image: Optional[str]
    business: Any = Field(exclude=True)
    created_at: datetime
    updated_at: datetime
    business_id: UUID

    @computed_field
    def business_name(self) -> str:
        return self.business.name if self.business else "Unknown"

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Laptop")
    category: Optional[str] = Field(None, example="Electronics")
    original_price: Optional[float] = Field(None, example=999.99)
    discount_percentage: Optional[int] = Field(None, example=10)
    stock: Optional[int] = Field(None, example=50)
    image: Optional[str] = Field(None, example="http://example.com/image.png")