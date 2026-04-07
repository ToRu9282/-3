from operator import ge

from fastapi import APIRouter, Depends, HTTPException
from fastapi import status

from app.db.session import get_db
from app.schemas.category import Category, CategoryCreate, CategoryUpdate
from app.api import get_category_service
from app.services.category import TaskNotFound

router = APIRouter(prefix='/categories')

@router.get('', response_model=list[Category])
def get_category()  -> list[Category]:
    '''Получить список категорий'''
    category_service = get_category_service()
    return category_service.list_categories()

@router.post('', response_model=Category, status_code=status.HTTP_201_CREATED)
def post_category(new_category: CategoryCreate):
    """Создать категорию"""
    category_service = get_category_service()
    return category_service.create_category(new_category)
    
@router.patch("/{category_id}", response_model=Category, status_code=status.HTTP_200_OK)
def patch_category(category_id: str, new_name: CategoryUpdate) -> Category:
    '''Изменить категорию'''
    category_service = get_category_service()
    try:
        return category_service.update_category(category_id, new_name)
    except TaskNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete('/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str) -> None:
    '''Удаление категории'''
    category_service = get_category_service()
    try:
        return category_service.delete_category(category_id)
    except TaskNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))