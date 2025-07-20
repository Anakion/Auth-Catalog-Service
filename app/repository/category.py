from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence, Optional
from sqlalchemy import select, delete, update
from app.models import Category
from app.schema import CreateCategoryRequest


class CategoryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all_categories(self, user_id) -> Sequence[Category]:
        result = await self.session.scalars(select(Category).where(Category.user_id == user_id))
        return result.all()

    async def get_category_by_id(self, category_id, user_id) -> Optional[Category]:
        result = await self.session.execute(
            select(Category).where(Category.id == category_id, Category.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create_category(self, category_name: CreateCategoryRequest, user_id) -> int:
        new_category = Category(name=category_name.name, user_id=user_id)
        self.session.add(new_category)
        await self.session.commit()
        await self.session.refresh(new_category)
        return new_category.id

    async def update_category(self, category_id, category) -> Optional[Category]:
        stmt = update(Category).where(Category.id == category_id).values(name=category.name).returning(Category)
        result = await self.session.scalars(stmt)
        await self.session.commit()
        return result.first()

    async def delete_category(self, category_id) -> bool:
        category = await self.session.get(Category, category_id)
        if not category:
            return False

        await self.session.delete(category)
        await self.session.commit()
        return True

    async def delete_all_categories(self) -> None:
        await self.session.execute(delete(Category))
        await self.session.commit()
