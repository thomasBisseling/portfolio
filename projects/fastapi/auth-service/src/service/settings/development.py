from .base import Settings as BaseSettings


class Settings(BaseSettings):
    """
    Server development settings.
    """

    secret_key = "bert_en_ernie"
