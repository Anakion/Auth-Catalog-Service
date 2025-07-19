import logging
from dataclasses import dataclass
from fastapi import HTTPException
from app.repository import CategoryRepository, CategoryCacheRepository
from app.schema import CategoryResponse
from schema import CreateCategoryRequest

logger = logging.getLogger(__name__)


@dataclass
class CategoryService:
    category_repository: CategoryRepository
    cache_repository: CategoryCacheRepository

    async def get_all_categories(self) -> list[CategoryResponse]:
        if categories := await self.cache_repository.get_category():
            logger.debug("Serving categories from CACHE")
            return categories
        else:
            logger.debug("Fetching all categories")
            categories = await self.category_repository.get_all_categories()
            logger.debug(f"Found {len(categories)} categories")
            categories_schema = [
                CategoryResponse.model_validate(category) for category in categories
            ]
            await self.cache_repository.set_category(categories_schema)
            return categories_schema

    async def create_category(
        self, body: CreateCategoryRequest, user_id: int
    ) -> CategoryResponse:
        category_id = await self.category_repository.create_category(body, user_id)
        category = await self.category_repository.get_category_by_id(
            category_id, user_id
        )
        return CategoryResponse.model_validate(category)

    async def get_category_by_id(
        self, category_id: int, user_id: int
    ) -> CategoryResponse:
        logger.debug(f"Fetching category by id: {category_id} for user: {user_id}")
        category = await self.category_repository.get_category_by_id(
            category_id, user_id
        )
        logger.debug(f"Found category: {category}")

        if not category:
            raise HTTPException(
                status_code=404, detail="Category not found or doesn't belong to user"
            )

        return CategoryResponse.model_validate(category)
