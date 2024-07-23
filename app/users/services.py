from datetime import datetime
from uuid import UUID

from sqlalchemy import desc, update, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import User
from app.users.schemas import UserCreateModel, UserLoginModel, UserUpdateModel
from app.users.helpers import PasswordHelper


class UserService:

    @classmethod
    async def get_all_users(self, session: AsyncSession):
        statement = select(User).order_by(desc(User.created_at))
        result = await session.execute(statement)
        return result.scalars().all()

    @classmethod
    async def get_user(self, user_id: UUID, session: AsyncSession):
        statement = select(User).where(User.id == user_id)
        result = await session.execute(statement)
        return result.scalar()

    @classmethod
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.execute(statement)
        return result.scalar()

    @classmethod
    async def login_user(self, user_data: UserLoginModel, session: AsyncSession):
        statement = select(User).where(User.email == user_data.email)
        result = await session.execute(statement)
        user = result.scalar()
        if not user:
            return False
        if not PasswordHelper.verify_password(user_data.password, user.password):
            return False
        return user

    @classmethod
    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data.password = PasswordHelper.hash_password(password=user_data.password)
        new_user = User(**user_data.model_dump())
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

    @classmethod
    async def update_user(
        self, user_id: UUID, user_data: UserUpdateModel, session: AsyncSession
    ):
        user_dict = user_data.model_dump(exclude_unset=True)
        user_dict["updated_at"] = datetime.now()

        if user_data.password:
            user_dict["password"] = PasswordHelper.hash_password(user_data.password)

        statement = (
            update(User)
            .where(User.id == user_id)
            .values(**user_dict)
            .execution_options(synchronize_session="fetch")
        )

        await session.execute(statement)
        await session.commit()
        return user_data

    @classmethod
    async def delete_user(self, user_id: UUID, session: AsyncSession):
        user = await self.get_user(user_id, session)
        if user is not None:
            await session.delete(user)
            await session.commit()
            return user
        return None
