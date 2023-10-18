from fastapi import Depends, HTTPException
from http import HTTPStatus

from app.api.products.dao import ProductDAO
from app.api.bakeries.dao import BakeryDAO
from app.api.orders.dao import OrderDAO


class ProductService:
    def __init__(self,
        product_dao: ProductDAO = Depends(),
        bakery_dao: BakeryDAO = Depends(),
        order_dao: OrderDAO = Depends()
    ):
        self.product_dao = product_dao
        self.bakery_dao = bakery_dao
        self.order_dao = order_dao

    async def list_products(self, limit: int = 12, offset: int = 0, name: str = None, location: str = None):
        products = await self.product_dao.filter(limit=limit, offset=offset, name=name, location=location)
        return products

    async def delete_product(self, product_id, user_id):
        orders = await self.order_dao.filter(product_id=product_id)
        if len(orders) > 0:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Cannot delete product with orders'
            )

        bakery = await self.bakery_dao.get_bakery_by_owner_id(owner_id=user_id)
        await self.product_dao.delete_product_model(product_id=product_id, bakery_id=bakery.id)
        return { 'success': True, 'message': 'Product deleted successfully' }

    async def update_product(self, product_id, payload, user_id):
        bakery = await self.bakery_dao.get_bakery_by_owner_id(owner_id=user_id)
        products = await self.product_dao.filter(id=product_id, baker_id=bakery.id)
        if len(products) == 0:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Product not found'
            )

        await self.product_dao.update_product_model(product_id=product_id, payload=payload)
        return { 'success': True, 'message': 'Product updated successfully' }
