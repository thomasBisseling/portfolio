from django.utils import timezone
from service.food.choices import MealType
from vitaleey.factories import (
    PlanFactory,
)


def test_generate_meal_plan(user, generate_recipes):
    """Test whether the user can generate a meal plan for today."""

    # Generate recipes for the user
    recipes = generate_recipes(user)

    # Create a plan for the user
    plan = PlanFactory(user=user)

    # Check that the recipe is not in the user available recipes
    available_recipes = user.profile.available_recipes()
    for recipe in recipes["disallow"]:
        assert recipe not in available_recipes
    for recipe in recipes["allow"]:
        assert recipe in available_recipes

    # Generate a meal plan for the user
    plan.generate_meal_plan()
    plan.refresh_from_db()

    # Check that the plan meals were created
    meal_type_len = len(MealType.labels)
    assert (
        plan.get_todays_meal_plan().count() == meal_type_len
    ), "Plan meals were not created, for each meal type"
    for plan_meal in plan.get_todays_meal_plan():
        assert plan_meal.recipe in available_recipes
        assert plan_meal.date == timezone.now().date()
        assert plan_meal.plan == plan
        assert plan_meal.recipe.meal_type in (
            meal_type[0] for meal_type in MealType.choices
        )


def test_generate_meal_plan_past_week(user, generate_recipes):
    """Test whether the user can generate a meal plan without using the recipes of the past week."""

    generate_recipes(user)

    # Create a plan for the user
    plan = PlanFactory(user=user)

    # Generate a meal plans for the past week
    past_week = timezone.now().date() - timezone.timedelta(days=7)
    for i in range(7):
        plan.generate_meal_plan(past_week + timezone.timedelta(days=i))

    # Generate a meal plan for tomorrow
    plan.refresh_from_db()

    # Used meals of last week are not available
    assert plan.get_recipes_past_week() not in plan.recipes_available()
    for meal in plan.get_recipes_past_week():
        assert meal not in plan.recipes_available()


def test_generate_meal_plan_if_used_recipes_are_at_last(
    user, generate_recipes
):
    """Test whether the user can generate a meal plan without using the recipes of the past week."""

    generate_recipes(user)

    # Create a plan for the user
    plan = PlanFactory(user=user)

    # Generate a meal plans for the past week
    week_before_past_week = timezone.now().date() - timezone.timedelta(days=14)
    for i in range(14):
        date = week_before_past_week + timezone.timedelta(days=i)
        plan.generate_meal_plan(date)

    # Generate a meal plan for tomorrow
    plan.refresh_from_db()

    for meal in plan.get_recipes_past_week():
        assert meal not in plan.recipes_available()

    recipes = plan.recipes_available()
    used_recipes = plan.get_used_recipes()

    # Check that the used recipes are at last
    for index, used_recipe in enumerate(used_recipes):
        assert any(
            used_recipe == recipe for recipe in recipes
        ), "Used recipe is not in recipes"
        assert recipes[len(recipes) - index - 1] == used_recipe
