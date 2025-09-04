import redis.asyncio as aioredis


async def get_redis_connection() -> aioredis.Redis:
    redis = await aioredis.from_url("redis://localhost/0")
    return redis



