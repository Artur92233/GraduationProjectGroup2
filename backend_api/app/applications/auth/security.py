from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from applications.auth.auth_handler import auth_handler
from applications.users.crud import get_user_by_email
from applications.users.models import User
from database.session_dependencies import get_async_session


class SecurityHandler:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    token: str = Depends(SecurityHandler.oauth2_scheme),
    session: AsyncSession = Depends(get_async_session),
) -> User:
    payload = await auth_handler.decode_token(token)
    user = await get_user_by_email(payload["user_email"], session)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
