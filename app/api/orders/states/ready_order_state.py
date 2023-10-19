from app.api.orders.schemas import OrderSchema, OrderStatus
from app.api.orders.states.base_state import OrderState


class ReadyOrderState(OrderState):
    """Class for ready order state."""

    def process(self, order: OrderSchema):
        """Execute state."""
        order.state = OrderStatus.READY.value
        return order
