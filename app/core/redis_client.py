import os

import redis.asyncio as redis

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")

pool = redis.ConnectionPool.from_url(REDIS_URL, decode_responses=True)

def get_redis_client() -> redis.Redis:
    return redis.Redis(connection_pool=pool)
