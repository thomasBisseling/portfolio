from service.core.cli import BaseCommand
from service.core.settings import settings


class Command(BaseCommand):
    """
    Command to migrate the model changes to the database
    """

    def add_arguments(self, parser):
        """
        Add arguments to the command
        """

        parser.add_argument(
            "--silent",
            action="store_true",
            default=False,
            help="Do not print any output",
        )
        parser.add_argument("--all", action="store_true", default=False)

    def are_migration_files_present(self):
        """
        Check if there are any migrations
        """

        result = self.shell_exec(
            [
                "alembic",
                "current",
            ],
        )

        return "no revisions are present" not in result.stdout

    def are_new_migration_files_present(self):
        """
        Check if there are any new migrations
        """

        result = self.shell_exec(
            [
                "alembic",
                "heads",
            ],
        )

        print(result.stdout)

        return "no heads" not in result.stdout.lower()

    def handle(self, **options):
        if not options["silent"]:
            self.stdout.write("Migrating the database")
        if not self.are_migration_files_present():
            if not options["silent"]:
                self.stdout.write(
                    "No migrations present, run 'python main.py createmigration'"
                )
                self.stdout.write(
                    self.stdout.style(
                        "No migrations present, run 'python main.py createmigration'",
                        color=self.colors.YELLOW,
                    )
                )
            return

        if not self.are_new_migration_files_present():
            if not options["silent"]:
                self.stdout.write("No new migrations present")
                self.stdout.write(
                    self.stdout.style(
                        "No new migrations present",
                        color=self.colors.YELLOW,
                    )
                )
            return

        result = self.shell_exec(
            [
                "alembic",
                "upgrade",
                "head",
            ]
        )

        if not result.returncode == 0:
            if not options["silent"]:
                self.stdout.write(
                    self.stdout.style("Migration failed", color=self.colors.RED)
                )
            raise Exception(result.stderr)

        if not options["silent"]:
            return self.stdout.write(
                self.stdout.style("Migration succeed", color=self.colors.GREEN)
            )
