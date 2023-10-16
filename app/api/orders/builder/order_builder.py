from app.api.orders.schemas import OrderCreateSchema
# from app.utils.generator import Generator
from datetime import datetime
from random import randint

class Builder:
    def __init__(self):
        self.order: OrderCreateSchema = None
        # self.generator = Generator
    
    def set_payment_method(self, payment_method: str) -> None:
        self.order.payment_method = payment_method

    def set_bakery_id(self, bakery_id: int) -> None:
        self.order.bakery_id = bakery_id
    
    def set_product_id(self, product_id: int) -> None:
        self.order.product_id = product_id

    def set_user_id(self, user_id: int) -> None:
        self.order.user_id = user_id
    
    def set_state(self, state: str) -> None:
        self.order.state = state

    def set_created_at(self) -> None:
        self.order.created_at = datetime.now()
    
    def set_updated_at(self) -> None:
        self.order.updated_at = datetime.now()
    
    def set_tracking_number(self) -> None:
        # self.order.tracking_number = self.generator.generate_id()
        self.order.tracking_number = randint(1000000000, 9999999999)
    
    def set_start_baking_at(self, start_baking_at: datetime) -> None:
        self.order.start_baking_at = start_baking_at
    
    def set_finish_baking_at(self, finish_baking_at: datetime) -> None:
        self.order.finish_baking_at = finish_baking_at
    
    def get_order(self) -> OrderCreateSchema:
        return self.order
