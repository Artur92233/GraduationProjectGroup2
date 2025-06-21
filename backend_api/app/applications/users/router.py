import uuid

from applications.services.rabbit.constants import SupportedQueues
from applications.services.rabbit.rabbitmq_service import rabbitmq_broker
from applications.users.crud import activate_user_account, create_user_in_db, get_user_by_email
from applications.users.schemas import BaseFields, BaseUserInfo, RegisterUserFields
from database.session_dependencies import get_async_session
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

router_users = APIRouter()


@router_users.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(
    request: Request,
    new_user: RegisterUserFields,
    background_task: BackgroundTasks,
    session: AsyncSession = Depends(get_async_session),
) -> BaseUserInfo:
    user = await get_user_by_email(new_user.email, session)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already exists")

    created_user = await create_user_in_db(new_user.email, new_user.name, new_user.password, session)
    background_task.add_task(
        rabbitmq_broker.send_message,
        message={
            "name": created_user.name,
            "email": created_user.email,
            "redirect_url": str(request.url_for("verify_user", user_uuid=created_user.uuid_data)),
        },
        queue_name=SupportedQueues.USER_REGISTRATION,
    )

    return created_user


@router_users.get("/verify/{user_uuid}")
async def verify_user(user_uuid: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    await activate_user_account(user_uuid, session)
    return {"Status": "activated"}
