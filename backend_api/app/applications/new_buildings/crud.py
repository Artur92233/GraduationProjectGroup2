import uuid
from typing import Annotated
from applications.new_buildings.models import NewBuildings
from sqlalchemy.ext.asyncio import AsyncSession
from applications.new_buildings.schemas import SearchParamsSchema, SortEnum, SortByEnum
from sqlalchemy import asc, desc, select, func, or_, and_
import math


# from applications.new_buildings.schemas import SearchParamsSchema, SortEnum, SortByEnum


async def create_new_buildings_in_db(new_buildings_uuid, title, description, type, price, address, contact, main_image, images, session) -> NewBuildings:
    new_buildings = NewBuildings(
        uuid_data=new_buildings_uuid,
        title=title.strip(),
        description=description.strip(),
        type=type,
        price=price,
        address=address,
        contact=contact,
        main_image=main_image,
        images=images
    )
    session.add(new_buildings)
    await session.commit()
    await session.refresh(new_buildings)
    return new_buildings


async def get_new_buildings_data(params: SearchParamsSchema, session: AsyncSession):
    query = select(NewBuildings)
    count_query = select(func.count()).select_from(NewBuildings)

    order_direction = asc if params.order_direction == SortEnum.ASC else desc

    if params.q:
        search_fields = [NewBuildings.title, NewBuildings.description]
        if params.use_sharp_q_filter:
            cleaned_query = params.q.strip().lower()
            search_condition = or_(*[func.lower(field) == cleaned_query for field in search_fields])
            query = query.filter(search_condition)
            count_query = count_query.filter(search_condition)
        else:
            words = [word for word in params.q.strip().split() if len(word) > 1]
            search_condition = or_(
                and_(*(search_field.icontains(word) for word in words)) for search_field in search_fields
            )
            query = query.filter(search_condition)
            count_query = count_query.filter(search_condition)


    sort_field = NewBuildings.price if params.sort_by == SortByEnum.PRICE else NewBuildings.id
    query = query.order_by(order_direction(sort_field))
    offset = (params.page - 1) * params.limit
    query = query.offset(offset).limit(params.limit)

    result = await session.execute(query)
    result_count = await session.execute(count_query)
    total = result_count.scalar()

    return {
        "items": result.scalars().all(),
        "total": total,
        'page': params.page,
        'limit': params.limit,
        'pages': math.ceil(total / params.limit)
    }


async def get_new_buildings_by_pk(pk: int, session: AsyncSession) -> NewBuildings | None:
    query = select(NewBuildings).filter(NewBuildings.id == pk)
    result = await session.execute(query)
    return result.scalar_one_or_none()

