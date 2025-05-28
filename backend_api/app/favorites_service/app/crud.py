from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Favorite
from app.schemas import FavoriteCreate


async def create_favorite(db: AsyncSession, fav: FavoriteCreate):
    new_fav = Favorite(**fav.dict())
    db.add(new_fav)
    await db.commit()
    await db.refresh(new_fav)
    return new_fav


async def delete_favorite(db: AsyncSession, fav: FavoriteCreate):
    result = await db.execute(
        select(Favorite).where(Favorite.user_id == fav.user_id, Favorite.apartment_id == fav.apartment_id)
    )
    obj = result.scalar_one_or_none()
    if obj:
        await db.delete(obj)
        await db.commit()
        return True
    return False
