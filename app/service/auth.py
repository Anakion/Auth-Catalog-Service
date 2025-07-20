from dataclasses import dataclass
import datetime as dt
from jose import jwt, JWTError
from datetime import timedelta
from exception import (
    UserNotFoundException,
    UserNotCorrectPasswordException,
    TokenExpiredException,
    TokenNotCorrectException,
)
from models import UserProfile
from repository import UserRepository
from schema import UserLoginSchema
from settings import settings


@dataclass
class AuthService:
    user_repository: UserRepository

    async def login(self, user_name: str, user_password: str) -> UserLoginSchema:
        user = await self.user_repository.get_user_by_name(user_name)
        await self._validate_auth_user(user, user_password)
        access_token = await self.generate_access_token(user_id=user.id)  # type: ignore
        return UserLoginSchema(
            user_id=user.id,  # type: ignore[arg-type]
            access_token=access_token,
        )

    @staticmethod
    async def _validate_auth_user(user: UserProfile, user_password: str):
        if not user:
            raise UserNotFoundException
        if user.password != user_password:
            raise UserNotCorrectPasswordException

    @staticmethod
    async def generate_access_token(user_id: int) -> str:
        expires_date_unix = (dt.datetime.utcnow() + timedelta(minutes=4)).timestamp()
        token = jwt.encode(
            {
                "user_id": user_id,
                "expire": expires_date_unix,
            },
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )
        return token

    @staticmethod
    async def get_user_id_from_access_token(access_token: str) -> int:
        try:
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        except JWTError:
            raise TokenNotCorrectException

        if payload["expire"] < dt.datetime.utcnow().timestamp():
            raise TokenExpiredException

        return payload["user_id"]
