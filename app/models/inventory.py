from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class InventoryItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    product_id: int = Field(foreign_key="product.id")

    quantity_on_hand: float = 0.0
    quantity_committed: float = 0.0
    quantity_available: float = 0.0


class InventoryMovement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    product_id: int = Field(foreign_key="product.id")

    movement_type: str                 # purchase, sale, adjustment
    quantity: float

    reference: Optional[str] = None       
    timestamp: datetime = Field(default_factory=datetime.utcnow)
