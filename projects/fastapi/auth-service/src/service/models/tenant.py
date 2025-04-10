from sqlmodel import (
    Field,
)

from service.core.models import BaseSQLModel, Datetime


class Tenant(BaseSQLModel, table=True):
    """
    Tenant model for the application.
    """

    owner_email_address: str = Field(
        unique=True,
        index=True,
        nullable=False,
    )
    name: str = Field(nullable=False)
    description: str = Field(nullable=True)
    created_at: Datetime = Field(nullable=False)
    is_active: bool = Field(default=False)
    is_verified: bool = Field(default=False)
    owner_id: int = Field(
        foreign_key="user.id",
        nullable=False,
        index=True,
        unique=True,
        ondelete="CASCADE",
    )


class TenantUser(BaseSQLModel, table=True):
    """
    Tenant user model for the application.
    """

    tenant_id: int = Field(foreign_key="tenant.id", nullable=False, ondelete="CASCADE")
    user_id: int = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
    is_active: bool = Field(default=False)
    is_verified: bool = Field(default=False)
