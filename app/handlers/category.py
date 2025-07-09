import logging
from typing import List, Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from app.dependecy import get_category_repo, get_cache_category_repo
from app.repository import CategoryRepository
from app.schema import (
    CategoryResponse,
    CreateCategoryRequest,
    UpdateCategoryRequest,
)
from app.repository import CategoryCacheRepository

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/category", tags=["Categories"])


@router.get("/", response_model=List[CategoryResponse])
async def get_all_categories(
    repo: Annotated[CategoryRepository, Depends(get_category_repo)],
    cache_repo: Annotated[CategoryCacheRepository, Depends(get_cache_category_repo)],
):
    if categories := await cache_repo.get_category():
        logger.debug("Serving categories from CACHE")
        return categories
    else:
        logger.debug("Fetching all categories")
        categories = await repo.get_all_categories()
        logger.debug(f"Found {len(categories)} categories")
        categories_schema = [
            CategoryResponse.model_validate(category) for category in categories
        ]
        await cache_repo.set_category(categories_schema)
        return categories_schema


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category_by_id(
    category_id: int,
    repo: Annotated[CategoryRepository, Depends(get_category_repo)],
):
    logger.debug(f"Fetching category by id: {category_id}")
    category = await repo.get_category_by_id(category_id)
    if not category:
        logger.warning(f"Category {category_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    logger.debug(f"Found category: {category}")
    return category


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_name: CreateCategoryRequest,
    repo: Annotated[CategoryRepository, Depends(get_category_repo)],
):
    logger.debug(f"Creating category: {category_name}")
    category = await repo.create_category(category_name.name)
    logger.debug(f"Created category: {category}")
    return category


@router.put(
    "/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK
)
async def update_category(
    category_id: int,
    category: UpdateCategoryRequest,
    repo: Annotated[CategoryRepository, Depends(get_category_repo)],
):
    logger.debug(f"Updating category: {category_id}")
    existing_category = await repo.get_category_by_id(category_id)
    if not existing_category:
        logger.warning(f"Category {category_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    updated_category = await repo.update_category(category_id, category)
    logger.debug(f"Updated category: {updated_category}")
    return updated_category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    repo: Annotated[CategoryRepository, Depends(get_category_repo)],
):
    logger.debug(f"Deleting category: {category_id}")
    existing_category = await repo.delete_category(category_id)
    if not existing_category:
        logger.warning(f"Category {category_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    logger.debug(f"Deleted category: {category_id}")


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_categories(
    repo: Annotated[CategoryRepository, Depends(get_category_repo)],
):
    logger.debug("Deleting all categories")
    await repo.delete_all_categories()
    logger.debug("Deleted all categories")
