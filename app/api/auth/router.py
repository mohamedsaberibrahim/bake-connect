from fastapi import APIRouter, Body, Depends, HTTPException
from typing import Dict, List

from http import HTTPStatus
from app.api.users.schemas import CreateUserSchema, UserSchema, UserBaseSchema, UserLoginSchema
from app.api.users.models import User as user_model
from app.api.users.dao import UserDAO
from app.api.auth.services import AuthHandler

router = APIRouter()

@router.post('/login', response_model=Dict)
async def login(
        payload: UserLoginSchema = Body(),
        user_dao: UserDAO = Depends(),
        auth_handler: AuthHandler = Depends()
    ):
    """Processes user's authentication and returns a token
    on successful authentication.

    request body:

    - username: Unique identifier for a user e.g email, 
                phone number, name

    - password:
    """
    try:
        user:user_model = await user_dao.get_user_by_email(email=payload.email)
    except:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid user credentials"
        )

    is_validated:bool = auth_handler.verify_password(payload.password, user.hashed_password)
    if not is_validated:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid user credentials"
        )

    return auth_handler.encode_token(user.id)

