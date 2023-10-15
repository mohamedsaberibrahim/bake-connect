from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dependencies import get_db_session
from app.api.bakeries.models import Bakery as bakery_model
from app.api.bakeries.schemas import BakeryBaseSchema

class BakeryDAO:
    """Class for accessing bakery table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_bakery_model(self, bakery: BakeryBaseSchema, owner_id: int) -> None:
        """
        Add single bakery to session.

        :param name: name of a bakery.
        """
        self.session.add(bakery_model(
            brand_name=bakery.brand_name,
            phone=bakery.phone,
            address=bakery.address,
            description=bakery.description,
            logo_url=bakery.logo_url,
            owner_id=owner_id
            ))

    async def get_all_bakery(self, limit: int, offset: int) -> List[bakery_model]:
        """
        Get all bakery models with limit/offset pagination.

        :param limit: limit of bakery.
        :param offset: offset of bakery.
        :return: stream of bakery.
        """
        raw_bakery = await self.session.execute(
            select(bakery_model).limit(limit).offset(offset),
        )

        return list(raw_bakery.scalars().fetchall())

    async def filter(
        self,
        name: Optional[str] = None
    ) -> List[bakery_model]:
        """
        Get specific bakery model.

        :param name: name of bakery instance.
        :return: bakery models.
        """
        query = select(bakery_model)
        if name:
            query = query.where(bakery_model.name == name)
        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())

    async def get_bakery_by_owner_id(
            self,
            owner_id: int
        ) -> bakery_model:
        """
        Get specific bakery model.

        :param owner_id: owner_id of bakery instance.
        :return: bakery models.
        """
        query = select(bakery_model).where(bakery_model.owner_id == owner_id)
        rows = await self.session.execute(query)
        return rows.scalars().first()
    