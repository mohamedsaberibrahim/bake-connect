from fastapi import Depends, HTTPException
from http import HTTPStatus
from datetime import datetime, timedelta
from app.api.bakeries.dao import BakeryDAO
from app.api.orders.dao import OrderDAO
from app.api.products.dao import ProductDAO
from app.api.bakeries.schemas import BakerySchema, BakeryBaseSchema
from app.api.orders.schemas import OrderSchema
from typing import List
from app.utils.time_utils import find_available_time_slots, get_available_ready_times

class BakeryService:
    """Bakery service class"""
    def __init__(self,
        bakery_dao: BakeryDAO = Depends(),
        order_dao: OrderDAO = Depends(),
        product_dao: ProductDAO = Depends()
    ):
        self.bakery_dao = bakery_dao
        self.order_dao = order_dao
        self.product_dao = product_dao

    async def create_bakery(self, payload: BakeryBaseSchema, user_id: int) -> BakerySchema:
        """Processes request to register bakery account."""
        await self.bakery_dao.create_bakery_model(bakery=payload, owner_id=user_id)
        bakery = await self.bakery_dao.get_bakery_by_owner_id(owner_id=user_id)
        return bakery
    
    async def get_bakery(self, bakery_id: int) -> BakerySchema:
        """Processes request to get bakery profile."""
        bakery = await self.bakery_dao.get_bakery_by_id(bakery_id=bakery_id)
        if not bakery:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Bakery not found'
            )
        return bakery

    async def calculate_collection_time(self, bakery_id: int, product_id: int):
        """Processes request to calculate collection time."""
        orders = await self.order_dao.filter(baker_id=bakery_id)
        orders.sort(key=lambda x: x.start_baking_at)

        busy_slots = []
        for order in orders:
            if order.start_baking_at and order.finish_baking_at:
                busy_slots.append((order.start_baking_at, order.finish_baking_at))

        result = find_available_time_slots(busy_slots, datetime(2023, 10, 19, 12, 0), datetime(2023, 10, 19, 23, 59))

        [product] = await self.product_dao.filter(id=product_id)
        available_collection_time = get_available_ready_times(result, product.baking_time)
        return available_collection_time