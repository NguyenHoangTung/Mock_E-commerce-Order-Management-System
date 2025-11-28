from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from app.models import User
from app.schemas.user_schema import UserCreate, UserResponse, UserLogin, Token
from app.utils.password import get_password_hash, verify_password
from app.utils.token import create_access_token
from app.utils.email import send_verification_email
from tortoise.exceptions import IntegrityError
from tortoise.expressions import Q
import uuid

router = APIRouter()

  
@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, background_tasks: BackgroundTasks):
    try:
        hashed_password = get_password_hash(user.password)
        verification_token = str(uuid.uuid4())
        user_obj = await User.create(
            username=user.username,
            email=user.email,
            password=hashed_password, 
            verification_token=verification_token
        )
        print(f"LOG DEBUG - Verification token generated: {verification_token}")
        background_tasks.add_task(
            send_verification_email,
            email=user.email,
            token=verification_token,
            username=user.username
        )
        return user_obj
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists."
        )

@router.get("/verify")
async def verify(token: str):
    user = await User.get_or_none(verification_token=token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification token or expired."
        )
    if user.is_verified:
        return {"message": "User already verified."}
    user.is_verified = True
    user.verification_token = None
    await user.save()
    return {"message": "User verified successfully."}

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    user_obj = await User.get_or_none(Q(username=user.identifier) | Q(email=user.identifier))
    if not user_obj or not verify_password(user.password, user_obj.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username/email or password."
        )
    if not user_obj.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is not verified."
        )
    access_token = create_access_token(data={"sub": str(user_obj.id), "email": user_obj.email})
    return {"access_token": access_token, "token_type": "bearer"}