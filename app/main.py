import os
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.routes import user_router, business_router, upload_router, product_router, order_router, payment_router
from fastapi.staticfiles import StaticFiles
from .db_config import TORTOISE_ORM
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="E-commerce Order Management System", swagger_ui_parameters={"persistAuthorization": True})

DATABASE_URL = os.getenv("DATABASE_URL")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(business_router, prefix="/businesses", tags=["businesses"])
app.include_router(upload_router, prefix="/upload", tags=["upload"])
app.include_router(product_router, prefix="/products", tags=["products"])
app.include_router(order_router, prefix="/orders", tags=["orders"])
app.include_router(payment_router, prefix="/payments", tags=["payments"])

register_tortoise(
    app,
    config=TORTOISE_ORM,
    modules={"models": ["app.models"]},
    generate_schemas=False,
    add_exception_handlers=True,
)

@app.get("/")
async def root():
    return {"message": "Welcome to the E-commerce Order Management System API"}