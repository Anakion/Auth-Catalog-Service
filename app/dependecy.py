from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.repository import CategoryRepository, CategoryCacheRepository
from app.cache import get_redis_connection
from app.service import CategoryService
from repository import UserRepository
from service import AuthService
from service.user import UserService


async def get_category_repo(db: AsyncSession = Depends(get_db)) -> CategoryRepository:
    return CategoryRepository(db)


async def get_cache_category_repo() -> CategoryCacheRepository:
    aioredis = await get_redis_connection()
    return CategoryCacheRepository(aioredis)


async def get_category_service(
    category_repository: CategoryRepository = Depends(get_category_repo),
    cache_repository: CategoryCacheRepository = Depends(get_cache_category_repo),
) -> CategoryService:
    return CategoryService(
        category_repository=category_repository,
        cache_repository=cache_repository,
    )


async def get_user_repository(
    session: AsyncSession = Depends(get_db),
) -> UserRepository:
    return UserRepository(session=session)


async def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(user_repository=user_repository)


async def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(user_repository=user_repository)
