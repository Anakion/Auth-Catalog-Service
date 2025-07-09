from typing import Optional

import redis.asyncio as aioredis

from app.schema import CategoryResponse


class CategoryCacheRepository:
    def __init__(self, redis: aioredis.Redis) -> None:
        self.redis = redis

    async def get_category(self) -> Optional[list[CategoryResponse]]:
        category_json = await self.redis.lrange("category", 0, -1)
        if not category_json:
            return None
        return [
            CategoryResponse.model_validate_json(cat.decode("utf-8"))
            for cat in category_json
        ]

    async def set_category(self, categories: list[CategoryResponse]):
        async with self.redis.pipeline() as pipe:
            await pipe.delete("category")
            await pipe.rpush("category", *[cat.model_dump_json() for cat in categories])
            await pipe.expire("category", 60)
            await pipe.execute()
