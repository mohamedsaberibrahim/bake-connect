from app.api.orders.schemas import OrderSchema, OrderStatus
from app.api.orders.states.base_state import OrderState

class BakingOrderState(OrderState):
    """Class for baking order state."""

    def process(self, order: OrderSchema):
        """Execute state."""
        order.state = OrderStatus.BAKING.value
        return order
