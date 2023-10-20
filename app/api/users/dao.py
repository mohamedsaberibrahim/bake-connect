from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dependencies import get_db_session
from app.api.users.models import User as user_model


class UserDAO:
    """Class for accessing user table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_user_model(self, user: user_model) -> None:
        """
        Add single user to session.

        :param name: name of a user.
        """
        self.session.add(user)

    async def get_all_users(self, limit: int, offset: int) -> List[user_model]:
        """
        Get all user models with limit/offset pagination.

        :param limit: limit of users.
        :param offset: offset of users.
        :return: stream of users.
        """
        raw_users = await self.session.execute(
            select(user_model).limit(limit).offset(offset),
        )

        return list(raw_users.scalars().fetchall())

    async def filter(
        self,
        name: Optional[str] = None
    ) -> List[user_model]:
        """
        Get specific user model.

        :param name: name of user instance.
        :return: user models.
        """
        query = select(user_model)
        if name:
            query = query.where(user_model.name == name)
        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())

    async def get_user_by_email(
            self,
            email: str) -> user_model:
        """
        Get specific user model.

        :param email: email of user instance.
        :return: user models.
        """
        query = select(user_model).where(user_model.email == email)
        rows = await self.session.execute(query)
        return rows.scalars().first()

    async def get_user_by_id(
            self,
            user_id: int) -> user_model:
        """
        Get specific user model.

        :param user_id: id of user instance.
        :return: user models.
        """
        query = select(user_model).where(user_model.id == user_id)
        rows = await self.session.execute(query)
        return rows.scalars().first()
