
from app.api.orders.schemas import OrderBaseSchema, OrderCreateSchema
from app.api.orders.schemas import OrderStateUpdateSchema, OrderStatus, OrderSchema
from app.api.orders.builder.order_builder import Builder
from app.api.orders.dao import OrderDAO
from fastapi import Depends
from fastapi.exceptions import HTTPException
from http import HTTPStatus
from app.api.orders.states.cancelled_order_state import CancelledOrderState
from app.api.orders.states.pending_order_state import PendingOrderState
from app.api.orders.states.baking_order_state import BakingOrderState
from app.api.orders.states.ready_order_state import ReadyOrderState
from app.api.orders.states.completed_order_state import CompletedOrderState
from app.api.orders.models import Order as order_model


class OrderService:
    def __init__(self, order_dao: OrderDAO = Depends()) -> None:
        self.builder = Builder()
        self.order_dao = order_dao

    async def create_order(self, payload: OrderBaseSchema, user_id: int) -> order_model:
        order = await self.create_order_builder(payload=payload, user_id=user_id)

        await self.order_dao.create_order_model(order)
        order: order_model = await self.order_dao.get_order_by_tracking_number(
            tracking_number=order.tracking_number)
        return order

    async def create_order_builder(
            self, payload: OrderBaseSchema, user_id: int) -> order_model:
        self.builder.set_payment_method(payload.payment_method)
        self.builder.set_bakery_id(payload.bakery_id)
        self.builder.set_product_id(payload.product_id)
        self.builder.set_user_id(user_id)
        self.builder.set_state()
        self.builder.set_created_at()
        self.builder.set_updated_at()
        self.builder.set_tracking_number()
        self.builder.set_start_baking_at(payload.start_baking_at)
        self.builder.set_finish_baking_at(payload.finish_baking_at)
        return self.builder.get_order()

    async def update_order_state(
            self,
            tracking_number: str,
            payload: OrderStateUpdateSchema,
            user_id: int
    ) -> OrderCreateSchema:
        order = await self.order_dao.get_order_by_tracking_number(
            tracking_number=tracking_number)
        if order is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Order not found.')
        if order.user_id != user_id:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail='You are not allowed to update this order.')

        state_mapping = {
            OrderStatus.CANCELLED.value: CancelledOrderState(),
            OrderStatus.PENDING.value: PendingOrderState(),
            OrderStatus.BAKING.value: BakingOrderState(),
            OrderStatus.READY.value: ReadyOrderState(),
            OrderStatus.COMPLETED.value: CompletedOrderState()
        }

        if payload.state not in state_mapping:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail='Invalid state.')

        self.transit_to_state = state_mapping[payload.state]

        order = self.transit_to_state.process(order=order)
        await self.order_dao.update_order_model(order=order)

        order: OrderSchema = await self.order_dao.get_order_by_tracking_number(
            tracking_number=order.tracking_number)
        return order
