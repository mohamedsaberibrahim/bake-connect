from pydantic import BaseModel


class BakeryBaseSchema(BaseModel):
    brand_name: str
    address: str
    phone: str
    description: str
    logo_url: str = None


class BakerySchema(BakeryBaseSchema):
    id: int
    owner_id: int
