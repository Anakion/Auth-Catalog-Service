import logging
from typing import List, Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from app.dependecy import get_category_repo, get_category_service, get_request_user_id
from app.repository import CategoryRepository
from app.schema import (
    CategoryResponse,
    CreateCategoryRequest,
    UpdateCategoryRequest,
)
from app.service import CategoryService
from exception import CategoryNotFoundError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/category", tags=["Categories"])


@router.get("/", response_model=List[CategoryResponse])
async def get_all_categories(
    category_service: Annotated[CategoryService, Depends(get_category_service)],
    user_id: int = Depends(get_request_user_id),
):
    return await category_service.get_all_categories(user_id)


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category_by_id(
    category_id: int,
    category_service: Annotated[CategoryService, Depends(get_category_service)],
    user_id: int = Depends(get_request_user_id),
):
    try:
        return await category_service.get_category_by_id(category_id, user_id)
    except CategoryNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    body: CreateCategoryRequest,
    category_service: Annotated[CategoryService, Depends(get_category_service)],
    user_id: int = Depends(get_request_user_id),
):
    category = await category_service.create_category(body, user_id)
    return category


@router.put("/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
async def update_category(
    category_id: int,
    category: UpdateCategoryRequest,
    category_service: Annotated[CategoryService, Depends(get_category_service)],
    user_id: int = Depends(get_request_user_id),
):
    try:
        return await category_service.update_category(category_id, category, user_id)
    except CategoryNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    repo: Annotated[CategoryRepository, Depends(get_category_repo)],
):
    logger.debug(f"Deleting category: {category_id}")
    existing_category = await repo.delete_category(category_id)
    if not existing_category:
        logger.warning(f"Category {category_id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    logger.debug(f"Deleted category: {category_id}")


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_categories(
    repo: Annotated[CategoryRepository, Depends(get_category_repo)],
):
    logger.debug("Deleting all categories")
    await repo.delete_all_categories()
    logger.debug("Deleted all categories")
