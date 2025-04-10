"""
Django settings for service project.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
from pathlib import Path

def get_secret(secret_path, fallback=None):
    if not os.path.exists(secret_path):
        return fallback
    return Path(secret_path).read_text().strip()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret(os.getenv("SECRET_KEY_FILE", "/run/secrets/secret_key"), "secret_key")

# Build paths inside the project like this: PROJECT_DIR / 'subdir'.
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Application definition
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "taggit",
    "rest_framework",
    # "guardian",
    "drf_yasg",
    "vitaleey.core",
    "service.apps.core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.RemoteUserMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "service.wsgi.application"

ROOT_URLCONF = "service.urls"

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# JavaScript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/3.1/ref/contrib/staticfiles/#manifeststaticfilesstorage
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

STATICFILES_DIRS = []

STATIC_ROOT = os.path.join(PROJECT_DIR, "public", "static")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(PROJECT_DIR, "public", "media")
MEDIA_URL = "/media/"

LOGIN_URL = "/login"
LOGIN_EXEMPT_URLS = ["/logout", MEDIA_URL]

CORS_ORIGIN_WHITELIST = ["http://localhost:3000"]

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

REST_FRAMEWORK = {
    "DEFAULT_PAGE_SIZE": {
        "SMALL": 10,
        "MEDIUM": 25,
        "LARGE": 50,
        "EXTRA_LARGE": 100,
    },
}

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
    "django.contrib.auth.backends.RemoteUserBackend",
)

APPEND_SLASH = False

SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "DEFAULT_INFO": "vitaleey.docs.openapi_info",
    "SECURITY_DEFINITIONS": {
        "JWT": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
}

REDOC_SETTINGS = {
    "HIDE_HOSTNAME": True,
}

GUARDIAN_RAISE_403 = True
ANONYMOUS_USER_NAME = None

BMR_CALCULATION_BOUNDARIES = {
    "weight": [40, 300],
    "height": [130, 240],
    "age": [15, 80],
}

JWT_AUTH = {
    "JWT_PAYLOAD_GET_USERNAME_HANDLER": "vitaleey.core.utils.jwt_get_username_from_payload_handler",
    "JWT_DECODE_HANDLER": "vitaleey.core.utils.jwt_decode_token",
    "JWT_ALGORITHM": "RS256",
    "JWT_AUDIENCE": "https://api.vitaleey.com",
    "JWT_ISSUER": "https://vitaleey.eu.auth0.com/",
    "JWT_AUTH_HEADER_PREFIX": "Bearer",
}
