from redis.asyncio import from_url
from redis.asyncio.client import Redis

from .config import settings


async def get_redis() -> Redis:
    return from_url(url=str(settings.redis))
