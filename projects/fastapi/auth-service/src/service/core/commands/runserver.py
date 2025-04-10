import uvicorn as uv

from service.core.cli import BaseCommand
from service.core.settings import settings


class Command(BaseCommand):
    # requires_migrations_checks = True

    def add_arguments(self, parser):
        """
        Add arguments to the command
        """
        parser.add_argument("--file", type=str, default="service")
        parser.add_argument("--host", type=str, default="127.0.0.1")
        parser.add_argument("--port", type=int, default=8000)
        parser.add_argument("--reload", action="store_true", default=False)
        parser.add_argument(
            "--proxy-headers",
            action="store_true",
            default=False,
        )

    def handle(self, **options):
        """
        Run the server
        """
        self.stdout.write(
            "Running server on {}:{}".format(options["host"], options["port"])
        )

        file = options.pop("file")
        uv.run(
            f"{file}:app",
            host=options["host"],
            port=options["port"],
            reload=options["reload"],
            proxy_headers=options["proxy_headers"],
            reload_dirs=[settings.project_path],
            reload_excludes=["*/migrations/*", "*/tests/*", "*/commands/*"],
        )
