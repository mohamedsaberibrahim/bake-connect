from fastapi import APIRouter, Body, Depends
from app.api.users.schemas import CreateUserSchema, UserSchema
from app.api.users.dao import UserDAO
from app.api.auth.services import AuthHandler
from app.api.users.services import UserService

router = APIRouter()


@router.post('', response_model=UserSchema)
async def register_new_user(
    payload: CreateUserSchema = Body(),
    user_service: UserService = Depends(),
):
    """Processes request to register user account."""
    user = await user_service.create_user(payload)
    return user

auth_handler = AuthHandler()


@router.get('', response_model=UserSchema)
async def get_user_profile(
    user_service: UserService = Depends(),
    user_id: int = Depends(auth_handler.auth_wrapper),
):
    """Processes request to get user profile."""
    user = await user_service.get_user_profile(user_id=user_id)
    return user
