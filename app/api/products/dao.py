from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dependencies import get_db_session
from app.api.products.models import Product as product_model
from app.api.products.schemas import ProductBaseSchema

class ProductDAO:
    """Class for accessing product table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_product_model(self, product: ProductBaseSchema, bakery_id: int) -> None:
        """
        Add single product to session.

        :param name: name of a product.
        """
        self.session.add(product_model(
            name=product.name,
            baker_id=bakery_id,
            baking_time=product.baking_time,
            price=product.price,
            image_url=product.image_url
            ))

    async def get_all_product(self, limit: int, offset: int) -> List[product_model]:
        """
        Get all product models with limit/offset pagination.

        :param limit: limit of product.
        :param offset: offset of product.
        :return: stream of product.
        """
        raw_product = await self.session.execute(
            select(product_model).limit(limit).offset(offset),
        )

        return list(raw_product.scalars().fetchall())

    async def filter(
        self,
        name: str = None,
        baker_id: int = None
    ) -> List[product_model]:
        """
        Get specific product model.

        :param name: name of product instance.
        :return: product models.
        """
        query = select(product_model)
        if name:
            query = query.filter(product_model.name == name)
        if baker_id:
            query = query.filter(product_model.baker_id == baker_id)
        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())
