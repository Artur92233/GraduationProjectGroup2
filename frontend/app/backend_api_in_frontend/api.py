import uuid
from enum import StrEnum
from urllib.parse import urljoin
from uuid import uuid4

import httpx
from fastapi import Body, Depends, File, Form, Request, UploadFile
from new_buildings_schema import NewBuildingSchema, SortTypeByEnum
from settings import settings


from services.s3.s3_frontend import s3_storage



async def login_user(user_email: str, password: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=urljoin(settings.BACKEND_API, "auth/login"),  # Безопасное объединение
            data={"username": user_email, "password": password},
        )
        return response.json()


async def register_user(user_email: str, password: str, name: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=f"{settings.BACKEND_API}users/create",
            json={"name": name, "password": password, "email": user_email},
            # headers={"Content-Type": "application/json"},
        )
        print(response.json(), 88888888888)
        return response.json()


async def get_user_info(access_token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=urljoin(settings.BACKEND_API, "auth/get-my-info"), headers={"Authorization": f"Bearer {access_token}"}
        )
        return response.json()


async def get_current_user_with_token(request: Request) -> dict:
    access_token = request.cookies.get("access_token")
    if not access_token:
        return {}
    user = await get_user_info(access_token)
    user["access_token"] = access_token
    return user


async def sell_buildings(
    user=Depends(get_current_user_with_token),
    main_image: UploadFile = File(),
    images: list[UploadFile] = File(None),
    title: str = Form(...),
    description: str = Form(...),
    type: str = Form(...),
    apartment_price: float = Form(...),
    address: str = Form(...),
    contact: str = Form(...),
):


    new_buildings_uuid = uuid.uuid4()
    main_image = await s3_storage.upload_new_buildings_image(main_image, new_buildings_uuid=new_buildings_uuid)
    images = images or []
    images_urls = []
    for image in images:
        url = await s3_storage.upload_new_buildings_image(image, new_buildings_uuid=new_buildings_uuid)
        images_urls.append(url)

    files = {
        "main_image": (main_image.filename, main_image.file, main_image.content_type),
    }

    files.update({f"images_{i}": (img.filename, img.file, img.content_type) for i, img in enumerate(images or [])})

    data = {
        "title": title,
        "description": description,
        "type": type,
        "apartment_price": str(apartment_price),
        "address": address,
        "contact": contact,
    }


    # Отправка данных на backend API
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=f"{settings.BACKEND_API}/sell_buildings",
            json={
                "title": title,
                "description": description,
                "type": type,
                "apartment_price": apartment_price,
                "address": address,
                "contact": contact,
                "main_image": main_image,
                "images": image_urls,
            },
            headers={"Authorization": f"Bearer {user.token}"}
        )

    return response.json()




class SortTypeByEnum(StrEnum):
    NEW_BUILDING = 'Новобудова'
    SECOND_OWNER = 'Вторинний ринок'
    FOR_RENT = 'Оренда'

async def get_building(pk: int) -> NewBuildingSchema:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.BACKEND_API}new_buildings/{pk}")
        response.raise_for_status()
        data = response.json()
        if "items" in data:
            building_data = data["items"][0]
        else:
            building_data = data
        return NewBuildingSchema(**building_data)


async def get_newBuildings(q: str = ""):
    async with httpx.AsyncClient() as client:
        response = await client.get(url=f"{settings.BACKEND_API}new_buildings/", params={"q": q})
        return response.json()



async def get_buildings_by_type(building_type: SortTypeByEnum, q: str = ""):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=f"{settings.BACKEND_API}new_buildings/",
            params={
                "type": building_type.value,  # передаем значение Enum как строку
                "q": q,
            },
        )
        return response.json()


async def get_new_buildings(q: str = ""):
    return await get_buildings_by_type(SortTypeByEnum.NEW_BUILDING, q)


async def get_second_owners(q: str = ""):
    return await get_buildings_by_type(SortTypeByEnum.SECOND_OWNER, q)


async def get_rents(q: str = ""):
    return await get_buildings_by_type(SortTypeByEnum.FOR_RENT, q)
