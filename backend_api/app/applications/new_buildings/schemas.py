from enum import StrEnum
from typing import Annotated, Optional

from pydantic import BaseModel, Field

class SortTypeByEnum(StrEnum):
    NEW_BUILDING = 'Новобудова'
    SECOND_OWNER = 'На вторинному ринку'
    FOR_RENT = 'На оренду'

class NewBuildingSchema(BaseModel):
    id: int
    title: str = Field(..., max_length=100)
    description: str
    type: str
    apartment_count: int
    price: float
    address: str
    contact: str
    main_image: str
    images: list[str]


class SortEnum(StrEnum):
    ASC = "asc"
    DESC = "desc"


class SortByEnum(StrEnum):
    ID = "id"
    PRICE = "price"


class SearchParamsSchema(BaseModel):
    q: Annotated[Optional[str], Field(default=None)] = None
    page: Annotated[int, Field(default=1, ge=1)]
    limit: Annotated[int, Field(default=10, ge=1, le=50)]
    order_direction: SortEnum = SortEnum.DESC
    sort_by: SortByEnum = SortByEnum.ID
    use_sharp_q_filter: bool = Field(default=False, description="used to search exact q")
