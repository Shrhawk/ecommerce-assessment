from pydantic import BaseModel
from datetime import datetime


class InventoryRequest(BaseModel):
    product_id: str
    stock_quantity: int


class InventoryResponse(InventoryRequest):
    id: str


class InventoryChangeResponse(BaseModel):
    id: str
    inventory_id: str
    old_stock: int
    current_stock: int
    created_at: datetime
    updated_at: datetime
    is_active: bool
