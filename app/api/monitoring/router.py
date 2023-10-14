from fastapi import APIRouter
from http import HTTPStatus

router = APIRouter()

@router.get("/health")
async def get_health_check():
    return {"message": "Server is running & up!", "status": HTTPStatus.OK }
