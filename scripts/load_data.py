from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from common.enums import UnitQuantity
from models import Category, Inventory, Product, Sales
from config.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# engine = create_engine(settings.DATABASE_URL)
# Session = sessionmaker(bind=engine)
session = Session()

categories = [
    Category(name="Test Category 1"),
    Category(name="Test Category 2"),
    Category(name="Test Category 3")
]
session.add_all(categories)
session.flush(categories)

products = [
    Product(
        name="Test Product 1",
        description="This is a test product",
        price=10.0, unit=UnitQuantity.UNIT,
        category_id=categories[0].id
    ),
    Product(
        name="Test Product 2",
        description="This is a test product",
        price=15.0,
        unit=UnitQuantity.UNIT,
        category_id=categories[0].id
    ),
    Product(
        name="Test Product 3",
        description="This is a test product",
        price=15.0,
        unit=UnitQuantity.UNIT,
        category_id=categories[0].id
    ),
]
session.add_all(products)
session.flush(products)

inventory = [
    Inventory(product_id=products[0].id, stock_quantity=100),
    Inventory(product_id=products[1].id, stock_quantity=50),
    Inventory(product_id=products[2].id, stock_quantity=50),
]
session.add_all(inventory)

sales = [
    Sales(product_id=products[0].id, quantity=5, amount=50.0),
    Sales(product_id=products[0].id, quantity=3, amount=45.0),
]
session.add_all(sales)

session.commit()
session.close()

print("Data has been loaded into the database")
