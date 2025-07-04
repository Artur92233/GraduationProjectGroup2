from pydantic import BaseModel, Field
from typing import List
from enum import StrEnum

class NewBuildingSchema(BaseModel):
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


class SortTypeByEnum(StrEnum):
    NEW_BUILDING = 'Новобудова'
    SECOND_OWNER = 'На вторинному ринку'
    FOR_RENT = 'На оренду'