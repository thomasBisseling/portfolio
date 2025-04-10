import pytest
from vitaleey.api.plans.calculate import calculate_bmr, calculate_tee
from vitaleey.api.plans.choices import ActivityLevel
from vitaleey.api.users.choices import Gender


@pytest.mark.parametrize(
    "gender, weight, height, age, expected",
    [
        (Gender.MAN.value, 80, 180, 25, 1912),
        (Gender.WOMAN.value, 60, 160, 30, 1378),
        (Gender.OTHER.value, 70, 170, 27, 1610),
    ],
)
def test_bmr_calculation(gender, weight, height, age, expected):
    """Test whether BMR calculation is correct"""

    result = calculate_bmr(gender, weight, height, age)
    assert result == expected, f"Result should be {expected}"


@pytest.mark.parametrize(
    "gender, weight, height, age",
    [
        ("invalid", 80, 180, 25),
        (Gender.MAN.value, -80, 180, 25),
        (Gender.WOMAN.value, 80, -180, 25),
        (Gender.OTHER.value, 80, 180, -25),
    ],
)
def test_bmr_calculation_with_invalid_parameters(gender, weight, height, age):
    """Test whether BMR calculation is correct with invalid parameters"""

    result = calculate_bmr(gender, weight, height, age)
    assert result == 0, "Result should be 0"


@pytest.mark.parametrize(
    "weight, height, age",
    [
        (40, 130, 15),
        (300, 240, 80),
        (40, 240, 80),
        (300, 130, 15),
    ],
)
def test_bmr_calculation_with_out_of_bound_parameters(weight, height, age):
    """
    Test BMR calculation with out of bound parameters
    """

    result = calculate_bmr(Gender.MAN, weight, height, age)
    assert result == 0, "Result should be 0"


@pytest.mark.parametrize(
    "activity_level, expected",
    [
        (ActivityLevel.SEDENTARY, 2295),
        (ActivityLevel.LIGHTLY_ACTIVE, 2629),
        (ActivityLevel.MODERATELY_ACTIVE, 2964),
        (ActivityLevel.ACTIVE, 3251),
        (ActivityLevel.VERY_ACTIVE, 3633),
        (ActivityLevel.EXTRA_ACTIVE, 3824),
        (ActivityLevel.EXTREME_ACTIVE, 7648),
    ],
)
def test_tee_calculation(activity_level, expected):
    """
    Test TEE calculation
    """

    bmr = 1912
    result = calculate_tee(bmr, activity_level.value)
    assert result == expected, f"Result should be {expected}"


@pytest.mark.parametrize(
    "bmr, activity_level",
    [
        (1912, -10),
        (-1912, ActivityLevel.SEDENTARY),
    ],
)
def test_tee_calculation_with_invalid_parameters(bmr, activity_level):
    """
    Test TEE calculation with invalid parameters
    """

    result = calculate_tee(bmr, activity_level)
    assert result == 0, "Result should be 0"
