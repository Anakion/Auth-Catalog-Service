from dataclasses import dataclass

from app.schema import UserLoginSchema
from app.repository import UserRepository
from app.service.auth import AuthService


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService

    async def create_user(self, user_name: str, user_password: str) -> UserLoginSchema:
        user = await self.user_repository.create_user(user_name, user_password)
        access_token = await self.auth_service.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)
