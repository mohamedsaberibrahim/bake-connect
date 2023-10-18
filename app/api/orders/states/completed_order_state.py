from app.api.orders.schemas import OrderSchema, OrderStatus
from app.api.orders.states.base_state import OrderState

class CompletedOrderState(OrderState):
    """Class for completed order state."""

    def process(self, order: OrderSchema):
        """Execute state."""
        order.state = OrderStatus.COMPLETED.value
        return order