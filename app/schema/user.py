from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    user_id: int
    access_token: str


class UserCreateSchema(BaseModel):
    user_name: str
    user_password: str
