from fastapi import APIRouter
from apps.api.routes.product import create
api_router = APIRouter()
api_router.include_router(create.router)
