import uuid
from typing import Annotated
from applications.users.models import User
from applications.auth.security import admin_required, get_current_user
from applications.new_buildings.crud import create_new_buildings_in_db, get_new_buildings_data, get_or_create_selected, get_or_create_selected_new_buildings, get_new_buildings_by_pk
from applications.new_buildings.schemas import NewBuildingSchema, SearchParamsSchema, SortTypeByEnum, SelectedSchema, SelectedNewBuildingsSchema
from database.session_dependencies import get_async_session
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status, Form, File, Body
from services.s3.s3 import s3_storage
from sqlalchemy.ext.asyncio import AsyncSession

from applications.new_buildings.crud import admin_check

new_buildings_router = APIRouter()
selected_router = APIRouter()


@selected_router.get("/")
async def get_current_selected(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
) -> SelectedSchema:
    selected = await get_or_create_selected(user_id=user.id, session=session)
    return selected

@selected_router.patch("/change-new-buildings")
async def change_new_buildings(
    quantity: float,
    new_buildings_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> SelectedSchema:
    selected = await get_or_create_selected(user_id=user.id, session=session)
    new_buildings = await get_new_buildings_by_pk(new_buildings_id, session)
    if not new_buildings:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='No product')

    selected_new_buildings = await get_or_create_selected_new_buildings(new_buildings_id, selected.id, session)  # Виправлено

    selected_new_buildings.quantity += quantity
    if selected_new_buildings.quantity < 0:
        selected_new_buildings.quantity = 0

    selected_new_buildings.price = new_buildings.apartment_price

    session.add(selected_new_buildings)
    await session.commit()

    selected = await get_or_create_selected(user_id=user.id, session=session)
    return selected



@new_buildings_router.post("/new_buildings")
async def create_new_buildings(
        main_image: UploadFile = File(...),
        images: list[UploadFile] = File(default=[]),
        title: str = Form(..., max_length=100),
        description: str = Form(..., max_length=1000),
        type: SortTypeByEnum = Body(SortTypeByEnum.SECOND_OWNER, max_length=50),
        apartment_count: int = Form(..., gt=1),
        apartment_price: float = Form(..., gt=1),
        address: str = Form(..., max_length=200),
        contact: str = Form(..., max_length=100),
        session: AsyncSession = Depends(get_async_session),
        user = Depends(get_current_user)
) -> NewBuildingSchema:
    await admin_check(user, type)  # Передаем оба аргумента
    new_buildings_uuid = uuid.uuid4()
    main_image = await s3_storage.upload_new_buildings_image(main_image, new_buildings_uuid=new_buildings_uuid)
    images = images or []
    images_urls = []
    for image in images:
        url = await s3_storage.upload_new_buildings_image(image, new_buildings_uuid=new_buildings_uuid)
        images_urls.append(url)
    created_new_buildings = await create_new_buildings_in_db(
        new_buildings_uuid=new_buildings_uuid,
        title=title,
        description=description,
        type=type,
        apartment_count=apartment_count,
        apartment_price=apartment_price,
        address=address,
        contact=contact,
        main_image=main_image,
        images=images_urls,
        session=session,
    )
    return created_new_buildings


@new_buildings_router.get("/{pk}")
async def get_new_buildings_pk(pk: int, session: AsyncSession = Depends(get_async_session)) -> NewBuildingSchema:
    new_buildings_pk = await get_new_buildings_by_pk(pk, session)
    if not new_buildings_pk:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with pk #{pk} not found")
    return new_buildings_pk


@new_buildings_router.get("/")
async def get_new_buildings(
        params: Annotated[SearchParamsSchema, Depends()], session: AsyncSession = Depends(get_async_session)
):
    result = await get_new_buildings_data(params, session)
    return result
