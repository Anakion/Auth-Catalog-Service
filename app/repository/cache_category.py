from dataclasses import dataclass
from typing import Optional

import redis.asyncio as aioredis

from app.schema import CategoryResponse

@dataclass
class CategoryCacheRepository:
    redis: aioredis.Redis

    async def get_category(self, user_id: int) -> Optional[list[CategoryResponse]]:
        cache_key = f"categories:user:{user_id}"
        category_json = await self.redis.lrange(cache_key, 0, -1)
        if not category_json:
            return None
        return [CategoryResponse.model_validate_json(cat.decode("utf-8")) for cat in category_json]

    async def set_category(self, user_id: int, categories: list[CategoryResponse]):
        cache_key = f"categories:user:{user_id}"

        async with self.redis.pipeline() as pipe:
            await pipe.delete(cache_key)
            if categories:
                await pipe.rpush(cache_key, *[cat.model_dump_json() for cat in categories])
                await pipe.expire(cache_key, 3600)
            await pipe.execute()
