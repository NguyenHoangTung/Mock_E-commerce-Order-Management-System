from fastapi import Request
from loguru import logger
import time
import uuid
import sys

logger.remove()
logger.add(sys.stderr, colorize=True, format="<green>{time}</green> <cyan>{level}</cyan> <magenta>{message}</magenta> <yellow>{extra}</yellow>", level="INFO")
logger.add("logs/app.log", rotation="1 day", retention="10 days", level="DEBUG")

async def log_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()
    logger.info(f"Request ID: {request_id} - Method: {request.method} - URL: {request.url}")

    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Request-ID"] = request_id
        logger.info(f"Request ID: {request_id} - Status: {response.status_code} - Time: {process_time:.4f}s")
        return response
    except Exception as e:
        logger.error(f"Request ID: {request_id} - Error: {str(e)}")
        raise e