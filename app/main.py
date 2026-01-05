import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from tortoise.contrib.fastapi import register_tortoise

from app.api.v1 import api_router
from app.core.config import settings
from app.core.db import TORTOISE_ORM
from app.middleware import log_middleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    swagger_ui_parameters={"persistAuthorization": True}
)

if not os.path.exists("static"):
    os.makedirs("static")
    
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)

app.include_router(api_router, prefix=settings.API_V1_STR)

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False,
    add_exception_handlers=True,
)