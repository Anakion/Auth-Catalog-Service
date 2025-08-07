import logging
from dataclasses import dataclass
from app.repository import CategoryRepository, CategoryCacheRepository
from app.schema import CategoryResponse
from exception import CategoryNotFoundError
from schema import CreateCategoryRequest, UpdateCategoryRequest

logger = logging.getLogger(__name__)


@dataclass
class CategoryService:
    category_repository: CategoryRepository
    cache_repository: CategoryCacheRepository

    async def get_all_categories(self, user_id: int) -> list[CategoryResponse]:
        if categories := await self.cache_repository.get_category(user_id):
            logger.debug(f"Serving categories from CACHE for user {user_id}")
            return categories
        else:
            logger.debug(f"Fetching categories from DB for user {user_id}")
            categories = await self.category_repository.get_all_categories(user_id)
            logger.debug(f"Found {len(categories)} categories for user {user_id}")
            categories_schema = [CategoryResponse.model_validate(category) for category in categories]
            await self.cache_repository.set_category(user_id, categories_schema)
            return categories_schema

    async def create_category(self, body: CreateCategoryRequest, user_id: int) -> CategoryResponse:
        category_id = await self.category_repository.create_category(body, user_id)
        category = await self.category_repository.get_category_by_id(category_id, user_id)
        return CategoryResponse.model_validate(category)

    async def get_category_by_id(self, category_id: int, user_id: int) -> CategoryResponse:
        category = await self.category_repository.get_category_by_id(category_id, user_id)

        if not category:
            raise CategoryNotFoundError

        return CategoryResponse.model_validate(category)

    async def update_category(
            self, category_id: int, category: UpdateCategoryRequest, user_id: int
    ) -> CategoryResponse:
        category = await self.category_repository.update_category(category_id, category, user_id)
        if not category:
            raise CategoryNotFoundError

        return CategoryResponse.model_validate(category)

    async def delete_category(self, category_id: int, user_id: int) -> None:
        success = await self.category_repository.delete_category(category_id, user_id)
        if not success:
            raise CategoryNotFoundError

    async def delete_all_categories(self, user_id: int) -> None:
        await self.category_repository.delete_all_categories(user_id)
