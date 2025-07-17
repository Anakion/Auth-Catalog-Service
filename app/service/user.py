import secrets
from dataclasses import dataclass

from app.schema import UserLoginSchema
from app.repository import UserRepository


@dataclass
class UserService:
    user_repository: UserRepository

    async def create_user(self, user_name: str, user_password: str) -> UserLoginSchema:
        access_token = await self._generate_access_token()
        user = await self.user_repository.create_user(user_name, user_password, access_token)
        return UserLoginSchema(user_id=user.id, access_token=user.access_token)

    @staticmethod
    async def _generate_access_token() -> str:
        return secrets.token_urlsafe(32)
