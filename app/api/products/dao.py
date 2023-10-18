from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select, update
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
        print(product)
        self.session.add(product_model(
            name=product.name,
            baker_id=bakery_id,
            baking_time=product.baking_time,
            price=product.price,
            image_url=product.image_url,
            location=product.location
            ))

    async def filter(
        self,
        limit: int = 10,
        offset: int = 0,
        name: str = None,
        baker_id: int = None,
        id: int = None,
        location: str = None
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
        if id:
            query = query.filter(product_model.id == id)
        if location:
            query = query.filter(product_model.location == location)
        query = query.limit(limit).offset(offset)

        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())

    async def delete_product_model(self, product_id: int, bakery_id: int) -> None:
        """
        Delete specific product model.

        :param product_id: id of product instance.
        :param bakery_id: id of baker instance.
        :return: None.
        """
        result = await self.session.execute(select(product_model).filter(product_model.id == product_id).filter(product_model.baker_id == bakery_id))
        product = result.scalars().first()
        await self.session.delete(product)
        # await self.session.commit()

    async def update_product_model(self, product_id: int, payload: ProductBaseSchema) -> None:
        """
        Update specific product model.

        :param product_id: id of product instance.
        :param payload: payload of product instance.
        :param bakery_id: id of baker instance.
        :return: None.
        """
        values = {}

        if payload.name:
            values['name'] = payload.name
        if payload.baking_time:
            values['baking_time'] = payload.baking_time
        if payload.price:
            values['price'] = payload.price
        if payload.image_url:
            values['image_url'] = payload.image_url
        
        stmt = (
            update(product_model)
            .where(product_model.id == product_id)
            .values(**values)
        )

        await self.session.execute(stmt)
