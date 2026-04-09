from fastapi import APIRouter

from app.api.routers.category_routers import router as categories_router
from app.api.routers.task_routers import router as tasks_router

api_router = APIRouter()
api_router.include_router(tasks_router)
api_router.include_router(categories_router)
