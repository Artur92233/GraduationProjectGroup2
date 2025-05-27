from pydantic import BaseModel

class FavoriteBase(BaseModel):
    user_id: int
    apartment_id: int

class FavoriteCreate(FavoriteBase):
    pass

class Favorite(FavoriteBase):
    id: int

    class Config:
        orm_mode = True
