import logging
from dataclasses import dataclass

from app.repository import CategoryRepository, CategoryCacheRepository
from app.schema import CategoryResponse

logger = logging.getLogger(__name__)


@dataclass
class CategoryService:
    category_repository: CategoryRepository
    cache_repository: CategoryCacheRepository

    async def get_all_categories(self):
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
