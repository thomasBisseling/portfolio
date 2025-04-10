from datetime import datetime, timedelta

import factory

from service.core.database import db_connection
from service.models.user import User
from service.security.password import generate_password_hash


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = db_connection.get_sync_session()
        sqlalchemy_session_persistence = "commit"


class UserFactory(BaseFactory):
    class Meta:
        model = User  # Replace with your actual User model

    email_address = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    created_at = factory.LazyFunction(datetime.utcnow)
    is_active = True
    blocked = False
    is_verified = True
    is_superuser = False
    is_staff = False

    @classmethod
    def create(cls, **kwargs):
        """
        Override the create method to hash the password before saving the user.
        """
        if "password" in kwargs:
            kwargs["password"] = generate_password_hash(kwargs["password"])
        return super().create(**kwargs)
