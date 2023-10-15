from fastapi import APIRouter, Body, Depends, HTTPException

from http import HTTPStatus
from app.api.bakeries.schemas import BakerySchema, BakeryBaseSchema
from app.api.bakeries.models import Bakery as bakery_model
from app.api.bakeries.dao import BakeryDAO
from app.api.auth.services import AuthHandler

router = APIRouter()
auth_handler = AuthHandler()

@router.post('', response_model=BakerySchema)
async def create_bakery_profile(
    payload: BakeryBaseSchema = Body(), 
    bakery_dao: BakeryDAO = Depends(),
    user_id = Depends(auth_handler.auth_wrapper)
):
    """Processes request to register bakery account."""
    await bakery_dao.create_bakery_model(bakery=payload, owner_id=user_id)
    bakery:bakery_model = await bakery_dao.get_bakery_by_owner_id(owner_id=user_id)
    return bakery
