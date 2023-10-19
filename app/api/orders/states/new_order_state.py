from app.api.orders.states.base_state import OrderState
from app.api.orders.schemas import OrderSchema, OrderStatus


class NewOrderState(OrderState):
    """Class for new order state."""

    def process(self, order: OrderSchema):
        """Execute state."""
        order.state = OrderStatus.NEW.value
        return order
