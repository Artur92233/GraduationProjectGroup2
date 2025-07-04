from pydantic import BaseModel, Field
from typing import List

class  NewBuildingSchema(BaseModel):
    id: int
    title: str = Field(..., max_length=100)
    description: str
    type: str
    apartment_count: int
    apartment_price: float
    address: str
    contact: str
    main_image: str
    images: list[str]