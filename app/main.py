import os

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.exceptions import HTTPException as StarletteHTTPException
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

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    message = "Validation errors:"
    for error in exc.errors():
        message += f"\nField: {error['loc']}, Error: {error['msg']}"
    return PlainTextResponse(message, status_code=400)

if not os.path.exists("static"):
    os.makedirs("static")
    
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)

app.include_router(api_router, prefix=settings.API_V1_STR)

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)

Instrumentator().instrument(app).expose(app)


