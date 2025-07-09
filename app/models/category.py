from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.database.database import Base
from app.models.products import Product


class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True)
    products: Mapped[list["Product"]] = relationship(
        back_populates="category", lazy="selectin", cascade="all, delete-orphan"
    )


# lazy="selectin" делает ровно 2 запроса (вместо потенциально сотен при N+1).
# Первый запрос — получает категорию(и).
# Второй запрос — получает ВСЕ продукты этих категорий одним пакетом.
# Избегаете N+1 — не делаете отдельный запрос для каждой категории
