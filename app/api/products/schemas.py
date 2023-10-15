from pydantic import BaseModel

class ProductBaseSchema(BaseModel):
    name: str
    baking_time: int
    price: int
    image_url: str = None

class ProductSchema(ProductBaseSchema):
    id: int
    baker_id: int
