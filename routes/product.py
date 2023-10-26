from typing import List

from fastapi import APIRouter, status, Depends, Query, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.db import get_db
from models import Product, Category
from schemas.product import RegisterProductRequest, RegisterProductResponse

product_router = APIRouter()


@product_router.post("", response_model=RegisterProductResponse, status_code=status.HTTP_201_CREATED)
async def register_product(request: RegisterProductRequest, db: Session = Depends(get_db)):
    """
    Registers a new product in the database
    :param request: RegisterProductRequest
    :param db: Session
    :return: RegisterProductResponse
    """
    result = await db.execute(select(Category).where(Category.is_active, Category.id == request.category_id))
    if request.category_id and not result.scalars().all():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    product = Product(**request.model_dump())
    db.add(product)
    await db.commit()
    return product


@product_router.get("", response_model=List[RegisterProductResponse], status_code=status.HTTP_200_OK)
async def get_products(
        category_id: str = Query(None, description="ID to filter products by"),
        db: Session = Depends(get_db)
):
    """
    Fetches all products from the database filtered by category ID
    :param category_id: Optional[str]
    :param db: Session
    :return: List[RegisterProductResponse]
    """
    query = select(Product).where(Product.is_active)
    if category_id:
        query = query.where(Product.category_id == category_id)
    result = await db.execute(query)
    return result.scalars().all()
