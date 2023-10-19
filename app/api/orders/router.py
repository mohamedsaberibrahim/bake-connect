from fastapi import APIRouter, Body, Depends

from app.api.orders.schemas import OrderSchema, OrderBaseSchema, OrderStateUpdateSchema
from app.api.auth.services import AuthHandler
from app.api.orders.services import OrderService

router = APIRouter()
auth_handler = AuthHandler()


@router.post('')
async def create_order(
    payload: OrderBaseSchema = Body(),
    order_service: OrderService = Depends(),
    user_id=Depends(auth_handler.auth_wrapper)
):
    """Processes request to register order account."""
    order = await order_service.create_order(payload=payload, user_id=user_id)
    return order


@router.put('/{tracking_number}/state', response_model=OrderSchema)
async def update_order_state(
    tracking_number: str,
    payload: OrderStateUpdateSchema = Body(),
    order_service: OrderService = Depends(),
    user_id=Depends(auth_handler.auth_wrapper)
):
    """Processes request to update order state."""
    order = await order_service.update_order_state(
        tracking_number=tracking_number, payload=payload, user_id=user_id)
    return order
