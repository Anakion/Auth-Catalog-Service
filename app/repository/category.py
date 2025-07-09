from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence, Optional
from sqlalchemy import select, delete, update
from app.database import Category


class CategoryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all_categories(self) -> Sequence[Category]:
        result = await self.session.scalars(select(Category).order_by(Category.id))
        return result.all()

    async def get_category_by_id(self, category_id) -> Optional[Category]:
        return await self.session.get(Category, category_id)

    async def create_category(self, category_name) -> Category:
        new_category = Category(name=category_name)
        self.session.add(new_category)
        await self.session.commit()
        await self.session.refresh(new_category)
        return new_category

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
