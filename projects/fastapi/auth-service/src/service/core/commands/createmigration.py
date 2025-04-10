import os
import subprocess  # nosec

from service.core.cli import BaseCommand
from service.core.settings import settings


class Command(BaseCommand):
    """
    Command to create migrations for the project
    """

    def add_arguments(self, parser):
        """
        Add arguments to the command
        """

        parser.add_argument("--message", type=str, default="auto")
        parser.add_argument(
            "--dry-run", action="store_true"
        )  # Dry run option to check if migrations are needed

    def get_alembic_migrations_path(self):
        """
        Get the path to the alembic migrations folder
        """

        alembic_ini = os.path.join(str(settings.base_path), "alembic.ini")
        if not os.path.exists(alembic_ini):
            return self.stderr.write(
                self.stderr.style(
                    f"Alembic configuration file not found at {alembic_ini}",
                    color=self.colors.RED,
                )
            )

        with open(alembic_ini, "r") as f:
            alembic_ini_content = f.read()

        for line in alembic_ini_content.split("\n"):
            if line.startswith("script_location"):
                return os.path.join(str(settings.base_path), line.split(" = ")[1])
        return self.stderr.write(
            self.stderr.style(
                "script_location not found in alembic.ini",
                color=self.colors.RED,
            )
        )

    def get_revision_number(self):
        """
        Get the revision number
        """

        alembic_versions_path = os.path.join(
            self.get_alembic_migrations_path(), "versions"
        )
        if not os.listdir(alembic_versions_path):
            return "0001"

        files = os.listdir(alembic_versions_path)
        migration_files = []

        for file in files:
            if file.endswith(".py") and file.split("_")[0].isdigit():
                migration_files.append(file)

        migration_files.sort()
        last_file = migration_files[-1]
        last_file_number = int(last_file.split("_")[0])

        return str(last_file_number + 1).zfill(4)

    def model_changes_found(self):
        """
        Check if the models have changed
        """

        result = self.shell_exec(
            [
                "alembic",
                "check",
            ],
        )

        return "no changes detected" not in result.stdout

    def create_migration(self, message):
        """
        Create a migration file
        """

        revision_number = self.get_revision_number()
        if revision_number == "0001":
            message = "initial"
            self.stdout.write(
                self.stdout.style(
                    "Creating initial migration",
                    color=self.colors.YELLOW,
                )
            )

        result = self.shell_exec(
            [
                "alembic",
                "revision",
                "--autogenerate",
                "-m",
                message,
                "--rev-id",
                revision_number,
            ]
        )

        if not result.returncode == 0:
            return self.stdout.write(
                self.stdout.style(
                    f"Migrations creation failed: {result.stderr}",
                    color=self.colors.RED,
                )
            )

        if "Target database is not up to date." in result.stdout:
            return self.stdout.write(
                self.stdout.style(
                    "Target database is not up to date, run 'python main.py migrate'",
                    color=self.colors.RED,
                )
            )

        if "FAILED" in result.stdout:
            reason = result.stdout.split("  FAILED: ")[1].lower()
            return self.stdout.write(
                self.stdout.style(
                    f"Migrations creation failed: {reason}",
                    color=self.colors.RED,
                )
            )

        alembic_migrations_path = self.get_alembic_migrations_path()
        versions_path = os.path.join(alembic_migrations_path, "versions")
        files = os.listdir(versions_path)
        for file in files:
            if file.startswith(revision_number):
                return self.stdout.write(
                    self.stdout.style(
                        f"New migration created: {revision_number}_{message.lower()}",
                        color=self.colors.GREEN,
                    )
                )

    def handle(self, **options):
        """
        Execute the command
        """

        if options["dry_run"]:
            if self.migration_required():
                return self.stdout.write("Migrations are needed")
            else:
                return self.stdout.write("No migrations needed")

        if not self.migration_required():
            return self.stdout.write("No changes detected, cannot create migrations")

        if self.model_changes_found():  # Check if the models have changed
            return self.create_migration(options["message"])
