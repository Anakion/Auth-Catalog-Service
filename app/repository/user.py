from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import UserProfile


@dataclass
class UserRepository:
    session: AsyncSession

    async def create_user(self, user_name: str, user_password: str, access_token: str) -> UserProfile:
        user = UserProfile(username=user_name, password=user_password, access_token=access_token)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_user_by_id(self, user_id: int) -> UserProfile | None:
        result = await self.session.get(UserProfile, user_id)
        return result
