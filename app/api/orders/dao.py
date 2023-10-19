from typing import List

from fastapi import Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dependencies import get_db_session
from app.api.orders.models import Order as order_model


class OrderDAO:
    """Class for accessing order table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_order_model(self, order: order_model) -> None:
        """
        Add single order to session.

        :param name: name of a order.
        """
        stat = (
            insert(order_model)
            .values(
                payment_method=order.payment_method,
                bakery_id=order.bakery_id,
                product_id=order.product_id,
                user_id=order.user_id,
                state=order.state,
                created_at=order.created_at,
                updated_at=order.updated_at,
                tracking_number=order.tracking_number,
                start_baking_at=order.start_baking_at,
                finish_baking_at=order.finish_baking_at,
            )
        )
        await self.session.execute(stat)

    async def get_order_by_tracking_number(self, tracking_number: str) -> order_model:
        """
        Get single order by tracking_number.

        :param tracking_number: tracking_number of a order.
        """
        result = await self.session.execute(
            select(order_model).filter(order_model.tracking_number == tracking_number)
        )
        return result.scalars().first()

    async def update_order_model(self, order: order_model) -> None:
        """
        Update single order.

        :param order: order model.
        """
        self.session.add(order)

    async def filter(
            self, product_id: int = None, baker_id: int = None) -> List[order_model]:
        """
        Get specific order model.

        :param product_id: product_id of order instance.
        :return: order models.
        """
        query = select(order_model)
        if product_id:
            query = query.filter(order_model.product_id == product_id)
        if baker_id:
            query = query.filter(order_model.bakery_id == baker_id)

        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())
