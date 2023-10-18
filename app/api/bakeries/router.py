from fastapi import APIRouter, Body, Depends, HTTPException

from http import HTTPStatus
from app.api.bakeries.schemas import BakerySchema, BakeryBaseSchema
from app.api.bakeries.models import Bakery as bakery_model
from app.api.bakeries.services import BakeryService
from app.api.auth.services import AuthHandler

router = APIRouter()
auth_handler = AuthHandler()

@router.post('', response_model=BakerySchema)
async def create_bakery_profile(
    payload: BakeryBaseSchema = Body(),
    bakery_service: BakeryService = Depends(),
    user_id = Depends(auth_handler.auth_wrapper)
):
    """Processes request to register bakery account."""
    bakery = await bakery_service.create_bakery(payload=payload, user_id=user_id)
    return bakery

@router.get('/{bakery_id}', response_model=BakerySchema)
async def get_bakery_profile(
    bakery_id: int,
    bakery_service: BakeryService = Depends()
):
    """Processes request to get bakery profile."""
    bakery = await bakery_service.get_bakery(bakery_id=bakery_id)
    return bakery

@router.get('/{bakery_id}/products/{product_id}/calculate-collection-time')
async def calculate_collection_time(
    bakery_id: int,
    product_id: int,
    bakery_service: BakeryService = Depends()
):
    """Processes request to calculate collection time."""
    available_collection_time = await bakery_service.calculate_collection_time(bakery_id=bakery_id, product_id=product_id)
    return { 'success': True, 'message': 'Collection time calculated successfully.', 'data': available_collection_time }