from app.handlers.category import router as category_router
from app.handlers.user import router as user_router
from app.handlers.auth import router as auth_router

routers = [category_router, user_router, auth_router]
