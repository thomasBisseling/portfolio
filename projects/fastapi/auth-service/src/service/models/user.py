from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import (
    Field,
    UniqueConstraint,
    select,
)

from service.core.models import BaseSQLModel, Datetime
from service.security.password import generate_password_hash, verify_password


class User(BaseSQLModel, table=True):
    """
    User model for the application.

    Superuser and staff users are only for internal use. Not for tenant use.
    """

    email_address: str = Field(
        unique=True,
        index=True,
        nullable=False,
    )
    first_name: str = Field(nullable=True)
    last_name: str = Field(nullable=True)
    password: str = Field(nullable=True)
    created_at: Datetime = Field(nullable=False)
    blocked: bool = Field(default=False)
    is_active: bool = Field(default=False)
    last_login: Datetime = Field(nullable=True)
    is_verified: bool = Field(default=False)
    is_superuser: bool = Field(default=False)
    is_staff: bool = Field(default=False)

    async def _get(self, session: AsyncSession):
        """
        Get the user from the database.
        """
        stmt = select(User).where(User.id == self.id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        return user

    async def set_password(self, session: AsyncSession, password: str):
        """
        Set the user's password after hashing it.
        """
        # This should be replaced with a proper password hashing method
        self.password = generate_password_hash(password)
        obj = await self._get(session)
        if obj:
            obj.password = self.password
            await session.commit()
            await session.refresh(obj)

        return user

    def full_name(self):
        """
        Returns the full name of the user.
        """
        return f"{self.first_name} {self.last_name}"


class UserRefreshToken(BaseSQLModel, table=True):
    """
    User refresh token model for the application.

    Tokens used for refreshing access tokens.
    """

    user_id: int = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
    token: str = Field(nullable=False)
    created_at: Datetime = Field(nullable=False)
    expires_at: Datetime = Field(nullable=False)

    __table_args__ = (UniqueConstraint("user_id", "token"),)


class PasswordReset(BaseSQLModel, table=True):
    """
    Password reset model for the application.
    """

    user_id: int = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
    token: str = Field(nullable=False)
    created_at: Datetime = Field(nullable=False)
    expires_at: Datetime = Field(nullable=False)
