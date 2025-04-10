from django.urls import reverse_lazy


def test_plan_meal_refresh(api_client, user, create_plan, generate_recipes):
    """Test whether we can refresh a plan's meal as admin"""

    generate_recipes(user, 10)
    plan = create_plan(user)
    meal_plan = plan.meal.all().first()

    url = reverse_lazy("plan-meal-refresh", kwargs={"pk": meal_plan.id})

    response = api_client(user).post(url, format="json")

    assert response.status_code == 200, "Should return 200"
    assert response.data["plan"]["id"] == plan.id, "Plan ID is not equal"
    assert (
        response.data["recipe"]["id"] != meal_plan.recipe.id
    ), "Recipe ID is equal"
