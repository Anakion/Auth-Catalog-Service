import logging

from fastapi import FastAPI
from app.handlers import routers

app = FastAPI()

for router in routers:
    app.include_router(router)

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,  # Уровень логирования
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Запись в файл
        logging.StreamHandler(),  # Вывод в консоль
    ],
)

logger = logging.getLogger(__name__)
logger.info("Starting application...")


# Middleware для логирования запросов
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    try:
        response = await call_next(request)
        logger.info(f"Response status: {response.status_code}")
        return response
    except Exception as e:
        logger.exception(f"Exception occurred: {str(e)}")
        raise


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting uvicorn server...")
    uvicorn.run("main:app", reload=True)
