

from sqlalchemy.orm import Mapped, mapped_column

class TaskORM(Base):
```
    """Модель для таблицы задач в Базе Данных"""
    __tablename__ = "tasks"
    
    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)