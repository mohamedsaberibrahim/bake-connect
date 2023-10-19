from pydantic import BaseModel


class ProductBaseSchema(BaseModel):
    name: str
    baking_time: int
    price: int
    image_url: str = None
    location: str


class ProductSchema(ProductBaseSchema):
    id: int
    baker_id: int


class ProductUpdateSchema(BaseModel):
    name: str = None
    baking_time: int = None
    price: int = None
    image_url: str = None
    location: str = None
