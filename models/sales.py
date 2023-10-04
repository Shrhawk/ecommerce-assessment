from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class Sales(BaseModel):
    __tablename__ = "sales"

    quantity = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    product_id = Column(String, ForeignKey("product.id"), nullable=False)

    product = relationship("Product", back_populates="sales")
