# E-Commerce Admin API Documentation

## Table of Contents

- [Introduction](#introduction)
- [Setup Instructions](#setup-instructions)
- [Dependencies](#dependencies)
- [API Endpoints](#api-endpoints)
- [Additional Information](#additional-information)

## Introduction

Welcome to the E-Commerce Admin API documentation. This API powers a web admin dashboard for e-commerce managers, providing insights into sales, revenue, product management, and inventory control. It's implemented using Python and FastAPI.

## Setup Instructions

To set up and run the E-Commerce Admin API on your local machine, follow these steps:

1. **Clone the Repository**:

   ```bash
   git clone <repository-url>
   ```
2. **Create and Activate Virtual Environment**

To create virtual environment, use the following command.
```shell
python -m venv <env>
```
To activate virtual environment, use the following command.
```shell
source <env>/bin/activate
```
3. **Install Dependencies**:

Ensure you have Python 3.7 or higher installed. Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
   ```

4. **Database Configuration**:

Create a [.env](.env) file and set DATABASE_URL to connect with your database.
```
DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5432/db
```

5. **Database Migrations**:

- Initialize the Alembic environment:

```bash
alembic init alembic
```

- Modify the `alembic.ini` file to specify the correct database URL.

- Generate an initial migration:

```bash
alembic revision --autogenerate -m "initial"
```
- Apply the migration to create the database tables:

```bash
alembic upgrade head
```
Additionally, if you want to load data to the database, run the following command
```bash
python scripts/load_data.py 
 ```
6. **Run the Application**:

Start the FastAPI application:

   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```

Customize the host and port to your preferences.

7.**Access the API**:

   The API will be available at `http://localhost:8000`. You can now make requests to the provided endpoints.

## Dependencies

The E-commerce Admin API relies on several libraries and tools, including:

- Python 3.7+
- FastAPI: A fast web framework for building APIs with Python.
- SQLAlchemy: A SQL toolkit and Object-Relational Mapping (ORM) library.
- PostgreSQL: A powerful open-source relational database system for data storage.
- Alembic: A database migration tool for managing schema changes.
- Pydantic: A powerful tool for schema validation

You must install these dependencies as described in the "Setup Instructions" section.

## API Endpoints

### 1. Product Management

#### Create a New Category

- **Endpoint**: `/api/v1/category/`
- **Method**: POST
- **Description**: Create a new category in the database.

#### Retrieve Categories

- **Endpoint**: `/api/v1/category/`
- **Method**: GET
- **Description**: Fetch categories with pagination support.

### 2. Inventory Management

#### Add Inventory

- **Endpoint**: `/api/v1/inventory/`
- **Method**: POST
- **Description**: Register a new product's inventory in the database.

#### View Inventory

- **Endpoint**: `/api/v1/inventory/`
- **Method**: GET
- **Description**: View current inventory status, including low stock alerts.

#### Update Inventory

- **Endpoint**: `/api/v1/inventory/`
- **Method**: PUT
- **Description**: Update inventory levels for a product and track changes over time.

#### Get Inventory Changes

- **Endpoint**: `/api/v1/inventory/change`
- **Method**: GET
- **Description**: Fetch inventory levels for a product and track changes over time.

### 3. Product Management

#### Register a New Product

- **Endpoint**: `/api/v1/products/`
- **Method**: POST
- **Description**: Register a new product in the database.

#### Get Products

- **Endpoint**: `/api/v1/products/`
- **Method**: GET
- **Description**: Fetch all products with optional category filtering.

### 4. Sales Management

#### Create Sales

- **Endpoint**: `/api/v1/sales/`
- **Method**: POST
- **Description**: Create new sales orders in the database.

#### Get Sales

- **Endpoint**: `/api/v1/sales/`
- **Method**: GET
- **Description**: Retrieve sales data based on a time interval, product, or category filter.

#### Get All Sales

- **Endpoint**: `/api/v1/sales/all`
- **Method**: GET
- **Description**: Retrieve paginated sales data.

#### Calculate Revenue

- **Endpoint**: `/api/v1/sales/revenue`
- **Method**: GET
- **Description**: Calculate revenue based on daily, weekly, monthly, or annual periods.

#### Compare Revenue

- **Endpoint**: `/api/v1/sales/compare-revenue`
- **Method**: GET
- **Description**: Compare revenue across different categories within a specified date range.

## Additional Information

- The API allows you to create and manage categories, products, and sales, while also providing inventory tracking.
- All data is stored in a PostgreSQL database with well-defined schemas.
- You can use the endpoints to retrieve, filter, analyze, and manage various aspects of your e-commerce business.
- Detailed API documentation is available for each endpoint, along with information about request parameters and response structures.
