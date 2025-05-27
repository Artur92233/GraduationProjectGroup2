from pydantic import BaseModel

class FavoriteBase(BaseModel):
    user_id: str
    apartment: str

class FavoriteCreate(FavoriteBase):
    pass

class Favorite(FavoriteBase):
    id: int

    class Config:
        from_attributes = True