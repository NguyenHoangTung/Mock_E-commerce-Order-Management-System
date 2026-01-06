from fastapi import APIRouter

from app.api.routes import (
    business_router,
    order_router,
    payment_router,
    product_router,
    upload_router,
    user_router,
)

api_router = APIRouter()
api_router.include_router(user_router)
api_router.include_router(business_router)
api_router.include_router(upload_router)
api_router.include_router(product_router)
api_router.include_router(order_router)
api_router.include_router(payment_router)

