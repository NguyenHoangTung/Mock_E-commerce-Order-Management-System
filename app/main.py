import os
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.routes import user_router, business_router, upload_router
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="E-commerce Order Management System")

DATABASE_URL = os.getenv("DATABASE_URL")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(business_router, prefix="/businesses", tags=["businesses"])
app.include_router(upload_router, prefix="/upload", tags=["upload"])

register_tortoise(
    app,
    db_url=DATABASE_URL,
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

@app.get("/")
async def root():
    return {"message": "Welcome to the E-commerce Order Management System API"}