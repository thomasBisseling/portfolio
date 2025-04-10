import os

from vitaleey.core.utils import get_redis_location

from .base import *  # noqa
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "CONN_MAX_AGE": 600,
        "DISABLE_SERVER_SIDE_CURSORS": True, # Disable server-side cursors for PgBouncer
        "NAME": os.getenv("POSTGRES_DB", "service-plan"),
        "USER": os.getenv("POSTGRES_USER", "service-plan"),
        "HOST": os.getenv("POSTGRES_HOST", "db"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
        "PASSWORD": get_secret(
            os.getenv("POSTGRES_PASSWORD_FILE", "/run/secrets/db_password"),
            "service_plan"
        ),
    }
}

REDIS = {
    "HOST": os.getenv("REDIS_HOST", "redis"),
    "PORT": os.getenv("REDIS_PORT", "6379"),
    "USERNAME": os.getenv("REDIS_USERNAME", "service-plan"),
    "PASSWORD": get_secret(
            os.getenv("REDIS_PASSWORD_FILE", "/run/secrets/redis_password"),
            "service_plan"
        ),
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": get_redis_location(),
    }
}
