from dataclasses import dataclass

from exception import UserNotFoundException, UserNotCorrectPasswordException
from models import UserProfile
from repository import UserRepository
from schema import UserLoginSchema


@dataclass
class AuthService:
    user_repository: UserRepository

    async def login(self, user_name: str, user_password: str) -> UserLoginSchema:
        user = await self.user_repository.get_user_by_name(user_name)
        await self._validate_auth_user(user, user_password)

        return UserLoginSchema(
            user_id=user.id,  # type: ignore[arg-type]
            access_token=user.access_token,  # type: ignore[arg-type]
        )

    @staticmethod
    async def _validate_auth_user(user: UserProfile, user_password: str):
        if not user:
            raise UserNotFoundException
        if user.password != user_password:
            raise UserNotCorrectPasswordException
