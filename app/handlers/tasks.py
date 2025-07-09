from fastapi import APIRouter

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/all")
async def get_tasks():
    return {"message": "ok"}


@router.post("/")
async def create_task():
    return {"text": "app is working"}
