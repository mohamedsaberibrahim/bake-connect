from app.api.orders.schemas import OrderSchema, OrderStatus
from app.api.orders.states.base_state import OrderState

class PendingOrderState(OrderState):
    """Class for pending order state."""

    def process(self, order: OrderSchema):
        """Execute state."""
        order.state = OrderStatus.PENDING.value
        return order
