from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dependencies import get_db_session
from app.api.orders.models import Order as order_model
from app.api.orders.schemas import OrderCreateSchema

class OrderDAO:
    """Class for accessing order table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_order_model(self, order: OrderCreateSchema) -> None:
        """
        Add single order to session.

        :param name: name of a order.
        """
        self.session.add(order_model(
            payment_method=order.payment_method,
            bakery_id=order.bakery_id,
            product_id=order.product_id,
            user_id=order.user_id,
            state=order.state,
            created_at=order.created_at,
            updated_at=order.updated_at,
            tracking_number=order.tracking_number,
            start_baking_at=order.start_baking_at,
            finish_baking_at=order.finish_baking_at
        ))

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