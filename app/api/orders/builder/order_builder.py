from app.api.orders.schemas import OrderCreateSchema, OrderStatus
from app.api.orders.models import Order as order_model
from datetime import datetime
from random import randint

class Builder:
    def __init__(self):
        pass

    def set_payment_method(self, payment_method: str) -> None:
        self.payment_method = payment_method

    def set_bakery_id(self, bakery_id: int) -> None:
        self.bakery_id = bakery_id
    
    def set_product_id(self, product_id: int) -> None:
        self.product_id = product_id

    def set_user_id(self, user_id: int) -> None:
        self.user_id = user_id
    
    def set_state(self) -> None:
        self.state = OrderStatus.NEW.value

    def set_created_at(self) -> None:
        self.created_at = datetime.now().isoformat()
    
    def set_updated_at(self) -> None:
        self.updated_at = datetime.now().isoformat()
    
    def set_tracking_number(self) -> None:
        self.tracking_number = str(randint(10000, 99999))
    
    def set_start_baking_at(self) -> None:
        self.start_baking_at = datetime.now().isoformat()
    
    def set_finish_baking_at(self) -> None:
        self.finish_baking_at = datetime.now().isoformat()
    
    def get_order(self) -> order_model:
        return order_model(
            payment_method=self.payment_method,
            bakery_id=self.bakery_id,
            product_id=self.product_id,
            user_id=self.user_id,
            state=self.state,
            created_at=self.created_at,
            updated_at=self.updated_at,
            tracking_number=self.tracking_number,
            start_baking_at=self.start_baking_at,
            finish_baking_at=self.finish_baking_at
        )
