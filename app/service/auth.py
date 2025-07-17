from dataclasses import dataclass

from schema import UserLoginSchema


@dataclass
class AuthService:
    async def login(self, user_name: str, user_password: str) -> UserLoginSchema: ...
