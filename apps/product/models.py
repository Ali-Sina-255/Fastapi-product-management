from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Item(SQLModel, table=True):
    __tablename__ = "items"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False)
    description: Optional[str] = None
    price: float = Field(default=0.0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
