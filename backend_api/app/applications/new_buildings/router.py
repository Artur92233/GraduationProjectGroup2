import uuid
from typing import Annotated

from applications.auth.security import admin_required
from applications.new_buildings.crud import create_new_buildings_in_db
from applications.new_buildings.schemas import NewBuildingSchema, SearchParamsSchema
from database.session_dependencies import get_async_session
from fastapi import APIRouter, Body, Depends, HTTPException, UploadFile, status
from services.s3.s3 import s3_storage
from sqlalchemy.ext.asyncio import AsyncSession

new_buildings_router = APIRouter()


@new_buildings_router.post("/", dependencies=[Depends(admin_required)])
async def create_new_buildings(
    main_image: UploadFile,
    images: list[UploadFile] = None,
    title: str = Body(max_length=100),
    description: str = Body(max_length=1000),
    type: str = Body(max_length=50),
    price: float = Body(gt=1),
    address: str = Body(max_length=200),
    contact: str = Body(max_length=100),
    session: AsyncSession = Depends(get_async_session),
) -> NewBuildingSchema:
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
        price=price,
        address=address,
        contact=contact,
        main_image=main_image,
        images=images_urls,
        session=session,
    )
    return created_new_buildings


@new_buildings_router.get("/{pk}")
async def get_new_buildings(pk: int, session: AsyncSession = Depends(get_async_session)) -> NewBuildingSchema:
    new_buildings = await new_buildings_router(pk, session)
    if not new_buildings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with pk #{pk} not found")
    return new_buildings


@new_buildings_router.get("/")
async def get_new_buildings(
    params: Annotated[SearchParamsSchema, Depends()], session: AsyncSession = Depends(get_async_session)
):
    result = await new_buildings_router(params, session)
    return result
