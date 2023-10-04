from sqlalchemy import Column, String, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship

from common.enums import UnitQuantity
from models.base_model import BaseModel


class Product(BaseModel):
    __tablename__ = "product"

    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    currency = Column(String, default="USD", nullable=False)
    unit = Column(Enum(UnitQuantity), nullable=False)
    category_id = Column(String, ForeignKey("category.id"), nullable=True)

    category = relationship("Category", back_populates="product")
    inventory = relationship("Inventory", back_populates="product")
    sales = relationship("Sales", back_populates="product")
