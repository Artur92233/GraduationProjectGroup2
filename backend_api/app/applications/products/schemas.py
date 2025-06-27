from pydantic import BaseModel


class ProductSchema(BaseModel):
    id: int
    title: str
    type: str
    description: str