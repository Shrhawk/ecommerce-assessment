from datetime import datetime

from pydantic import BaseModel

from schemas.product import RegisterProductRequest


class ProductSchema(RegisterProductRequest):
    id: str


class SalesRequest(BaseModel):
    quantity: int
    amount: int
    product_id: str


class SalesResponse(BaseModel):
    id: str
    quantity: int
    amount: int
    product: ProductSchema
    created_at: datetime
    updated_at: datetime
    is_active: bool


class SalesRevenue(BaseModel):
    revenue: float

