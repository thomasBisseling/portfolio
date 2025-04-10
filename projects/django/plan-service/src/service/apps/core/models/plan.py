from django.db import models
from django.utils import timezone

# from .choices.food import MealType
from service.apps.core.choices import ActivityLevel, BodyType
from vitaleey.core.models.base import AbstractBaseModel

# from .plan_meal import PlanMeal
# from .recipe import Recipe


class Plan(AbstractBaseModel):
    user = models.CharField(max_length=255, verbose_name="User ID")
    body_weight = models.FloatField(null=True)
    body_height = models.FloatField(null=True)
    body_type = models.CharField(
        max_length=255, choices=BodyType.choices, default=BodyType.AVERAGE
    )
    activity_level = models.FloatField(
        choices=ActivityLevel.choices, default=ActivityLevel.LIGHTLY_ACTIVE
    )
    name = models.CharField(max_length=50)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True)

    def __str__(self):
        return f"{self.user.email} - {self.name}"

    @property
    def is_active(self) -> bool:
        return self.start_date <= timezone.now().date() <= self.end_date

    # def get_recipes_past_week(self, date=None):
    #     """Get recipes from the past week"""

    #     if not date:
    #         date = timezone.now().date()
    #     past_week = date - timezone.timedelta(days=7)
    #     return self.get_used_recipes(date__gte=past_week, date__lt=date)

    # def get_used_recipes(self, meal_type=None, **filters):
    #     """Get used recipes"""

    #     qs = PlanMeal.objects.filter(plan=self, **filters).order_by("date")

    #     if meal_type:
    #         qs = qs.filter(recipe__meal_type=meal_type)
    #     return Recipe.objects.filter(
    #         pk__in=qs.values_list("recipe", flat=True)
    #     )

    # def recipes_available(self, date=None, meal_type=None):
    #     """Get available recipes for a specific date"""

    #     if not date:
    #         date = timezone.now().date()
    #     recipes = self.user.profile.available_recipes().exclude(
    #         pk__in=self.get_recipes_past_week(date)
    #     )
    #     used_recipes = self.get_used_recipes(meal_type=meal_type)

    #     recipes = recipes.annotate(
    #         used=Case(
    #             When(pk__in=used_recipes, then=True),
    #             default=False,
    #             output_field=BooleanField(),
    #         )
    #     ).order_by("used")

    #     if meal_type:
    #         return recipes.filter(meal_type=meal_type)
    #     return recipes

    # def set_meal_plan(self, date, recipe, update_or_create=False):
    #     """Set meal plan for a specific date, is meal plan already exists, update it. Otherwise, create it."""

    #     if not recipe:
    #         return

    #     if update_or_create:
    #         self.meal.update_or_create(
    #             date=date, recipe__meal_type=recipe.meal_type, recipe=recipe
    #         )
    #         return self.meal

    #     self.meal.create(
    #         date=date,
    #         recipe=recipe,
    #     )

    #     return self.meal

    # def get_random_recipe(self, meal_type, date):
    #     """Get random recipe for a specific meal type"""

    #     recipes = self.recipes_available(date=date, meal_type=meal_type)
    #     return recipes.order_by("?").first()

    # def generate_meal_plan(self, date=None):
    #     """Generate meal plan for a specific date"""

    #     if not date:
    #         date = timezone.now().date()

    #     # Create meal plan for each meal type
    #     for meal_type in MealType.values:
    #         recipe = self.get_random_recipe(meal_type, date)
    #         self.set_meal_plan(date, recipe)

    # def get_todays_meal_plan(self):
    #     """Get today's meal plan"""

    #     return self.meal.filter(date=timezone.now().date())

    # def get_meal_plan(self, date):
    #     """Get meal plan for a specific date"""

    #     return self.meal.filter(date=date)

    class Meta:
        unique_together = ["user", "name", "start_date", "end_date"]
        ordering = ["-start_date"]
        verbose_name_plural = "Plans"
        permissions = [
            ("view_all_plans", "Can view all plans"),
        ]
