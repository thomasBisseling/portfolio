from django.db import models
from vitaleey.core.models.base import AbstractBaseModel


class PlanProgress(AbstractBaseModel):
    plan = models.ForeignKey("core.Plan", on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.FloatField()
    log = models.TextField()

    def __str__(self):
        return f"{self.plan} - {self.date}"

    class Meta:
        unique_together = ["plan", "date"]
        ordering = ["-date"]
