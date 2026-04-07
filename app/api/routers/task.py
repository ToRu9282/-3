from fastapi import APIRouter, HTTPException
from fastapi import status

from app.api.dependencies import get_task_service
from app.schemas.task import Task, TaskCreate, TaskUpdate
from app.services.task import TaskNotFound



router = APIRouter(prefix='/tasks')


@router.get(response_model=list[Task], tags=['Задачи'])
def get_tasks() -> list[Task]:
    """Получить список задач"""
    task_service = get_task_service()
    return task_service.list_tasks()


@router.post(response_model=Task, status_code=status.HTTP_201_CREATED, tags=['Задачи'])
def create_task(payload: TaskCreate) -> Task:
    """Создать новую задачу"""
    task_service = get_task_service()
    return task_service.create_task(payload)


@router.patch("/{task_id}", response_model=Task, tags=['Задачи'])
def update_task(task_id: str, payload: TaskUpdate) -> Task:
    '''Изменить задачу'''
    task_service = get_task_service()
    try:
        return task_service.update_task(task_id, payload)
    except TaskNotFound as e:   
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete('/{task_id}', status_code = status.HTTP_204_NO_CONTENT, tags=['Задачи'])
def delete_task(task_id: str) -> None:
    task_service = get_task_service()
    try:
        return task_service.delete_task(task_id)
    except TaskNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
