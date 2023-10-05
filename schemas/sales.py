from datetime import datetime
from typing import List

from pydantic import BaseModel

from schemas.product import RegisterProductRequest


class ProductSchema(RegisterProductRequest):
    id: str


class SalesRequest(BaseModel):
    quantity: int
    amount: float
    product_id: str


class SalesResponse(BaseModel):
    id: str
    quantity: int
    amount: float
    product: ProductSchema
    created_at: datetime
    updated_at: datetime
    is_active: bool


class SalesRevenue(BaseModel):
    revenue: float


class RevenueComparison(BaseModel):
    category_id: str
    total_revenue: float


class SalesRevenueComparison(BaseModel):
    revenue_comparison: List[RevenueComparison]
