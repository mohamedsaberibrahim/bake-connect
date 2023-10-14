from fastapi import APIRouter, Body, Depends, HTTPException
from typing import Dict

from http import HTTPStatus
from app.api.users.schemas import CreateUserSchema, UserSchema, UserBaseSchema, UserLoginSchema
from app.api.users.models import User as user_model
from app.api.users.dao import UserDAO

router = APIRouter()

@router.post('/signup', response_model=UserBaseSchema)
async def signup(
    payload: CreateUserSchema = Body(), 
    user_dao: UserDAO = Depends()
):
    """Processes request to register user account."""
    print("payload: ", payload)
    payload.hashed_password = user_model.hash_password(payload.hashed_password)
    await user_dao.create_user_model(user=payload)
    user:user_model = await user_dao.get_user_by_email(email=payload.email)
    return user

@router.post('/login', response_model=Dict)
async def login(
        payload: UserLoginSchema = Body(),
        user_dao: UserDAO = Depends(),
    ):
    """Processes user's authentication and returns a token
    on successful authentication.

    request body:

    - username: Unique identifier for a user e.g email, 
                phone number, name

    - password:
    """
    try:
        print("email:", payload.email)
        user:user_model = await user_dao.get_user_by_email(email=payload.email)
        print("user:", user)
    except:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid user credentials"
        )

    is_validated:bool = user.validate_password(payload.password)
    if not is_validated:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid user credentials"
        )

    return user.generate_token()