from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class UserProfile(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
