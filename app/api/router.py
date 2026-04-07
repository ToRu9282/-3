from fastapi import APIRouter

from app.api.routers.task import router as tasks_router
from app.api.routers.category import router as categories_router

api_router = APIRouter()
api_router.include_router(router=tasks_router)
api_router.include_router(router=categories_router)