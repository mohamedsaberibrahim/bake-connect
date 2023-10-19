from fastapi import APIRouter, Body, Depends
from typing import List

from app.api.products.schemas import ProductSchema, ProductBaseSchema
from app.api.products.schemas import ProductUpdateSchema
from app.api.products.models import Product as product_model
from app.api.products.dao import ProductDAO
from app.api.auth.services import AuthHandler
from app.api.bakeries.dao import BakeryDAO
from app.api.products.services import ProductService

router = APIRouter()
auth_handler = AuthHandler()


@router.post('', response_model=List[ProductSchema])
async def create_product(
    payload: ProductBaseSchema = Body(),
    product_dao: ProductDAO = Depends(),
    bakery_dao: BakeryDAO = Depends(),
    user_id=Depends(auth_handler.auth_wrapper)
):
    """Processes request to create product."""
    bakery = await bakery_dao.get_bakery_by_owner_id(owner_id=user_id)
    await product_dao.create_product_model(product=payload, bakery_id=bakery.id)
    product: List[product_model] = await product_dao.filter(
        baker_id=bakery.id, name=payload.name)
    return product


@router.delete('/{product_id}')
async def delete_product(
    product_id: int,
    product_service: ProductService = Depends(),
    user_id=Depends(auth_handler.auth_wrapper)
):
    """Processes request to delete product."""
    await product_service.delete_product(product_id=product_id, user_id=user_id)
    return {'success': True, 'message': 'Product deleted successfully'}


@router.put('/{product_id}')
async def update_product(
    product_id: int,
    payload: ProductUpdateSchema = Body(),
    product_service: ProductService = Depends(),
    user_id=Depends(auth_handler.auth_wrapper)
):
    """Processes request to update product."""
    await product_service.update_product(
        product_id=product_id, payload=payload, user_id=user_id)
    return {'success': True, 'message': 'Product updated successfully'}


@router.get('')
async def list_products(
    limit: int = 10,
    offset: int = 0,
    name: str = None,
    location: str = None,
    product_service: ProductService = Depends(),
):
    """Processes request to list products."""
    products = await product_service.list_products(
        limit=limit, offset=offset, name=name, location=location)
    return {'success': True,
            'data': products,
            'message': 'Fetching products successfully.'}
