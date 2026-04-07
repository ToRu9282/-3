from sqlalchemy.orm import Session

from app.repositorie.category import CategoryRepository
from app.schemas.category import Category, CategoryCreate, CategoryUpdate

class TaskNotFound(Exception):
    '''Задача не найдена'''

class CategoryService:
    """Сервис для работы с категориями"""
    def __init__(self, db: Session):
        self.db = db
        self.repository = CategoryRepository(db)

    def list_categories(self) -> list[Category]:
        """Получить все категории"""
        categories = self.repository.get_all()
        return [Category.model_validate(category) for category in categories]
    
    def create_category(self, category_create: CategoryCreate) -> Category:
        """Создать новую категорию"""
        category = self.repository.create(category_create.name)
        self.db.commit()
        return Category.model_validate(category)
    
    def update_category(self, category_id: str, category_update: CategoryUpdate) -> Category:
        """Изменить категорию"""
        category = self.repository.get_by_id(category_id)
        try:
            category = self.repository.get_by_id(category_id)
        except Exception:
            raise TaskNotFound(f"Категория с ID {category_id} не найдена")  

        category.name = category_update.name if category_update.name is not None else category.name
            
        self.db.commit()
        return Category.model_validate(category)
    
    def delete_category(self, category_id: str) -> None:
        """Удалить категорию"""
        try:
            category = self.repository.get_by_id(category_id)
        except Exception:
            raise TaskNotFound(f"Категория с ID {category_id} не найдена")
        self.repository.delete(category)
        self.db.commit()