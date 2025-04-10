from os import path

import factory
import pytest
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from faker import Faker
from faker_file.providers.png_file import PngFileProvider
from rest_framework.test import APIClient
from vitaleey.api.food.choices import MealType
from vitaleey.factories import (
    AllergenFactory,
    DietFactory,
    PlanFactory,
    RecipeFactory,
)
from vitaleey.factories.users import create_user

faker = Faker()
faker.add_provider(PngFileProvider)


@pytest.fixture(autouse=True, scope="function")
def django_db_setup(db):
    """
    Fixture to setup the database
    """


@pytest.fixture(autouse=True, scope="function")
def clear_cache():
    """Fixture to clear the cache"""
    assert (
        settings.CACHES["default"]["BACKEND"]
        == "django.core.cache.backends.locmem.LocMemCache"
    )
    yield

    cache.clear()


@pytest.fixture(scope="function")
def admin():
    """
    Fixture to create an admin user
    """

    user = create_user(is_admin=True)
    return user


@pytest.fixture(scope="function")
def user():
    """
    Fixture to create a user
    """

    user = create_user()
    return user


@pytest.fixture(scope="function")
def api_client():
    """
    Fixture to provide an API client
    """

    def client(user=None, **kwargs):
        client = APIClient()
        if user:
            client.force_authenticate(user=user)
        return client

    return client


@pytest.fixture(scope="function")
def image_file():
    """
    Fixture to provide an image file
    """
    return factory.django.ImageField().generate({})


@pytest.fixture(scope="function")
def mock_file():
    """
    Fixture to provide an image file
    """

    def get(file_name):
        file_path = path.join(
            path.dirname(__file__), "mocks", "files", file_name
        )
        f = open(file_path, "rb")
        return f

    return get


@pytest.fixture
def generate_recipes():
    def _generate_recipes(user, count=3):
        # Add diets and allergens to the user
        allow_allergens = AllergenFactory.create_batch(count)
        disallow_allergens = AllergenFactory.create_batch(count)
        diets = DietFactory.create_batch(count)
        user.profile.diets.set(diets)
        user.profile.allergies.set(disallow_allergens)
        user.profile.save()

        # Create a recipe with allergens and diets
        allow_recipes = []
        disallow_recipes = []
        for meal_type in MealType.values:
            allow_recipes.extend(
                RecipeFactory.create_batch(count, meal_type=meal_type)
            )

            a_batch = RecipeFactory.create_batch(count)
            for b in a_batch:
                b.allergens.set(allow_allergens)
                b.save()

            allow_recipes.extend(a_batch)

            d_batch = RecipeFactory.create_batch(count)
            for b in d_batch:
                b.allergens.set(disallow_allergens)
                b.save()

            disallow_recipes.extend(d_batch)
        return {"allow": allow_recipes, "disallow": disallow_recipes}

    return _generate_recipes


@pytest.fixture(scope="function")
def create_plan(generate_recipes):
    """
    Fixture to create a plan
    """

    def _make_plan(user, **kwargs):
        today = faker.date_this_year()
        end_date = today + timezone.timedelta(days=30)
        plan = PlanFactory(
            **kwargs, user=user, start_date=today, end_date=end_date
        )

        for i in range(30):
            plan.generate_meal_plan(today + timezone.timedelta(days=i))
        return plan

    return _make_plan
