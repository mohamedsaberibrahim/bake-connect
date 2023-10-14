from fastapi import APIRouter
from http import HTTPStatus
from app import monitoring

api_router = APIRouter()

api_router.include_router(monitoring.router)
