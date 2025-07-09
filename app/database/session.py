from typing import AsyncGenerator
from app.database.database import AsyncSession, AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
