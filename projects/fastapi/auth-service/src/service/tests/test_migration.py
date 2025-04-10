from io import StringIO

from service.core.cli import call_command

# def test_migration_model_changes():
#     """
#     Test whether the migrations are created properly. And in sync with the models.
#     """
#
#     output = StringIO()
#     call_command("createmigration", stdout=output, dry_run=True)
#     assert (
#         output.getvalue() == "No changes detected\n"
#     ), "Migrations are needed before running tests"
