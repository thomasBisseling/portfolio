from datetime import datetime

import pytest

from service.core.settings import settings
from service.factories import UserFactory
from service.models.user import User
from service.security.jwt import AUDIENCE, ISSUER, jwt_decode
from service.services.user import UserService

pytestmark = pytest.mark.asyncio


@pytest.fixture
def is_access_token_valid():
    """
    Fixture to check if the access token is valid.
    """

    def _is_access_token_valid(data: dict, user: User):
        """
        Check if the access token is valid.
        :param token: Access token
        :return: True if valid, False otherwise
        """

        expires_at = data["expires_at"]
        datatime_expires_at = datetime.fromisoformat(expires_at)
        assert (
            datatime_expires_at > datetime.now()
        ), "Refresh token should not be expired"

        jwt_access_token = jwt_decode(data["access_token"])

        return all(
            [
                "access_token" in data,
                jwt_access_token["sub"] == str(user.id),
                jwt_access_token["exp"] > datetime.now(),
                jwt_access_token["iss"] == ISSUER,
                jwt_access_token["aud"] == AUDIENCE,
                jwt_access_token["nbf"] < datetime.now(),
                jwt_access_token["iat"] < datetime.now(),
            ]
        )

    return _is_access_token_valid


async def test_auth_login(client, is_access_token_valid):
    """
    Test the login endpoint with valid credentials.
    """

    password = "admin"
    user = UserFactory(password=password)

    # Test login endpoint
    response = client.post(
        "/api/auth/login",
        json={
            "email_address": user.email_address,
            "password": password,
        },
    )

    # Verify results
    assert response.status_code == 200

    data = response.json()
    assert is_access_token_valid(data, user)

    # Test user not found
    response = client.post(
        "/api/auth/login",
        json={
            "email_address": "a@a.com",
            "password": "123",
        },
    )
    assert response.status_code == 401


async def test_auth_refresh(client, db_session, is_access_token_valid):
    """
    Test the refresh endpoint with valid credentials.
    """

    user = UserFactory()
    user_service = UserService(db_session)
    refresh_token = await user_service.set_refresh_token(user)

    # Test refresh endpoint
    response = client.post(
        "/api/auth/refresh",
        json={
            "refresh_token": refresh_token.token,
        },
    )

    # Verify results
    assert response.status_code == 200
    data = response.json()

    assert is_access_token_valid(data, user)
