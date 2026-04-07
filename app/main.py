from fastapi.concurrency import asynccontextmanager
import uvicorn

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import engine
from app.models.base import Base
from app.core.config import get_settings

from app.api.routers.task import router as tasks_router
from app.api.routers.category import router as categories_router



#Классы для БД
@asynccontextmanager
async def lifespan(_: FastAPI): #Запускается атоматически
    '''Функция для создания таблиц'''
    from app.models.task import TaskORM
    Base.metadata.create_all(bind=engine)
    from app.models.category import CategoryORM
    Base.metadata.create_all(bind=engine)
    yield

settings = get_settings()
app = FastAPI(lifespan=lifespan)
app.include_router(router=tasks_router)
app.include_router(router=categories_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


    
if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True, port=8080)