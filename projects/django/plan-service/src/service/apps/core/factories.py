import factory
from factory import fuzzy
from faker import Faker
from service.apps.core.choices import ActivityLevel, BodyType

fake = Faker()

__all__ = ["PlanFactory", "PlanMealFactory"]


class PlanFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "service.apps.core.Plan"

    user = factory.SubFactory("service.apps.core.factories.UserFactory")
    name = factory.LazyAttribute(lambda x: f"{x}{fake.name()}")
    start_date = factory.LazyAttribute(lambda x: fake.past_datetime())
    end_date = factory.LazyAttribute(lambda x: fake.future_datetime())
    body_weight = factory.LazyAttribute(lambda x: fake.random_number())
    body_height = factory.LazyAttribute(lambda x: fake.random_number())
    body_type = fuzzy.FuzzyChoice(
        [
            BodyType.AVERAGE,
            BodyType.THIN,
            BodyType.SLIM,
            BodyType.ATHLETIC,
            BodyType.OVERWEIGHT,
            BodyType.MUSCULAR,
        ]
    )
    activity_level = fuzzy.FuzzyChoice(
        [
            ActivityLevel.SEDENTARY,
            ActivityLevel.LIGHTLY_ACTIVE,
            ActivityLevel.MODERATELY_ACTIVE,
            ActivityLevel.VERY_ACTIVE,
            ActivityLevel.EXTRA_ACTIVE,
        ]
    )


class PlanMealFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "service.apps.core.PlanMeal"

    recipe = factory.SubFactory("service.apps.core.factories.RecipeFactory")
    plan = factory.SubFactory("service.apps.core.factories.PlanFactory")
