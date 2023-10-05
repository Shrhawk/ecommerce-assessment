from datetime import datetime, time, timedelta
from typing import List

from fastapi import APIRouter, Depends, status, Query, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from common.enums import Period
from common.helpers import parse_date
from database.db import get_db
from models import Category, Product, Sales, Inventory, InventoryChange
from schemas.sales import SalesRequest, SalesResponse, SalesRevenue, SalesRevenueComparison

sales_router = APIRouter()


@sales_router.post("", response_model=List[SalesResponse], status_code=status.HTTP_201_CREATED)
async def create_sale(request: List[SalesRequest], db: Session = Depends(get_db)):
    """
    Creates a new sale in the database
    :param request: List[SalesRequest]
    :param db: Session
    :return: List[SalesResponse]
    """
    for order_request in request:
        inventory = db.query(Inventory).filter(Inventory.product_id == order_request.product_id).all()[0]
        if not inventory or order_request.quantity > inventory.stock_quantity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Insufficient inventory found for product: {order_request.product_id}"
            )
    sales = []
    for order_request in request:
        inventory = db.query(Inventory).filter(Inventory.product_id == order_request.product_id).all()[0]
        inventory.stock_quantity -= order_request.quantity
        db.add(inventory)
        inventory_change = InventoryChange(
            inventory_id=inventory.id,
            old_stock=inventory.stock_quantity + order_request.quantity,
            current_stock=inventory.stock_quantity
        )
        db.add(inventory_change)
        sales.append(Sales(**order_request.model_dump()))
    db.add_all(sales)
    db.commit()
    return sales


@sales_router.get("", response_model=List[SalesResponse], status_code=status.HTTP_200_OK)
async def get_sales(
        start_date: str = Query(..., description="Start date for sales data (format: YYYY-MM-DD)"),
        end_date: str = Query(..., description="End date for sales data (format: YYYY-MM-DD)"),
        product_id: str = Query(None, description="Product ID to filter sales data"),
        category_id: str = Query(None, description="Category ID to filter sales data"),
        db: Session = Depends(get_db)
):
    """
    Returns sales based on time interval, product_id, or category_id
    :param start_date: str
    :param end_date: str
    :param product_id: str
    :param category_id: str
    :param db: Session
    :return: List[SalesResponse]
    """
    start_date = parse_date(start_date)
    end_date = parse_date(end_date)
    end_date = datetime.combine(end_date.date(), time(23, 59, 59))
    query = db.query(Sales).filter(
        Sales.created_at >= start_date,
        Sales.created_at <= end_date,
        Sales.is_active
    )
    if product_id:
        query = query.filter(Sales.product_id == product_id)
    if category_id:
        query = query.filter(Product.category_id == category_id)
    return query.all()


@sales_router.get("/all", response_model=List[SalesResponse], status_code=status.HTTP_200_OK)
async def get_all_sales(
        limit: int = Query(10, description="Items per page", le=50),
        offset: int = Query(0, description="Offset for pagination", ge=0),
        db: Session = Depends(get_db)
):
    """
    Returns paginated sales data
    :param limit: int (default 10, max 50)
    :param offset: int (default 0)
    :param db: Session
    :return: List[SalesResponse]
    """
    return db.query(Sales).limit(limit).offset(offset).all()


@sales_router.get("/revenue", response_model=SalesRevenue, status_code=status.HTTP_200_OK)
async def calculate_revenue(
        period: Period = Query(..., description="Time period for revenue analysis"),
        date: str = Query(None, description="Date for daily revenue analysis (format: YYYY-MM-DD)"),
        week_start: str = Query(None, description="Start date of the week (format: YYYY-MM-DD)"),
        month: str = Query(None, description="Month for monthly revenue analysis (format: YYYY-MM)"),
        year: int = Query(None, description="Year for annual revenue analysis"),
        db: Session = Depends(get_db)
):
    """
    Returns revenue in a particular time span based on date, week, month, and year
    :param period: Period
    :param date: str
    :param week_start: str
    :param month: str
    :param year: int
    :param db: Session
    :return: SalesRevenue
    """
    if period == Period.DAILY:
        if not date:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Date not found"
            )
        start_date = parse_date(date)
        end_date = start_date + timedelta(days=1)
    elif period == Period.WEEKLY:
        if not week_start:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Week not found"
            )
        start_date = parse_date(week_start)
        end_date = start_date + timedelta(weeks=1)
    elif period == Period.MONTHLY:
        if not month:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Month not found"
            )
        start_date = parse_date(month + "-01")
        if start_date.month == 12:
            end_date = datetime(start_date.year + 1, 1, 1)
        else:
            end_date = datetime(start_date.year, start_date.month + 1, 1)
    elif period == Period.ANNUAL:
        if not week_start:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Year not found"
            )
        start_date = datetime(year, 1, 1)
        end_date = datetime(year + 1, 1, 1)
    else:
        return {"revenue": 0}
    query = db.query(Sales).filter(
        Sales.created_at >= start_date,
        Sales.created_at < end_date,
        Sales.is_active
    )
    total_revenue = sum(sale.amount for sale in query.all())
    return {"revenue": total_revenue}


@sales_router.get("/compare-revenue", response_model=SalesRevenueComparison, status_code=status.HTTP_200_OK)
async def compare_revenue(
        start_date: str = Query(..., description="Start date for revenue comparison (format: YYYY-MM-DD)"),
        end_date: str = Query(..., description="End date for revenue comparison (format: YYYY-MM-DD)"),
        db: Session = Depends(get_db)
):
    """
    Compares revenue of categories in a particular time span
    :param start_date: str
    :param end_date: str
    :param db: Session
    :return: SalesRevenueComparison
    """
    start_date = parse_date(start_date)
    end_date = parse_date(end_date)
    end_date = datetime.combine(end_date.date(), time(23, 59, 59))
    sales_data = db.query(Product.category_id, func.sum(Sales.amount)). \
        join(Product, Sales.product_id == Product.id). \
        join(Category, Product.category_id == Category.id). \
        filter(Sales.created_at >= start_date, Sales.created_at <= end_date). \
        group_by(Product.category_id, Category.id).all()

    result = [
        {
            "category_id": category_id,
            "total_revenue": total_revenue
        }
        for category_id, total_revenue in sales_data
    ]

    return {"revenue_comparison": result}
