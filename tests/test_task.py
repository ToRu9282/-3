from unittest.mock import Mock

from app.models.task import TaskORM
from app.schemas.task import TaskCreate, TaskRead
from app.services.task import TaskService


def test_list_tasks_returns_pydantic_models(
    service: TaskService,
    repository_mock: Mock,
) -> None:
    # Имитируем, что метод get_all репозитория вернет эти задачи
    repository_mock.get_all.return_value = [
        TaskORM(id="task-1", title="Изучить pytest", completed=False),
        TaskORM(id="task-2", title="Написать первый тест", completed=True),
    ]

    result = service.list_tasks()

    assert result == [
        TaskRead(id="task-1", title="Изучить pytest", completed=False),
        TaskRead(id="task-2", title="Написать первый тест", completed=True),
    ]


def test_create_task_returns_TaskRead(
    service: TaskService,
    repository_mock: Mock,
) -> None:
    payload = TaskCreate(title="Изучить pytest", completed=False)

    repository_mock.create.return_value = TaskORM(
        id="task-3", title="Изучить pytest", completed=False
    )

    result = service.create_task(payload=payload)

    assert result.id == "task-3"
    assert result.title == "Изучить pytest"
    assert not result.completed

    # Проверяем, что репозиторий был вызван с правильными аргументами
    repository_mock.create.assert_called_once()
