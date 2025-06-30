from urllib.parse import urljoin

import httpx
from fastapi import Request, UploadFile, Body
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




# async def create_product(main_image: UploadFile,
#     images: list[UploadFile] = None,
#     title: str = Body(max_length=100),
#     description: str = Body(max_length=1000),
#     type: # str = Body(max_length=50),
#     price: float = Body(gt=1),
#     address: str = Body(max_length=200),
#     contact: str = Body(max_length=100)):
#     async with httpx.AsyncClient as client:
#         response = await client.post(
#              url=f'{settings.BACKEND_API}sell_buildings',
#              params={'main_image': main_image,
#                      'images': images,
#                      'title': title,
#                      'description': description,
#                       type: # type
#                      }
#         )
#
#         print(response.json(), 55555555555555)
#     return response.json()