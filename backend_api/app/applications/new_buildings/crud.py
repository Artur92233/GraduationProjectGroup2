import math

from applications.auth.security import admin_required
from applications.new_buildings.models import NewBuildings, Selected, SelectedNewBuildings
from applications.new_buildings.schemas import (NewBuildingSchema, SearchParamsSchema, SortByEnum, SortEnum,
                                                SortTypeByEnum)
from fastapi import APIRouter
from sqlalchemy import and_, asc, desc, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

new_buildings_router = APIRouter()


# Определяем admin_check на уровне модуля
async def admin_check(user, type: SortTypeByEnum):
    if type == SortTypeByEnum.NEW_BUILDING:
        await admin_required(user)


async def create_new_buildings_in_db(
    new_buildings_uuid,
    title,
    description,
    type,
    apartment_count,
    apartment_price,
    address,
    contact,
    main_image,
    images,
    session,
) -> NewBuildingSchema:
    new_buildings = NewBuildings(
        uuid_data=new_buildings_uuid,
        title=title.strip(),
        description=description.strip(),
        type=type,
        apartment_count=apartment_count,
        apartment_price=apartment_price,
        address=address,
        contact=contact,
        main_image=main_image,
        images=images,
    )
    session.add(new_buildings)
    await session.commit()
    await session.refresh(new_buildings)
    return new_buildings


async def get_new_buildings_data(params: SearchParamsSchema, session: AsyncSession):
    query = select(NewBuildings)
    count_query = select(func.count()).select_from(NewBuildings)

    order_direction = asc if params.order_direction == SortEnum.ASC else desc

    # Фильтр по типу, если передан

    if params.type and params.type in SortTypeByEnum.__members__.values():
        query = query.filter(NewBuildings.type == params.type)
        count_query = count_query.filter(NewBuildings.type == params.type)

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
                and_(*(search_field.ilike(f"%{word}%") for word in words)) for search_field in search_fields
            )
            query = query.filter(search_condition)
            count_query = count_query.filter(search_condition)

    sort_field = NewBuildings.apartment_price if params.sort_by == SortByEnum.APARTMENT_PRICE else NewBuildings.id
    query = query.order_by(order_direction(sort_field))
    offset = (params.page - 1) * params.limit
    query = query.offset(offset).limit(params.limit)

    result = await session.execute(query)
    result_count = await session.execute(count_query)
    total = result_count.scalar_one()

    return {
        "items": result.scalars().all(),
        "total": total,
        "page": params.page,
        "limit": params.limit,
        "pages": math.ceil(total / params.limit),
    }


async def get_new_buildings_by_pk(pk: int, session: AsyncSession) -> NewBuildings | None:
    query = select(NewBuildings).filter(NewBuildings.id == pk)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_or_create_selected(user_id: int, session: AsyncSession):
    query = select(Selected).filter_by(user_id=user_id, is_closed=False)
    result = await session.execute(query)
    selected = result.scalar_one_or_none()

    if selected:
        return selected

    selected = Selected(user_id=user_id, is_closed=False)
    session.add(selected)
    await session.commit()
    return selected


async def get_or_create_selected_new_buildings(
    NewBuildings_id: int, selected_id: int, session: AsyncSession
) -> SelectedNewBuildings:
    query = select(SelectedNewBuildings).filter_by(selected_id=selected_id, NewBuildings_id=NewBuildings_id)
    result = await session.execute(query)
    selected_new_buildings = result.scalar_one_or_none()

    if selected_new_buildings:
        return selected_new_buildings

    selected_new_buildings = SelectedNewBuildings(selected_id=selected_id, NewBuildings_id=NewBuildings_id)
    session.add(selected_new_buildings)
    await session.commit()
    return selected_new_buildings
