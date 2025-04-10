from pathlib import Path

from decouple import config as d_config

from service.core.settings.default import BaseSettings, read_secret_file


class Settings(BaseSettings):
    """Server config settings."""

    project_path = Path(__file__).resolve().parent.parent
    base_path = project_path.parent

    # App settings
    app_list = ["service", "service.core"]

    # Database Engine settings
    db_port: int = 5432
    db_name: str = d_config("DB_NAME", default="plan_service")
    db_user: str = d_config("DB_USER", default="service-plan")
    db_password: str = d_config("DB_PASSWORD", default="service_plan")
    db_engine: str = "postgresql"
    public_routes = [
        "/auth/login",
        "/auth/register",
        "/auth/verify",
        "/auth/refresh",
        "/auth/reset-password",
    ]
