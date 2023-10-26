from typing import List

from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.db import get_db
from models.inventory import Inventory, InventoryChange
from schemas.inventory import InventoryRequest, InventoryResponse, InventoryChangeResponse

inventory_router = APIRouter()


@inventory_router.post("", response_model=InventoryResponse, status_code=status.HTTP_201_CREATED)
async def add_inventory(request: InventoryRequest, db: Session = Depends(get_db)):
    """
    Registers a new product in the database
    :param request: InventoryRequest
    :param db: Session
    :return: InventoryResponse
    """
    inventory = Inventory(**request.model_dump())
    db.add(inventory)
    await db.commit()
    return inventory


@inventory_router.get("", response_model=List[InventoryResponse], status_code=status.HTTP_200_OK)
async def view_inventory(
        low_stock_threshold: int = Query(None, description="Low stock threshold quantity"),
        db: Session = Depends(get_db)
):
    """
    View current inventory status, including low stock alerts.
    :param low_stock_threshold: int
    :param db: Session
    :return: List[InventoryStatus]
    """
    query = select(Inventory).where(Inventory.is_active)
    if low_stock_threshold:
        query = query.where(Inventory.stock_quantity <= low_stock_threshold)
    result = await(db.execute(query))
    return result.scalars().all()


@inventory_router.put("", response_model=InventoryResponse, status_code=status.HTTP_200_OK)
async def update_inventory(
        product_id: str,
        quantity: int = 0,
        db: Session = Depends(get_db)
):
    """
    Update inventory levels for a product and track changes over time.
    :param product_id: str
    :param quantity: int (default 10)
    :param db: Session
    :return: InventoryChangeResponse
    """
    result = await db.execute(select(Inventory).where(Inventory.is_active, Inventory.product_id == product_id))
    result = result.scalars().one_or_none()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    result.stock_quantity += quantity
    inventory_change = InventoryChange(
        inventory_id=result.id,
        old_stock=result.stock_quantity - quantity,
        current_stock=result.stock_quantity
    )
    db.add(result)
    db.add(inventory_change)
    await db.commit()
    return result


@inventory_router.get("/change", response_model=List[InventoryChangeResponse], status_code=status.HTTP_200_OK)
async def get_inventory_changes(
        inventory_id: str,
        db: Session = Depends(get_db)
):
    """
    Fetch inventory levels for a product and track changes over time.
    :param inventory_id: str
    :param db: Session
    :return: List[InventoryChangeResponse]
    """
    query = select(InventoryChange).where(InventoryChange.inventory_id == inventory_id)
    result = await db.execute(query)
    return result.scalars().all()
