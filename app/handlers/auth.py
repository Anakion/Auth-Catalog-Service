from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.dependecy import get_auth_service
from app.schema import UserLoginSchema, UserCreateSchema
from app.service import AuthService
from app.exception import UserNotFoundException, UserNotCorrectPasswordException

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("", response_model=UserLoginSchema)
async def login(
    body: UserCreateSchema,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    try:
        return await auth_service.login(body.user_name, body.user_password)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except UserNotCorrectPasswordException as e:
        raise HTTPException(status_code=401, detail=e.detail)
