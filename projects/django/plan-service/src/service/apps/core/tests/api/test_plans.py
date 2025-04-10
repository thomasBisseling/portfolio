import pytest
from django.urls import reverse_lazy
from vitaleey.factories.plans import PlanFactory
from vitaleey.factories.users import create_user


def test_plan_list_as_admin(api_client, admin):
    """Test whether we can get a list of plans as an admin."""

    total_accessable_plan_count = 60
    PlanFactory.create_batch(50)
    PlanFactory.create_batch(10, user=admin)
    url = reverse_lazy("plan-list")
    response = api_client(admin).get(url)

    assert response.status_code == 200, "Should return 200"
    assert (
        total_accessable_plan_count == response.data["count"]
    ), "Should return plans"


@pytest.mark.parametrize(
    "plan_user, auth_user, expected_status_code, expected_count",
    [(create_user(is_admin=True), create_user(), 200, 10)],
)
def test_plan_list_of_user(
    api_client, plan_user, auth_user, expected_status_code, expected_count
):
    """Test whether we can get a list of plans of a user."""

    # PlanFactory.create_batch(15)
    # PlanFactory.create_batch(10, user=user)
    url = reverse_lazy("plan-user-list", kwargs={"pk": plan_user.id})
    response = api_client(auth_user).get(url)

    assert (
        response.status_code == expected_status_code
    ), f"Should return {expected_status_code}"
    assert expected_count == response.data["count"]


def test_plan_detail_as_owner_and_user(api_client, user):
    """Test whether we can get a plan detail as the owner and user"""

    plan = PlanFactory(user=user)
    url = reverse_lazy("plan-detail", kwargs={"pk": plan.id})
    response = api_client(user).get(url)
    assert response.status_code == 200, "Should return 200"

    assert response.data["id"] == plan.id, "Should return the plan id"
    assert response.data["name"] == plan.name, "Should return the plan name"


def test_plan_detail_as_not_owner_and_user(api_client, user):
    """Test whether we can get a plan detail as not the owner and user"""

    plan = PlanFactory()
    url = reverse_lazy("plan-detail", kwargs={"pk": plan.id})
    response = api_client(user).get(url)
    assert (
        response.status_code == 404
    ), "Should return 404, user can't access the plan"


def test_plan_detail_as_admin(api_client, admin):
    """Test whether we can get a plan detail as an admin"""

    plan = PlanFactory()
    url = reverse_lazy("plan-detail", kwargs={"pk": plan.id})
    response = api_client(admin).get(url)
    assert response.status_code == 200, "Should return 200"


def test_plan_create_as_user(api_client, user):
    """Test whether we can create a plan as a user for oneself"""

    url = reverse_lazy("plan-create")
    data = {
        "name": "Test Plan",
        "start_date": "2022-01-01",
        "end_date": "2022-12-31",
        "user": user.id,
    }
    response = api_client(user).post(url, data=data)
    assert response.status_code == 201, "Should return 201"
    assert response.data["name"] == data["name"], "Should return the plan name"


def test_plan_create_as_user_for_user(api_client, user):
    """Test whether we can create a plan as an admin for another user"""

    url = reverse_lazy("plan-create")
    user2 = create_user()
    data = {
        "name": "Test Plan",
        "start_date": "2022-01-01",
        "end_date": "2022-12-31",
        "user": user2.id,
    }
    response = api_client(user).post(url, data=data)
    assert (
        response.status_code == 400
    ), "Should return 400, user can't create a plan for another user"


def test_plan_create_start_date_is_after_end_date(api_client, user):
    """Test whether we can create a plan if start date is after end date"""

    url = reverse_lazy("plan-create")
    data = {
        "name": "Test Plan",
        "start_date": "2022-12-31",
        "end_date": "2022-01-01",
    }
    response = api_client(user).post(url, data=data)
    assert response.status_code == 400, "Should return 400"


def test_plan_update_as_owner(api_client, user):
    """Test whether we can update a plan as the owner"""

    plan = PlanFactory(user=user)
    url = reverse_lazy("plan-update", kwargs={"pk": plan.id})
    data = {
        "name": "Test Plan",
        "start_date": "2022-01-01",
        "end_date": "2022-12-31",
    }
    response = api_client(user).patch(url, data=data)

    assert response.status_code == 200, "Should return 200"
    assert response.data["name"] == data["name"], "Should return the plan name"


def test_plan_update_of_user_as_user(
    api_client,
    user,
):
    """Test whether we can update a plan of other user as a user"""

    user2 = create_user()
    plan = PlanFactory(user=user2)
    url = reverse_lazy("plan-update", kwargs={"pk": plan.id})
    data = {
        "name": "Test Plan",
        "start_date": "2022-01-01",
        "end_date": "2022-12-31",
    }
    response = api_client(user).patch(url, data=data)

    assert (
        response.status_code == 404
    ), "Should return 404, user can't access the plan"


def test_plan_update_as_admin(api_client, admin):
    """Test whether we can update a plan as an admin for other user"""

    plan = PlanFactory()
    url = reverse_lazy("plan-update", kwargs={"pk": plan.id})
    data = {
        "name": "Test Plan",
        "start_date": "2022-01-01",
        "end_date": "2022-12-31",
    }
    response = api_client(admin).patch(url, data=data)

    assert response.status_code == 200, "Should return 200"
    assert response.data["name"] == data["name"], "Should return the plan name"


def test_plan_update_start_date_is_after_end_date(api_client, user):
    """Test whether we can update a plan if start date is after end date"""

    plan = PlanFactory(user=user)
    url = reverse_lazy("plan-update", kwargs={"pk": plan.id})
    data = {
        "name": "Test Plan",
        "start_date": "2022-12-31",
        "end_date": "2022-01-01",
    }
    response = api_client(user).patch(url, data=data)
    assert response.status_code == 400, "Should return 400"


def test_plan_update_update_user(api_client, user):
    """Test whether we can't update the user of a plan"""

    plan = PlanFactory(user=user)
    url = reverse_lazy("plan-update", kwargs={"pk": plan.id})
    data = {
        "name": "Test Plan",
        "start_date": "2022-01-01",
        "end_date": "2022-12-31",
        "user": user.id,
    }
    response = api_client(user).patch(url, data=data)
    assert response.status_code == 400, "Should return 400"


def test_plan_delete_as_owner(api_client, user):
    """Test whether we can delete a plan as the owner"""

    plan = PlanFactory(user=user)
    url = reverse_lazy("plan-delete", kwargs={"pk": plan.id})
    response = api_client(user).delete(url)
    assert response.status_code == 204, "Should return 204"


def test_plan_delete_of_user_as_user(
    api_client,
    user,
):
    """Test whether we can delete a plan of other user as a user"""

    user2 = create_user()
    plan = PlanFactory(user=user2)
    url = reverse_lazy("plan-delete", kwargs={"pk": plan.id})
    response = api_client(user).delete(url)
    assert (
        response.status_code == 404
    ), "Should return 404, user can't access the plan"


def test_plan_delete_as_admin(api_client, admin):
    """Test whether we can delete a plan as an admin for other user"""

    plan = PlanFactory()
    url = reverse_lazy("plan-delete", kwargs={"pk": plan.id})
    response = api_client(admin).delete(url)
    assert response.status_code == 204, "Should return 204"
