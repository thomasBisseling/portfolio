import pytest
from django.urls import reverse_lazy
from vitaleey.api.plans.choices import ActivityLevel
from vitaleey.api.users.choices import Gender


@pytest.mark.parametrize(
    "gender, weight, height, age, expected",
    [
        (Gender.MAN.value, 80, 180, 25, [1912, 2629]),
        (Gender.WOMAN.value, 60, 160, 30, [1378, 1895]),
        (Gender.OTHER.value, 70, 170, 27, [1610, 2214]),
    ],
)
def test_plan_calculation(
    api_client, user, gender, weight, height, age, expected
):
    """Test whether we can calculate a plan as guest"""

    url = reverse_lazy("plan-calculate")

    # Man
    payload = {
        "body_weight": weight,
        "body_height": height,
        "activity_level": ActivityLevel.LIGHTLY_ACTIVE.value,
        "age": age,
        "gender": gender,
    }
    response = api_client(user).get(url, payload)

    assert response.status_code == 200, "Should return 200"
    assert (
        response.data["bmr"] == expected[0]
    ), f"BMR is not equal, must be {expected[0]}"
    assert (
        response.data["tee"] == expected[1]
    ), f"TEE is not equal, must be {expected[1]}"


def test_plan_calculation_with_invalid_data(api_client):
    """Test whether we can calculate a plan with invalid data"""

    url = reverse_lazy("plan-calculate")
    payload = {
        "body_weight": 70,
        "body_height": 0,
        "activity_level": ActivityLevel.LIGHTLY_ACTIVE,
        "age": 46,
        "gender": 40,
    }

    response = api_client().get(url, data=payload)
    assert response.status_code == 400, "Should return 400"

    payload = {
        "body_weight": 70,
        "body_height": 170,
        "activity_level": ActivityLevel.LIGHTLY_ACTIVE,
        "age": 0,
        "gender": Gender.MAN,
    }

    response = api_client().get(url, data=payload)
    assert response.status_code == 400, "Should return 400"

    payload = {
        "body_weight": 0,
        "body_height": 170,
        "activity_level": ActivityLevel.LIGHTLY_ACTIVE,
        "age": 40,
        "gender": Gender.MAN,
    }

    response = api_client().get(url, data=payload)
    assert response.status_code == 400, "Should return 400"
