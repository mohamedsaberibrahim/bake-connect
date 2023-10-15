from fastapi import APIRouter
from app.api import monitoring
from app.api import users
from app.api import auth

api_router = APIRouter()

api_router.include_router(monitoring.router)
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])