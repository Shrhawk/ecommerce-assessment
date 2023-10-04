from typing import List

from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from models.inventory import Inventory, InventoryChange
from schemas.inventory import InventoryRequest, InventoryResponse, InventoryChangeResponse

inventory_router = APIRouter()


@inventory_router.post("", response_model=InventoryResponse, status_code=status.HTTP_201_CREATED)
async def add_inventory(request: InventoryRequest, db: Session = Depends(get_db)):
    """
    Registers a new inventory in the database
    :param request: InventoryRequest
    :param db: Session
    :return: InventoryResponse
    """
    inventory = Inventory(**request.model_dump())
    db.add(inventory)
    db.commit()
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
    inventory = db.query(Inventory)
    if low_stock_threshold:
        inventory = inventory.filter(Inventory.stock_quantity <= low_stock_threshold)
    return inventory.all()


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
    product_inventory = db.query(Inventory).filter(Inventory.product_id == product_id)
    if not product_inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    product_inventory = db.query(Inventory).filter(Inventory.product_id == product_id).first()
    product_inventory.stock_quantity += quantity
    InventoryChange(
        inventory_id=product_inventory.id,
        old_stock=product_inventory.stock_quantity,
        current_stock=product_inventory.stock_quantity + quantity
    )
    db.add(product_inventory)
    db.commit()
    return product_inventory


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
    return db.query(InventoryChange).filter(InventoryChange.inventory_id == inventory_id).all()
