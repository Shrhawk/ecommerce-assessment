from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class Inventory(BaseModel):
    __tablename__ = "inventory"

    product_id = Column(String, ForeignKey("product.id"), nullable=False)
    stock_quantity = Column(Integer, nullable=False)

    product = relationship("Product", back_populates="inventory")
    inventory_change = relationship("InventoryChange", back_populates="inventory")


class InventoryChange(BaseModel):
    __tablename__ = "inventory_change"

    inventory_id = Column(String, ForeignKey("inventory.id"), nullable=False)
    old_stock = Column(Integer, nullable=False)
    current_stock = Column(Integer, nullable=False)

    inventory = relationship("Inventory", back_populates="inventory_change")
