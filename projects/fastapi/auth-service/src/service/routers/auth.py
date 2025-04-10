from typing import Annotated, List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from service import serializers
from service.core.database import db_connection
from service.core.response import statusCodes
from service.services.auth import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)


@router.post("/login", response_model=serializers.UserAccess)
async def login(
    user_credentials: serializers.UserLogin,
    session=Depends(db_connection.get_async_session),
):
    """
    Login to the system. This will return a token that can be used to access the system.
    """

    auth_service = AuthService(session)
    user = await auth_service.login(
        email_address=user_credentials.email_address,
        password=user_credentials.password,
    )
    if not user:
        raise HTTPException(
            status_code=statusCodes.UNAUTHORIZED_401,
            detail="Invalid credentials",
        )
    return user


@router.post("/refresh", response_model=serializers.UserAccess)
async def refresh(
    refresh_token: serializers.UserRefresh,
    session=Depends(db_connection.get_async_session),
):
    """
    Refresh the access token.
    """

    auth_service = AuthService(session)
    user = await auth_service.refresh(refresh_token=refresh_token.refresh_token)
    if not user:
        raise HTTPException(
            status_code=statusCodes.UNAUTHORIZED_401,
            detail="Invalid refresh token",
        )
    return user
