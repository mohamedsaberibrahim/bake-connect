from pydantic import BaseModel

class OrderBaseSchema(BaseModel):
    payment_method: str
    bakery_id: int
    product_id: int

class OrderCreateSchema(OrderBaseSchema):
    user_id: int
    state: str
    created_at: str
    updated_at: str
    tracking_number: str
    start_baking_at: str
    finish_baking_at: str

class OrderSchema(OrderBaseSchema):
    id: int

class CreatedOrderSchema(OrderBaseSchema):
    id: int
    tracking_number: str