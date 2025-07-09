import redis.asyncio as aioredis


async def get_redis_connection() -> aioredis.Redis:
    redis = await aioredis.from_url("redis://localhost/0")
    return redis


# async def set_category():
#     redis = await get_redis_connection()
#     await redis.set("category", "test", ex=60)
#
#
# if __name__ == "__main__":
#     import asyncio
#
#     asyncio.run(set_category())
