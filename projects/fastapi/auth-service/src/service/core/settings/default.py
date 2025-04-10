from decouple import config as d_config

__all__ = ["BaseSettings"]


def read_secret_file(secret_file: str) -> str:
    with open(secret_file) as f:
        return f.read().strip()


class BaseSettings:
    """Server config settings."""

    release_version: str = d_config("RELEASE_VERSION", default="0.1.0")
    root_url: str = d_config("ROOT_URL", default="http://localhost:8080")

    # App settings
    app_list = []

    # Database Engine settings
    db_engine: str = d_config("DB_ENGINE", default="postgresql")
    db_host: str = d_config("DB_HOST", default="localhost")
    db_port: int = d_config("DB_PORT", cast=int, default=5432)
    db_name: str = d_config("DB_NAME", default="postgres")
    db_user: str = d_config("DB_USER", default="postgres")
    db_password: str = d_config("DB_PASSWORD", default="postgres")
    db_pool_size: int = d_config("DB_POOL_SIZE", cast=int, default=5)
    db_max_overflow: int = d_config("DB_MAX_OVERFLOW", cast=int, default=10)
    db_pool_timeout: int = d_config("DB_POOL_TIMEOUT", cast=int, default=30)
    db_sql_log: bool = d_config("DB_SQL_LOG", cast=bool, default=False)
    db_url: str = d_config("DB_URL", default=None)

    # Security settings
    secret_key: str = d_config("SECRET_KEY", default=None)
