from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from applications.auth.password_handler import PasswordEncrypt
from applications.users.models import User


async def create_user_in_db(email, name, password, session: AsyncSession) -> User:
    hashed_password = await PasswordEncrypt.get_password_hash(password)
    new_user = User(email=email, hashed_password=hashed_password, name=name)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def get_user_by_email(email, session: AsyncSession) -> User | None:
    query = select(User).filter(User.email == email)
    result = await session.execute(query)
    return result.scalar_one_or_none()
