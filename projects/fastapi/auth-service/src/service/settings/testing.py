from .development import Settings as BaseSettings
from decouple import config as d_config

class Settings(BaseSettings):
    """
    Server testing settings.
    """

    db_port = d_config("DB_PORT", cast=int, default=7432)
    db_name = "service_test"
    release_version = "1.0.0"
    commit_hash = "testhash"