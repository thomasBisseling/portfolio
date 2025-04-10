from sqlmodel import SQLModel


class UserDetail(SQLModel):
    id: str | int
    first_name: str | None
    last_name: str | None
    email_address: str | None
    password: str | None
    created_at: str | None
    blocked: bool | None
    is_active: bool | None
    last_login: str | None
    is_verified: bool | None
    is_superuser: bool | None
    is_staff: bool | None


class UserCreate(SQLModel):
    email_address: str
    password: str
    password_confirmation: str


class UserUpdate(SQLModel):
    email_address: str | None
    first_name: str | None
    last_name: str | None


class UserPasswordChange(SQLModel):
    old_password: str
    new_password: str
    new_password_confirmation: str


class UserPasswordUpdate(SQLModel):
    password: str
    password_confirmation: str


class UserLogin(SQLModel):
    email_address: str
    password: str


class UserAccess(SQLModel):
    access_token: str
    expires_at: str
    refresh_token: str


class UserRefresh(SQLModel):
    refresh_token: str
