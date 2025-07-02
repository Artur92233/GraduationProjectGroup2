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
    await admin_check(user)
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=f"{settings.BACKEND_API}/sell_buildings",
            json={
                "title": title,
                "description": description,
                "type": type,
                "price": price,
                "address": address,
                "contact": contact,
            },
            files={"main_image": main_image.file, **{
                f"images_{i}": img.file for i, img in enumerate(images or [])
            }},
            headers={"Authorization": f"Bearer {user.token}"}
        )

    return response.json()

async def get_building(pk: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=f'{settings.BACKEND_API}new_building/{pk}',
        )
        return response.json()



async def get_new_buildings(q: str = ""):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=f'{settings.BACKEND_API}new_buildings/',
            params={"q": q}

        )
        print(response.json(), 3333333333333333333333333)
        return response.json()
async def get_rents(q: str = ""):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=f'{settings.BACKEND_API}rent/',
            params={"q": q}

        )
        print(response.json(), 3333333333333333333333333)
        return response.json()

async def get_second_owners(q: str = ""):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=f'{settings.BACKEND_API}second_owner/',
            params={"q": q}

        )
        print(response.json(), 3333333333333333333333333)
        return response.json()