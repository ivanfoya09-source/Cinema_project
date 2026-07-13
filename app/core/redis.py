import redis

from app.core.config import settings


if settings.REDIS_URL:

    redis_client = redis.from_url(
        settings.REDIS_URL,
        decode_responses=True,
    )

else:

    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        decode_responses=True,
    )