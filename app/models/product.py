from sqlmodel import SQLModel, Field
from typing import Optional
from app.models.common import ERPBase

class Product(ERPBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    sku: str = Field(index=True, unique=True)
    name: str
    description: Optional[str] = None

    price: float = 0.0
    cost: float = 0.0

    is_active: bool = Field(default=True)
