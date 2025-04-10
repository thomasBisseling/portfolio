import uuid
from datetime import datetime, timedelta

from sqlmodel import select, update

from service.core.models import Datetime
from service.core.service import Service
from service.models.user import User, UserRefreshToken
from service.security.jwt import jwt_decode
from service.security.password import generate_password_hash


class UserService(Service):
    model = User

    async def get_user_by_email_address(self, email_address: str):
        """
        Get a user by its email address.
        """
        stmt = select(User).where(User.email_address == email_address)
        result = await self.execute(stmt)
        user = result.scalar_one_or_none()
        return user

    async def get_user_by_token(self, token: str):
        """
        Get a user by its token.
        """

        decoded_token = jwt_decode(token)
        if not decoded_token:
            return None

        user_id = int(decoded_token.get("sub"))
        return await self.get_by_id(user_id)

    async def get_user_by_refresh_token(self, refresh_token: str):
        """
        Get a user by its refresh token.
        """
        stmt = (
            select(User)
            .join(UserRefreshToken)
            .where(UserRefreshToken.token == refresh_token)
        )
        result = await self.execute(stmt)
        user = result.scalar_one_or_none()
        return user

    async def update_user(self, user: User, user_update, **kwargs):
        """
        Update an existing user.
        """
        user_data = user_update.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(user, key, value)

        stmt = update(User).where(User.id == user.id).values(**user_data)
        await self.execute(stmt)

    async def set_password(self, user: User, password: str):
        """
        Set a user's password.
        """

        user.password = generate_password_hash(password)
        stmt = update(User).where(User.id == user.id).values(password=user.password)
        return await self.execute(stmt)

    async def invoke_refresh_token(self, refresh_token: str):
        """
        Invalidate a refresh token.
        """

        stmt = select(UserRefreshToken).where(UserRefreshToken.token == refresh_token)
        result = await self.execute(stmt)
        await self.delete(result)

    async def set_refresh_token(self, user: User):
        """
        Generate a new refresh token for a user.
        """
        now: Datetime | datetime = datetime.now()
        expires_at: Datetime = now + timedelta(days=2)
        token = str(uuid.uuid4())
        refresh_token = UserRefreshToken(
            user_id=user.id,
            token=token,
            created_at=now,
            expires_at=expires_at,
        )
        self.session.add(refresh_token)
        await self.session.commit()
        return refresh_token
