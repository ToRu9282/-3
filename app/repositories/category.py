from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.category import CategoryORM


class CategoryRepository:
    """Репозиторий для работы с категориями в Базе Данных"""
    def __init__(self, db: Session):
        self.db = db
        
    def get_all(self) -> list[CategoryORM]:
        '''Получить все категории из БД'''
        return self.db.scalars(select(CategoryORM)).all()
    
    def get_by_id(self, category_id: str) -> CategoryORM | None:
        '''Получить категорию по ID из БД'''
        return self.db.get(CategoryORM, category_id)
    
    def create(self, name: str) -> CategoryORM:
        '''Создать новую категорию в БД'''
        category = CategoryORM(name=name)
        self.db.add(category)
        return category
    
    def delete(self, category: CategoryORM) -> None:
        '''Удалить категорию из БД'''
        self.db.delete(category)