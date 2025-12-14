from sqlmodel import SQLModel, Field
from typing import Optional
from app.models.common import ERPBase

class Customer(ERPBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    name: str
    email: Optional[str] = None
    phone: Optional[str] = None

    address: Optional[str] = None
    gst_number: Optional[str] = None
