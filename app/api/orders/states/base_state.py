from abc import ABC, abstractmethod
from app.api.orders.dao import OrderDAO
from fastapi import Depends

class OrderState(ABC):
    """Abstract class for order states."""

    def __init__(self, order_dao: OrderDAO = Depends()):
        self.order_dao = order_dao

    @abstractmethod
    def process(self, order):
        pass
