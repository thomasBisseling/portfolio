from datetime import datetime, timedelta
from typing import Any

from jose import JWTError, jwt
from sqlalchemy.sql.annotation import Annotated

from service.core.settings import settings

ALGORITHM = "HS256"
AUDIENCE = "forraad-hub"
ISSUER = "auth-service-forraad-hub"


def jwt_encode(user_id: int, expires_at: datetime) -> str:
    """
    Encode a dictionary into a JWT token.
    """
    data = {
        "sub": str(user_id),  # Subject (user ID)
        "exp": int(expires_at.timestamp()),  # Expiration time
        "iat": int(datetime.utcnow().timestamp()),  # Issued at
        "iss": ISSUER,  # Issuer of the token
        "aud": AUDIENCE,  # Audience
        "nbf": int((datetime.utcnow()).timestamp()),  # Not before
    }
    return jwt.encode(data, settings.secret_key, algorithm=ALGORITHM)


def jwt_decode(token: str) -> dict[str, Any] | None:
    """
    Decode a JWT token into a dictionary.
    """

    payload = jwt.decode(
        token,
        settings.secret_key,
        algorithms=[ALGORITHM],
        issuer=ISSUER,
        audience=AUDIENCE,
    )
    if payload:
        payload.update(
            {
                "exp": datetime.fromtimestamp(payload.get("exp")),
                "iat": datetime.fromtimestamp(payload.get("iat")),
                "nbf": datetime.fromtimestamp(payload.get("nbf")),
            }
        )
    return payload
