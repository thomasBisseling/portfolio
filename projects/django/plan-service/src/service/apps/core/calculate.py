import math

from django.conf import settings
from vitaleey.core.choices import Gender


def _bmr_calculation(gender, weight, height, age):
    """Basal Metabolic Rate (BMR) calculation"""

    params = _get_bmr_calculation_params(gender)
    if not params:
        return 0

    a = params[0]
    b = params[1] * weight
    c = params[2] * height
    d = params[3] * age
    return a + b + c - d


def _get_bmr_calculation_params(gender):
    """Get Basal Metabolic Rate (BMR) calculation parameters"""

    a, b, c, d = 0, 0, 0, 0

    if gender is Gender.MAN.value:
        a = 66
        b = 13.7
        c = 5
        d = 6
    elif gender is Gender.WOMAN.value:
        a = 655
        b = 9.6
        c = 1.8
        d = 4.7
    else:
        return

    return a, b, c, d


def calculate_bmr(gender, weight, height, age):
    """
    Basal Metabolic Rate (BMR) is the number of calories that your body needs to function at rest.\n
    It is the number of calories that your body needs to maintain basic physiological functions, such as breathing, circulation, cell production, and nutrient processing.

    NOTE: The BMR calculation is based on the Harris-Benedict equation.

    """

    boundaries_weight = settings.BMR_CALCULATION_BOUNDARIES["weight"]
    boundaries_height = settings.BMR_CALCULATION_BOUNDARIES["height"]
    boundaries_age = settings.BMR_CALCULATION_BOUNDARIES["age"]
    calc = 0
    if not (
        boundaries_weight[0] < weight < boundaries_weight[1]
        and boundaries_height[0] < height < boundaries_height[1]
        and boundaries_age[0] < age < boundaries_age[1]
    ):
        return 0

    if gender is Gender.OTHER.value:
        woman_calculation = _bmr_calculation(
            Gender.WOMAN.value, weight, height, age
        )
        man_calculation = _bmr_calculation(
            Gender.MAN.value, weight, height, age
        )
        calc = (woman_calculation + man_calculation) * 0.5
    else:
        calc = _bmr_calculation(gender, weight, height, age)

    return math.ceil(calc) if calc > 0 else 0


def calculate_tee(bmr, pal):
    """
    Total Energy Expenditure (TEE) is the total amount of calories that you burn each day.\n
    It takes into account your Basal Metabolic Rate (BMR) and your activity level.

    NOTE: The Physical Activity Level (PAL) is a measure of the amount of physical activity that a person does in a day. It is calculated by dividing the total energy expenditure (TEE) by the Basal Metabolic Rate (BMR).
    """

    calc = bmr * pal
    return math.ceil(calc) if calc > 0 else 0
