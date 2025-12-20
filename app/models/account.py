from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Account(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    name: str
    code: str

    parent_id: Optional[int] = Field(default=None, foreign_key="account.id")

    # MANY → ONE (child → parent)
    parent: Optional["Account"] = Relationship(
        back_populates="children",
        sa_relationship_kwargs={"remote_side": "Account.id"},
    )

    # ONE → MANY (parent → children)
    children: List["Account"] = Relationship(
        back_populates="parent"
    )
