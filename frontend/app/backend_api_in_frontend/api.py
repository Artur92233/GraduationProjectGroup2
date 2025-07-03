from enum import StrEnum
from urllib.parse import urljoin

import httpx
from fastapi import Request, UploadFile, Body, File, Depends

from settings import settings

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
    main_image: UploadFile = File(...),
    images: list[UploadFile] = File(None),
    title: str = Body(..., max_length=100),
    description: str = Body(..., max_length=1000),
    type: str = Body(..., max_length=50),
    price: float = Body(..., gt=1),
    address: str = Body(..., max_length=200),
    contact: str = Body(..., max_length=100),
):
    files = {
        "main_image": (
            getattr(main_image, "filename", "main_image.png"),
            getattr(main_image, "file", main_image),
            getattr(main_image, "content_type", "application/octet-stream"),
        )
    }

    if images:
        if not isinstance(images, list):
            images = [images]  # Оборачиваем в список, если это одиночный файл
        for i, img in enumerate(images):
            files[f"images_{i}"] = (
                getattr(img, "filename", f"image_{i}.png"),
                getattr(img, "file", img),
                getattr(img, "content_type", "application/octet-stream"),
            )

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=f"{settings.BACKEND_API}/sell_buildings",
            data={
                "title": title,
                "description": description,
                "type": type,
                "price": price,
                "address": address,
                "contact": contact,
            },
            files=files,
            headers={"Authorization": f"Bearer {user.token}"}
        )

    return response.json()

async def get_building(pk: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=f'{settings.BACKEND_API}new_building/{pk}',
        )
        return response.json()



class SortTypeByEnum(StrEnum):
    NEW_BUILDING = 'Новобудова'
    SECOND_OWNER = 'На вторинному ринку'
    FOR_RENT = 'На оренду'


async def get_buildings_by_type(building_type: SortTypeByEnum, q: str = ""):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=f"{settings.BACKEND_API}new_buildings/",
            params={
                "type": building_type.value,  # передаем значение Enum как строку
                "q": q,
            }
        )
        return response.json()


async def get_new_buildings(q: str = ""):
    return await get_buildings_by_type(SortTypeByEnum.NEW_BUILDING, q)

async def get_second_owners(q: str = ""):
    return await get_buildings_by_type(SortTypeByEnum.SECOND_OWNER, q)

async def get_rents(q: str = ""):
    return await get_buildings_by_type(SortTypeByEnum.FOR_RENT, q)