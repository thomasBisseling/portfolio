from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "service.apps.core"
    label = "core"

    def ready(self):
        try:
            from . import signals  # noqa F401
        except ImportError:
            pass
