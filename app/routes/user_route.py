from fastapi import APIRouter, HTTPException, status, BackgroundTasks, Request
from app.models import User
from app.schemas.user_schema import UserCreate, UserResponse, UserLogin, Token
from app.utils.password import get_password_hash, verify_password
from app.utils.token import create_access_token
from app.utils.email import send_verification_email
from tortoise.exceptions import IntegrityError
from tortoise.expressions import Q
import uuid
from loguru import logger

router = APIRouter()

  
@router.post("/register", response_model=UserResponse)
async def register(
    user: UserCreate, 
    background_tasks: BackgroundTasks,
    request: Request
):
    client_ip = request.client.host
    reg_logger = logger.bind (
        event = "registration",
        ip = client_ip,
        email = user.email
    )
    reg_logger.info("Registration attempt started")
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
        reg_logger.success("Registration successful")
        return user_obj
    except IntegrityError:
        reg_logger.warning("Registration failed: Email/Username exists")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists."
        )
    except Exception as e:
        reg_logger.error(f"Registration failed: {str(e)}")
        raise e

@router.get("/verify")
async def verify(token: str, request: Request):
    client_ip = request.client.host
    verify_logger = logger.bind(
        event = "verification",
        ip = client_ip,
        token_prefix = token[:5]
    )
    verify_logger.info("Verification attempt started")
    user = await User.get_or_none(verification_token=token)
    if not user:
        verify_logger.warning("Verification failed: Invalid token")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification token or expired."
        )
    if user.is_verified:
        verify_logger.info("Verification skipped: Already verified")
        return {"message": "User already verified."}
    user.is_verified = True
    user.verification_token = None
    await user.save()
    verify_logger.success(f"Verification successful for user {user.email}")
    return {"message": "User verified successfully."}

@router.post("/login", response_model=Token)
async def login(
    user: UserLogin,
    request: Request
):
    client_ip = request.client.host
    identifier = user.identifier
    auth_logger = logger.bind(
        event = "authentication",
        ip = client_ip,
        user = identifier,
        method = "json_login"
    )
    auth_logger.info("Login attempt started")
    user_obj = await User.get_or_none(Q(username=user.identifier) | Q(email=user.identifier))
    if not user_obj or not verify_password(user.password, user_obj.password):
        auth_logger.warning("Login failed: Invalid credentials")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username/email or password."
        )
    if not user_obj.is_verified:
        auth_logger.warning("Login failed: User is not verified")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is not verified."
        )
    auth_logger.success("Login successful")
    access_token = create_access_token(data={"sub": str(user_obj.id), "email": user_obj.email})
    return {"access_token": access_token, "token_type": "bearer"}