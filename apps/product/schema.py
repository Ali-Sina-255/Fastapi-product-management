from pydantic import BaseModel
from typing import Optional, Any, Generic, TypeVar

T = TypeVar("T")


class ResponseSchema(BaseModel):
    message: str
    data: Optional[Any] = None
    status_code: int
    success: bool = True


class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = 0.0


class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    created_at: str
