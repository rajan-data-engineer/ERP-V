from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class Account(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    code: str = Field(index=True, unique=True)
    name: str
    type: str  # asset, liability, equity, income, expense
    is_active: bool = Field(default=True)

    parent_id: Optional[int] = Field(default=None, foreign_key="account.id")

    # Relationships
    children: List["Account"] = Relationship(back_populates="parent")
    parent: Optional["Account"] = Relationship(back_populates="children")
