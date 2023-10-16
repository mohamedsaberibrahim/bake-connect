
from app.api.orders.schemas import OrderBaseSchema, OrderCreateSchema
from app.api.orders.builder.order_builder import Builder

class OrderService:
    def __init__(self) -> None:
        self.builder = Builder()

    def create_order_builder(self, payload: OrderBaseSchema, user_id: int) -> OrderCreateSchema:
        self.builder.set_payment_method(payload.payment_method)
        self.builder.set_bakery_id(payload.bakery_id)
        self.builder.set_product_id(payload.product_id)
        self.builder.set_user_id(user_id)
        self.builder.set_state()
        self.builder.set_created_at()
        self.builder.set_updated_at()
        self.builder.set_tracking_number()
        self.builder.set_start_baking_at()
        self.builder.set_finish_baking_at()
        return self.builder.get_order()
