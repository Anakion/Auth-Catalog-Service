from app.handlers.ping import router as ping_router
from app.handlers.tasks import router as tasks_router
from app.handlers.category import router as category_router

routers = [ping_router, tasks_router, category_router]
