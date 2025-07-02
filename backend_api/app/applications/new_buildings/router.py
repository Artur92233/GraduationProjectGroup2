import uuid
from typing import Annotated
from applications.users.models import User
from applications.auth.security import admin_required, get_current_user
from applications.new_buildings.crud import create_new_buildings_in_db, get_new_buildings_data, get_or_create_selected
from applications.new_buildings.schemas import NewBuildingSchema, SearchParamsSchema, SortTypeByEnum
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
):
    selected = await get_or_create_selected(user_id=user.id, session=session)

@new_buildings_router.post("/new_buildings")
async def create_new_buildings(
        main_image: UploadFile = File(...),
        images: list[UploadFile] = File(default=[]),
        title: str = Form(..., max_length=100),
        description: str = Form(..., max_length=1000),
        type: SortTypeByEnum = Body(SortTypeByEnum.SECOND_OWNER, max_length=50),
        apartment_count: int = Form(..., gt=1),
        price: float = Form(..., gt=1),
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
        price=price,
        address=address,
        contact=contact,
        main_image=main_image,
        images=images_urls,
        session=session,
    )
    return created_new_buildings


@new_buildings_router.get("/{pk}")
async def get_new_buildings_pk(pk: int, session: AsyncSession = Depends(get_async_session)) -> NewBuildingSchema:
    new_buildings_pk = await new_buildings_router(pk, session)
    if not new_buildings_pk:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with pk #{pk} not found")
    return new_buildings_pk


@new_buildings_router.get("/")
async def get_new_buildings(
        params: Annotated[SearchParamsSchema, Depends()], session: AsyncSession = Depends(get_async_session)
):
    result = await get_new_buildings_data(params, session)
    return result
