from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from applications.users.crud import create_user_in_db
from applications.users.schemas import BaseFields, RegisterUserFields
from database.session_dependencies import get_async_session

router_users = APIRouter()


@router_users.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(new_user: RegisterUserFields, session: AsyncSession = Depends(get_async_session)) -> BaseFields:
    await create_user_in_db(new_user.email, new_user.name, new_user.password, session)
    return new_user
