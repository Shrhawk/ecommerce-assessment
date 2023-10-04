from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class Category(BaseModel):
    __tablename__ = "category"

    name = Column(String, unique=True, index=True)

    product = relationship("Product", back_populates="category")
