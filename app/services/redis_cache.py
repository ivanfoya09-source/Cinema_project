import json

from redis.asyncio import Redis


class RedisCache:

    def __init__(self, redis: Redis):
        self.redis = redis

    async def get(self, key: str):

        data = await self.redis.get(key)

        if data:
            return json.loads(data)

        return None

    async def set(
        self,
        key: str,
        value,
        expire: int = 300,
    ):

        await self.redis.set(
            key,
            json.dumps(value),
            ex=expire,
        )

    async def delete(self, key: str):

        await self.redis.delete(key)