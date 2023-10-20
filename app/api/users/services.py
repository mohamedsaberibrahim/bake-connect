from fastapi import Depends, HTTPException
from app.api.users.models import User as user_model
from app.api.users.dao import UserDAO
from app.api.auth.services import AuthHandler


class UserService:
    """User service class"""
    def __init__(self, auth_handler: AuthHandler = Depends(),
                user_dao: UserDAO = Depends()):
        self.auth_handler = auth_handler
        self.user_dao = user_dao


    async def create_user(self, payload):
        """Creates a new user"""
        user: user_model = await self.user_dao.get_user_by_email(email=payload.email)
        if user:
            raise HTTPException(status_code=400, detail="Email already registered")
        payload.hashed_password = self.auth_handler.get_password_hash(payload.hashed_password)
        await self.user_dao.create_user_model(user=payload)
        user: user_model = await self.user_dao.get_user_by_email(email=payload.email)
        return user


    async def get_user_profile(self, user_id: int):
        """Gets user profile"""
        user: user_model = await self.user_dao.get_user_by_id(user_id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
