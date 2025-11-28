from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

class BusinessCreate(BaseModel):
    name: str = Field(..., example="Tech Solutions")
    city: str = Field(default="Unspecified", example="New York")
    country: str = Field(default="Unspecified", example="USA")
    business_description: Optional[str] = Field(None, example="A leading tech company.")
    phone_number: Optional[str] = Field(None, example="+1-234-567-8901")
    logo: Optional[str] = Field(None, example="http://example.com/logo.png")

class BusinessResponse(BaseModel):
    id: UUID
    name: str
    city: str
    country: str
    business_description: Optional[str]
    phone_number: Optional[str]
    created_at: datetime
    updated_at: datetime
    logo: Optional[str]
    owner_id: UUID

    class Config:
        from_attributes = True