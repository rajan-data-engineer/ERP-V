from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class SalesOrder(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    so_number: str = Field(index=True)
    customer_id: int = Field(foreign_key="customer.id")

    order_date: datetime = Field(default_factory=datetime.utcnow)
    expected_delivery: Optional[datetime] = None

    status: str = Field(default="draft")
    # draft, submitted, approved, shipped, cancelled


class SalesOrderLine(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    sales_order_id: int = Field(foreign_key="salesorder.id")
    product_id: int = Field(foreign_key="product.id")

    quantity: float
    unit_price: float
