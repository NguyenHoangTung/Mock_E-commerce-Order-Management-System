from fastapi import APIRouter, HTTPException, status
from app.models import User
from app.schemas.user_schema import UserCreate, UserResponse
from app.utils.password import get_password_hash
from tortoise.exceptions import IntegrityError

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    try:
        print(f"LOG DEBUG - Password before hashing: {user.password}")
        print(f"LOG DEBUG - Length of password: {len(user.password)}")
        hashed_password = get_password_hash(user.password)
        user_obj = await User.create(
            username=user.username,
            email=user.email,
            password=hashed_password 
        )
        return user_obj
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists."
        )

