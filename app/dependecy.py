from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.repository import CategoryRepository, CategoryCacheRepository
from app.cache import get_redis_connection


async def get_category_repo(db: AsyncSession = Depends(get_db)) -> CategoryRepository:
    return CategoryRepository(db)


async def get_cache_category_repo() -> CategoryCacheRepository:
    aioredis = await get_redis_connection()
    return CategoryCacheRepository(aioredis)
