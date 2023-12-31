from pydantic import BaseModel
from enum import Enum


class OrderBaseSchema(BaseModel):
    payment_method: str
    bakery_id: int
    product_id: int
    start_baking_at: str
    finish_baking_at: str


class OrderStatus(Enum):
    NEW = 'new'
    CANCELLED = 'cancelled'
    PENDING = 'pending'
    BAKING = 'baking'
    READY = 'ready'
    COMPLETED = 'completed'


class OrderCreateSchema(OrderBaseSchema):
    user_id: int
    state: str
    created_at: str
    updated_at: str
    tracking_number: str


class OrderSchema(OrderBaseSchema):
    id: int


class CreatedOrderSchema(OrderBaseSchema):
    id: int
    tracking_number: str


class OrderStateUpdateSchema(BaseModel):
    state: str
    updated_at: str
