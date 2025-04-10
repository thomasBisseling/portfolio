import datetime
from datetime import datetime, timedelta

from sqlmodel import select, update

from service.core.service import Service
from service.models.user import User, UserRefreshToken
from service.security.jwt import jwt_encode
from service.security.password import verify_password
from service.services.user import UserService


class AuthService(Service):
    def __init__(self, session):
        super().__init__(session, True)
        self.user_service = UserService(session)

    async def login(self, email_address, password):
        user = await self.user_service.get_user_by_email_address(email_address)
        if user and verify_password(password, user.password):
            # Generate a new access token and refresh token
            refresh_token = await self.user_service.set_refresh_token(user)
            expires_at = datetime.utcnow() + timedelta(minutes=15)
            access_token = jwt_encode(
                user_id=user.id,
                expires_at=expires_at,
            )

            return {
                "access_token": access_token,
                "refresh_token": refresh_token.token,
                "expires_at": refresh_token.expires_at.isoformat(),
            }
        return None

    async def register(self, email_address, password, first_name, last_name):
        """
        Register a new user.
        :param email_address:
        :param password:
        :param first_name:
        :param last_name:
        :return:
        """
        if await self.user_service.get_user_by_email_address(email_address):
            return None
        return self.user_service.create(
            {
                "email_address": email_address,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
            }
        )

    async def register_user_by_invitation(
        self, email_address, first_name, last_name, tenant_id
    ):
        """
        Register a new user by invitation.
        Password must be set by the user. When the user clicks on the link in the email,
        :param email_address:
        :param first_name:
        :param last_name:
        :param tenant_id:
        :return:
        """

        if await self.user_service.get_user_by_email_address(email_address):
            return None
        return self.user_service.create(
            {
                "email_address": email_address,
                "first_name": first_name,
                "last_name": last_name,
                "tenant_id": tenant_id,
            }
        )

    async def reset_password(self, email_address, new_password):
        user = await self.user_service.get_user_by_email_address(email_address)
        if user:
            await user.set_password(new_password)
            return True
        return False

    async def logout(self, token):
        user = await self.user_service.get_user_by_token(token)
        if user:
            user.invalidate_token(token)
            return True
        return False

    async def verify_token(self, token):
        user = await self.user_service.get_user_by_token(token)
        if user:
            return True
        return False

    async def get_refresh_token_object(self, refresh_token: str):
        """
        Get a refresh token object by its token.
        """
        stmt = select(UserRefreshToken).where(UserRefreshToken.token == refresh_token)
        result = await self.execute(stmt)
        return result.scalar_one_or_none()

    async def refresh(self, refresh_token: str):
        _refresh_token = await self.get_refresh_token_object(refresh_token)
        if _refresh_token:
            # Generate a new access token and refresh token
            expires_at = datetime.utcnow() + timedelta(minutes=15)
            access_token = jwt_encode(
                user_id=_refresh_token.user_id,
                expires_at=expires_at,
            )
            return {
                "access_token": access_token,
                "refresh_token": _refresh_token.token,
                "expires_at": _refresh_token.expires_at.isoformat(),
            }
        return None
