from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    bcrypt__default_rounds=14,
    bcrypt__min_rounds=14,
    bcrypt__max_rounds=18,
    bcrypt__salt_size=22,
)


def generate_password_hash(password: str) -> str:
    """
    Generate a password hash.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.
    """

    # Check if the hashed password is in the correct format
    if not pwd_context.identify(hashed_password):
        return False
    # Verify the password
    return pwd_context.verify(plain_password, hashed_password)
