from fastapi import APIRouter, status, HTTPException, Depends
from sqlmodel import Session
from apps.product.models import Item as DBItem  # Database model
from apps.product.schema import ResponseSchema, ItemCreate
from apps.core.db import get_session
from typing import Union

router = APIRouter(prefix="/items", tags=["Items"])


@router.post("/", response_model=ResponseSchema, status_code=status.HTTP_201_CREATED)
def create_items(
    item: ItemCreate,
    session: Session = Depends(get_session),
):
    # Validation
    if not item.name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Item name is required"
        )

    # Create database item
    db_item = DBItem(name=item.name, description=item.description, price=item.price)

    # Save to database
    session.add(db_item)
    session.commit()
    session.refresh(db_item)

    return ResponseSchema(
        message="Item created successfully",
        data={
            "id": db_item.id,
            "name": db_item.name,
            "description": db_item.description,
            "price": db_item.price,
            "created_at": db_item.created_at.isoformat(),
        },
        status_code=201,
        success=True,
    )


@router.get("/", response_model=list[ResponseSchema])
def get_items(session: Session = Depends(get_session), skip: int = 0, limit: int = 100):
    items = session.query(DBItem).offset(skip).limit(limit).all()
    return [
        ResponseSchema(
            message="Item retrieved",
            data={
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "price": item.price,
            },
            status_code=200,
            success=True,
        )
        for item in items
    ]
