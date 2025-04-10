from django.db import models
from vitaleey.core.models.base import AbstractBaseModel


class PlanMeal(AbstractBaseModel):
    date = models.DateField(
        auto_now_add=True, help_text="Date of the meal plan"
    )
    plan = models.ForeignKey(
        "core.Plan", on_delete=models.CASCADE, related_name="meal"
    )
    recipe = models.CharField(max_length=255, verbose_name="Recipe ID")

    def __str__(self):
        return f"{self.plan} - {self.recipe} - {self.recipe.meal_type}"
