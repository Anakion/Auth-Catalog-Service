from fastapi import APIRouter

from app.settings import settings

router = APIRouter(prefix="/ping", tags=["ping"])


@router.get("/db")
async def ping_db():
    # print("Все переменные окружения:", dict(os.environ))  # Вывод в консоль сервера
    # return {"message": f"ok, {settings.GOOGLE_TOKEN_ID, dict(os.environ)}"}
    return {"lox": f"you {settings.GOOGLE_TOKEN_ID}"}


@router.get("/app")
async def ping_app():
    return {"text": "app is working"}
