from uuid import uuid4
import uvicorn

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker


DATABASE_URL = "postgresql+psycopg://postgres:admin@127.0.0.1:5432/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal=sessionmaker(bind=engine)

#Классы для БД

class Base(DeclarativeBase):
    """Базовый класс для всех моделей таблиц БД"""
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))

class TaskORM(Base):
    """Модель для таблицы задач в Базе Данных"""
    __tablename__ = "tasks"
    
    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)
    
class CategoryORM(Base):
    """Модель для таблицы категорий в Базе Данных"""
    __tablename__ = 'category'
    
    name: Mapped[str]


async def lifespan(_: FastAPI): #Запускается атоматически
    '''Функция для создания таблиц'''
    Base.metadata.create_all(bind=engine) # Создает таблицы при запуске
    Base.metadata.create_all(bind=engine)# Создает таблицы при запуске
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://localhost:3000'
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

#Классы для данных

class Task(BaseModel):
    """Модель задачи"""
    id: str
    title: str
    completed: bool = False

class TaskCreate(BaseModel):
    title: str
    
class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None


class Category(BaseModel):
    """Модель категорий"""
    id: str
    name: str

class CategoryCreate(BaseModel):
    name: str

class CategoryUpdate(BaseModel):
    name: str


# Выпомогательные функции
def get_db(): 
    '''Создает и закрыевает Сессии'''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def task_orm_to_model(task_orm: TaskORM) -> Task:
    '''Переводит задачи из SQL в понятный для пайтона язык(кортежи)'''
    return Task(id=task_orm.id, title=task_orm.title, completed=task_orm.completed)

def category_orm_to_model(category_orm: CategoryORM) -> Category:
    '''Переводит категории из SQL в понятный для пайтона язык(кортежи)'''
    return Category(id=category_orm.id, name=category_orm.name)




# Задачи
@app.get("/tasks", response_model=list[Task], tags=['Задачи'])
def get_tasks(db: Session = Depends(get_db)) -> list[Task]:
    """Получить список задач"""
    tasks_from_db = db.scalars(select(TaskORM)).all()
    return [task_orm_to_model(task) for task in tasks_from_db]

@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED, tags=['Задачи'])
def create_task(payload: TaskCreate, db: Session = Depends(get_db)) -> Task:
    """Создать новую задачу"""
    task = TaskORM(title=payload.title, completed=False)
    db.add(task)
    db.commit()
    return task_orm_to_model(task)

@app.patch("/tasks/{task_id}", response_model=Task, tags=['Задачи'])
def update_task(task_id: str, payload: TaskUpdate, db: Session = Depends(get_db)) -> Task:
    '''Изменить задачу'''
    task_update = db.get(TaskORM, task_id)
    if task_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Задача не найдена')
    
    task_update.title = payload.title if payload.title is not None else task_update.title
    task_update.completed = payload.completed if payload.completed is not None else task_update.completed
        
    db.commit()
    return task_orm_to_model(task_update)
    
@app.delete('/tasks/{task_id}', status_code = status.HTTP_204_NO_CONTENT, tags=['Задачи'])
def delete_task(task_id: str, db: Session = Depends(get_db)) -> None:
    '''Удаление задачи'''
    task_delete = db.get(TaskORM, task_id)
    if task_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Задача не найдина')
    
    db.delete(task_delete)
    db.commit()
    


# Каталог

categorys: list[Category]=[]

@app.get('/categories', response_model=list[Category], tags=["Категории"])
def get_category(db: Session = Depends(get_db))  -> list[Category]:
    '''Получить список категорий'''
    categorys_from_bd = db.scalars(select(CategoryORM)).all()
    return [category_orm_to_model(category) for category in categorys_from_bd]

@app.post('/categories', response_model=Category, status_code=status.HTTP_201_CREATED, tags=['Категории'])
def post_category(new_category: CategoryCreate, db: Session = Depends(get_db)):
    """Создать категорию"""
    category = CategoryORM(name= new_category.name)
    db.add(category)
    db.commit()
    return category_orm_to_model(category)

@app.patch("/categories/{category_id}", response_model=Category, status_code=status.HTTP_200_OK, tags=["Категории"])
def patch_category(category_id: str, new_name: CategoryUpdate, db: Session = Depends(get_db)) -> Category:
    '''Изменить категорию'''
    category_new = db.get(CategoryORM, category_id)
    if category_new is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Категория не найдина')
    
    category_new.name=new_name.name
    db.commit()
    return category_orm_to_model(category_new)

@app.delete('/categories/{category_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Категории'])
def delete_category(category_id: str, db: Session = Depends(get_db)) -> None:
    '''Удаление категории'''
    category_delete=db.get(CategoryORM, category_id)
    if category_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Задача не найдина')
    
    db.delete(category_delete)
    db.commit()
    
if __name__ =='__main__':
    uvicorn.run("main:app", reload=True, port=8080)