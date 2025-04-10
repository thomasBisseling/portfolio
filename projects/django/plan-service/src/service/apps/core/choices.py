from django.db import models


class BodyType(models.TextChoices):
    """Body Type Choices"""

    THIN = "t"
    SLIM = "s"
    AVERAGE = "a"
    ATHLETIC = "at"
    MUSCULAR = "m"
    OVERWEIGHT = "o"


class ActivityLevel(float, models.Choices):
    """Activity Level Choices"""

    SEDENTARY = 1.2
    LIGHTLY_ACTIVE = 1.375
    MODERATELY_ACTIVE = 1.55
    ACTIVE = 1.7
    VERY_ACTIVE = 1.9
    EXTRA_ACTIVE = 2
    EXTREME_ACTIVE = 4
