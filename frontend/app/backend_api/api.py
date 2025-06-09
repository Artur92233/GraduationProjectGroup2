import httpx
from settings import settings
from fastapi import Request
from urllib.parse import urljoin

async def login_user(user_email: str, password: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=urljoin(settings.BACKEND_API, "auth/login"),  # Безопасное объединение
            data={"username": user_email, "password": password}
        )
        return response.json()

async def register_user(user_email: str, password: str, name: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=f'{settings.BACKEND_API}users/create',
            json={"name": name, 'password': password, "email": user_email},
            headers={'Content-Type': 'application/json'}

        )
        print(response.json(), 88888888888)
        return response.json()


async def get_user_info(access_token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=urljoin(settings.BACKEND_API, "auth/get-my-info"),
            headers={"Authorization": f'Bearer {access_token}'}
        )
        return response.json()

async def get_current_user_with_token(request: Request) -> dict:
    access_token = request.cookies.get('access_token')
    if not access_token:
        return {}
    user = await get_user_info(access_token)
    user['access_token'] = access_token
    return user
