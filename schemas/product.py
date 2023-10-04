from pydantic import BaseModel
from typing import Optional
from common.enums import UnitQuantity
from datetime import datetime


class RegisterProductRequest(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    unit: UnitQuantity = UnitQuantity.UNIT
    category_id: Optional[str] = None


class RegisterProductResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    price: float
    unit: UnitQuantity
    category_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    is_active: bool
