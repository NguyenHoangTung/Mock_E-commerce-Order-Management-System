from fastapi import APIRouter, HTTPException, status, Depends
from app.models import Business, User
from app.schemas.business_schema import BusinessCreate, BusinessResponse
from app.utils.dependency import get_current_user
from tortoise.exceptions import IntegrityError

router = APIRouter()

@router.post("/", response_model=BusinessResponse)
async def create_business(
    business: BusinessCreate,
    current_user: User = Depends(get_current_user)
):
    try:
        business_obj = await Business.create(
            name=business.name,
            city=business.city,
            country=business.country,
            business_description=business.business_description,
            phone_number=business.phone_number,
            logo=business.logo,
            owner=current_user
        )
        return business_obj
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Business with this name already exists."
        )
    
@router.get("/my-businesses", response_model=list[BusinessResponse])
async def get_my_businesses(
    current_user: User = Depends(get_current_user)
):
    businesses = await Business.filter(owner=current_user)
    return businesses