from fastapi import APIRouter, Body, Depends, HTTPException

from http import HTTPStatus
from app.api.orders.schemas import OrderSchema, OrderBaseSchema, CreatedOrderSchema, OrderStateUpdateSchema
from app.api.orders.models import Order as order_model
from app.api.orders.dao import OrderDAO
from app.api.auth.services import AuthHandler
from app.api.orders.services import OrderService

router = APIRouter()
auth_handler = AuthHandler()

@router.post('', response_model=OrderSchema)
async def create_order(
    payload: OrderBaseSchema = Body(), 
    order_service: OrderService = Depends(),
    order_dao: OrderDAO = Depends(),
    user_id = Depends(auth_handler.auth_wrapper)
):
    """Processes request to register order account."""
    order = order_service.create_order_builder(payload=payload, user_id=user_id)
    await order_dao.create_order_model(order)
    order:order_model = await order_dao.get_order_by_tracking_number(tracking_number=order.tracking_number)
    return order


@router.put('/{tracking_number}/state', response_model=OrderSchema)
async def update_order_state(
    tracking_number: str, 
    payload: OrderStateUpdateSchema = Body(), 
    order_service: OrderService = Depends(),
    user_id = Depends(auth_handler.auth_wrapper)
):
    """Processes request to update order state."""
    order = await order_service.update_order_state(tracking_number=tracking_number, payload=payload, user_id=user_id)
    return order
