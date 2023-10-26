from typing import List

from fastapi import APIRouter, status, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.db import get_db
from models import Category
from schemas.category import CategoryRequest, CategoryResponse

category_router = APIRouter()


@category_router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(request: CategoryRequest, db: Session = Depends(get_db)):
    """
    Creates a new category in the database
    :param request: CategoryRequest
    :param db: Session
    :return: CategoryResponse
    """
    category = Category(name=request.name)
    db.add(category)
    await db.commit()
    return category


@category_router.get("", response_model=List[CategoryResponse], status_code=status.HTTP_200_OK)
async def get_categories(
        limit: int = Query(10, description="Items per page", le=50),
        offset: int = Query(0, description="Offset for pagination", ge=0),
        db: Session = Depends(get_db)
):
    """
    Fetches categories from database
    :param limit: int (default 10, max 50)
    :param offset: int (default 0)
    :param db: Session
    :return: List[CategoryResponse]
    """
    result = await db.execute(select(Category).where(Category.is_active).limit(limit).offset(offset))
    return result.scalars().all()
