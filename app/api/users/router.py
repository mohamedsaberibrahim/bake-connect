from fastapi import APIRouter, Body, Depends
from typing import List

from app.api.users.schemas import CreateUserSchema, UserSchema
from app.api.users.models import User as user_model
from app.api.users.dao import UserDAO
from app.api.auth.services import AuthHandler

router = APIRouter()


@router.post('', response_model=UserSchema)
async def register_new_user(
    payload: CreateUserSchema = Body(),
    user_dao: UserDAO = Depends(),
    auth_handler: AuthHandler = Depends()
):
    """Processes request to register user account."""
    payload.hashed_password = auth_handler.get_password_hash(payload.hashed_password)
    await user_dao.create_user_model(user=payload)
    user: user_model = await user_dao.get_user_by_email(email=payload.email)
    return user

auth_handler = AuthHandler()


@router.get('', response_model=List[UserSchema])
async def get_users(
    limit: int = 10,
    offset: int = 0,
    user_dao: UserDAO = Depends(),
    user_id=Depends(auth_handler.auth_wrapper)
):
    """Processes request to get all users."""
    print(user_id)
    users = await user_dao.get_all_users(limit=limit, offset=offset)
    return users
