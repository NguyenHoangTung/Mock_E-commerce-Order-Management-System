from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    is_verified: bool
    join_date: datetime

    class Config:
        from_attributes = True