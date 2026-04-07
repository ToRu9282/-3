from sqlalchemy.orm import Session

from app.repositorie.task import TaskRepository
from app.schemas.task import Task, TaskUpdate, TaskCreate

class TaskNotFound(Exception):
    '''Задача не найдена'''

class TaskService:
    """Ключевые операции с задачами, включая бизнес-логику, валидацию и прочее"""
    def __init__(self, db: Session):
        self.db = db
        self.repository = TaskRepository(db)
        
    def list_tasks(self) -> list[Task]:
        tasks = self.repository.get_all()
        return [Task.model_validate(task) for task in tasks]
    
    def create_task(self, task_create: TaskCreate) -> Task:
        task = self.repository.create(task_create.title)
        self.db.commit()
        return Task.model_validate(task)
    
    def update_task(self, task_id: str, title: TaskUpdate) -> Task:
        try:
            task = self.repository.get_by_id(task_id)
        except Exception:
            raise TaskNotFound(f"Задача с ID {task_id} не найдена")

        task.title = title.title if title.title is not None else task.title
        task.completed = title.completed if title.completed is not None else task.completed
            
        self.db.commit()
        return Task.model_validate(task)
    
    def delete_task(self, task_id: str) -> None:
        try:
            task = self.repository.get_by_id(task_id)
        except Exception:
            raise TaskNotFound(f"Задача с ID {task_id} не найдена")
        self.repository.delete(task)
        self.db.commit()