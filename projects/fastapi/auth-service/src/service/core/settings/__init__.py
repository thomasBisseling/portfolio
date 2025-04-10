import importlib
import os

__all__ = ["settings"]


class Settings:
    """
    Settings class to load the settings module.
    """

    def __init__(self):
        self.settings_path = os.getenv("API_SETTINGS_MODULE", "service.settings")
        self._settings = None

    def get_settings(self):
        """
        Get the settings module.
        """
        if self._settings is None:
            try:
                module = importlib.import_module(self.settings_path)
                if "Settings" not in dir(module):
                    raise ImportError(
                        f"Settings module '{self.settings_path}' does not have a 'Settings' class."
                    )
                self._settings = module.Settings()
            except ImportError as e:
                raise ImportError(
                    f"Could not import settings module '{self.settings_path}'."
                ) from e
        return self._settings

    def __getattr__(self, name):
        return getattr(self.get_settings(), name)

    def __contains__(self, name):
        return hasattr(self.get_settings(), name)

    def __call__(self, *args, **kwargs):
        return self.get_settings()


settings = Settings()
