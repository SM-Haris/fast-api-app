from uuid import UUID
from typing import List

from fastapi import APIRouter, HTTPException, Request, status, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.shared_utils.auth_utils import create_access_token
from app.users.models import User
from app.database import get_session
from app.users.schemas import (
    UserCreateModel,
    UserLoginModel,
    UserResponseModel,
    UserUpdateModel,
)
from app.users.services import UserService

user_router = APIRouter()


@user_router.post(
    "/signup", response_model=UserResponseModel, status_code=status.HTTP_201_CREATED
)
async def signup(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    db_user = await UserService.get_user_by_email(user_data.email, session)
    if db_user:
        print(db_user)
        raise HTTPException(status_code=400, detail="User is already registered")
    user = await UserService.create_user(user_data, session)
    return user


@user_router.post("/login")
async def login(
    user_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    user = await UserService.login_user(user_data, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.get("/me", response_model=UserResponseModel | None)
async def fetch_me(request: Request, session: AsyncSession = Depends(get_session)):
    user = await UserService.get_user_by_email(request.state.user_email, session)
    if user:
        return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@user_router.delete("/{user_id}")
async def delete_user(user_id: UUID, session: AsyncSession = Depends(get_session)):
    user = await UserService.delete_user(user_id, session)
    if user:
        return {"detail": "User deleted"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@user_router.patch("/{user_id}")
async def update(
    user_id: UUID,
    user_data: UserUpdateModel,
    session: AsyncSession = Depends(get_session),
):
    user = await UserService.update_user(user_id, user_data, session)
    if user:
        return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@user_router.get("/{user_id}", response_model=UserResponseModel | None)
async def get_user(user_id: UUID, session: AsyncSession = Depends(get_session)):
    user = await UserService.get_user(user_id, session)
    if user:
        return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@user_router.get("/", response_model=List[UserResponseModel | None])
async def get_all_users(session: AsyncSession = Depends(get_session)):
    user = await UserService.get_all_users(session)
    return user
