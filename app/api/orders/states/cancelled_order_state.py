from app.api.orders.schemas import OrderSchema, OrderStatus
from app.api.orders.states.base_state import OrderState
from datetime import datetime


class CancelledOrderState(OrderState):
    """Class for cancelled order state."""

    def process(self, order: OrderSchema):
        """Execute state."""
        if order.state != OrderStatus.NEW.value:
            raise Exception('Order is not in NEW state.')
        order.state = OrderStatus.CANCELLED.value
        order.cancelled_at = datetime.now().isoformat()
        return order
