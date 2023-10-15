from fastapi import APIRouter, Body, Depends, HTTPException
from typing import List

from http import HTTPStatus
from app.api.products.schemas import ProductSchema, ProductBaseSchema
from app.api.products.models import Product as product_model
from app.api.products.dao import ProductDAO
from app.api.auth.services import AuthHandler
from app.api.bakeries.dao import BakeryDAO

router = APIRouter()
auth_handler = AuthHandler()

@router.post('', response_model=List[ProductSchema])
async def create_product(
    payload: ProductBaseSchema = Body(), 
    product_dao: ProductDAO = Depends(),
    bakery_dao: BakeryDAO = Depends(),
    user_id = Depends(auth_handler.auth_wrapper)
):
    """Processes request to create product."""
    bakery = await bakery_dao.get_bakery_by_owner_id(owner_id=user_id)
    await product_dao.create_product_model(product=payload, bakery_id=bakery.id)
    product:List[product_model] = await product_dao.filter(baker_id=bakery.id, name=payload.name)
    return product
