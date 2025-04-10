from service.core.cli import BaseCommand
from service.core.database import db_connection
from service.factories import BaseFactory, UserFactory
from service.models import User
from service.services.user import UserService


class Command(BaseCommand):
    """
    Command to generate demo data
    """

    @staticmethod
    def get_small_factory_batch():
        """
        Get the counts for the small factories
        """

        return {}

    @staticmethod
    def get_user_factory_dict(**kwargs):
        """
        Create a user factory dictionary
        """

        data = UserFactory.build(**kwargs).__dict__
        return User.cast_dict(data)

    async def handle(self, *args, **options):
        """
        Handle the command
        """

        default_password = "admin"

        async for session in db_connection.get_async_session():
            superuser_data = self.get_user_factory_dict(is_superuser=True)

            user_service = UserService(session)
            superuser = await user_service.create(superuser_data)
            await user_service.set_password(superuser, default_password)

            # Create staff users
            for _ in range(2):
                staff_user_data = self.get_user_factory_dict(is_staff=True)
                staff_user = await user_service.create(staff_user_data)
                await user_service.set_password(staff_user, default_password)

            # Create demo users
            for _ in range(5):
                user_data = self.get_user_factory_dict(
                    is_staff=False, is_superuser=False
                )
                user = await user_service.create(user_data)
                await user_service.set_password(user, default_password)
            await user_service.save()

        self.stdout.write(
            self.stdout.style("Demo data created", color=self.colors.GREEN)
        )
