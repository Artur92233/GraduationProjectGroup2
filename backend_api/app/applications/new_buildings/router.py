from typing import Annotated
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status, UploadFile, Body
from applications.new_buildings.schemas import NewBuildingSchema, SearchParamsSchema
from sqlalchemy.ext.asyncio import AsyncSession
from database.session_dependencies import get_async_session
from applications.new_buildings.models import NewBuildings
from applications.auth.security import admin_required
import uuid
from services.s3.s3 import s3_storage
from applications.new_buildings.crud import get_new_buildings_data, get_new_buildings_by_pk, create_new_buildings_in_db
from applications.users.models import User
from applications.users.crud import create_user_in_db, get_user_by_email, activate_user_account
from applications.users.schemas import BaseUserInfo, RegisterUserFields
from database.session_dependencies import get_async_session


new_buildings_router = APIRouter()


@new_buildings_router.post('/', dependencies=[Depends(admin_required)])
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

    created_new_buildings = await create_new_buildings_in_db(new_buildings_uuid=new_buildings_uuid, title=title, description=description, type=type, price=price, address=address,
                                contact=contact, main_image=main_image, images=images_urls, session=session)
    return created_new_buildings


@new_buildings_router.get('/{pk}')
async def get_new_buildings(pk: int, session: AsyncSession = Depends(get_async_session)) -> NewBuildingSchema:
    new_buildings = await new_buildings_router(pk, session)
    if not new_buildings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with pk #{pk} not found")
    return new_buildings


@new_buildings_router.get('/')
async def get_new_buildings(params: Annotated[SearchParamsSchema, Depends()], session: AsyncSession = Depends(get_async_session)):
    result = await new_buildings_router(params, session)
    return result

