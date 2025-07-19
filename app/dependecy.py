from fastapi import Depends, security, Security, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.repository import CategoryRepository, CategoryCacheRepository
from app.cache import get_redis_connection
from app.service import CategoryService
from exception import TokenExpiredException, TokenNotCorrectException
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


async def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(user_repository=user_repository)


async def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service),
) -> UserService:
    return UserService(user_repository=user_repository, auth_service=auth_service)


reusable_oauth2 = security.HTTPBearer()


async def get_request_user_id(
    auth_service: AuthService = Depends(get_auth_service),
    token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2),
) -> int:
    try:
        user_id = await auth_service.get_user_id_from_access_token(token.credentials)
    except TokenExpiredException as e:
        raise HTTPException(status_code=401, detail=e.detail)
    except TokenNotCorrectException as e:
        raise HTTPException(status_code=401, detail=e.detail)
    return user_id
