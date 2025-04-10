from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_guardian.filters import ObjectPermissionsFilter
from vitaleey.core.views import BaseAPIView

from . import docs
from .calculate import calculate_bmr, calculate_tee
from .models import Plan, PlanMeal
from .serializers import (
    PlanCalculateSerializer,
    PlanMealSerializer,
    PlanSerializer,
    PlanUpdateSerializer,
)


class BasePlanView(BaseAPIView):
    """
    Base API endpoint that allows plans to be viewed or edited.
    """

    serializer_class = PlanSerializer
    queryset = Plan.objects.all().order_by("name")


class PlanList(BasePlanView, generics.ListAPIView):
    """Get a list of plans.

    Use this endpoint to retrieve a list of plans.
    """

    filter_backends = [ObjectPermissionsFilter]

    @docs.plan_list
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PlanUserList(BasePlanView, generics.ListAPIView):
    """Get a list of plans of a user.

    Use this endpoint to retrieve a list of plans of a user.
    """

    filter_backends = [ObjectPermissionsFilter]

    def check_user_plans(self):
        user_plans = Plan.objects.filter(user=self.kwargs["pk"])
        qs = self.filter_queryset(self.get_queryset())

        if user_plans.count() != qs.count():
            raise self.permission_denied(
                self.request, message="Permission denied", code=403
            )

    def get_queryset(self):
        return super().get_queryset().filter(user=self.kwargs["pk"])

    def list(self, request, *args, **kwargs):
        self.check_user_plans()
        return super().list(request, *args, **kwargs)

    @docs.plan_list
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PlanCreate(BasePlanView, generics.CreateAPIView):
    """Create a single plan.

    Use this endpoint to create a single plan.
    """

    serializer_class = PlanUpdateSerializer

    @docs.plan_create_single
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PlanDetail(BasePlanView, generics.RetrieveAPIView):
    """Get a single plan.

    Use this endpoint to retrieve a single plan. The plan is identified by the plan's id.
    """

    @docs.plan_detail
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PlanUpdate(BasePlanView, generics.UpdateAPIView):
    """Update a single plan.

    Use this endpoint to update a single plan. The plan is identified by the plan's id.
    """

    serializer_class = PlanUpdateSerializer

    @docs.plan_update_single
    def patch(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class PlanDelete(BasePlanView, generics.DestroyAPIView):
    """Delete a single plan.

    Use this endpoint to delete a single plan. The plan is identified by the plan's id.
    """

    @docs.plan_delete_single
    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class PlanCalulate(BasePlanView):
    """Calculate a plan.

    Use this endpoint to calculate a plan.
    """

    authentication_classes = []
    serializer_class = PlanCalculateSerializer
    permission_classes = []

    def calculate(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        data["bmr"] = calculate_bmr(
            data["gender"],
            data["body_weight"],
            data["body_height"],
            data["age"],
        )
        data["tee"] = calculate_tee(data["bmr"], data["activity_level"])

        return Response(data, status=status.HTTP_200_OK)

    @docs.plan_calculate
    def get(self, request, *args, **kwargs):
        return self.calculate(request, *args, **kwargs)


class PlanMealRefresh(BasePlanView, generics.RetrieveAPIView):
    """Refresh a plan's meals.

    Use this endpoint to refresh a plan's meals.
    """

    queryset = PlanMeal.objects.all()
    serializer_class = PlanMealSerializer
    object_permission_list = ["change_planmeal", "view_planmeal"]

    def refresh_meal(self, request, *args, **kwargs):
        object = self.get_object()
        recipe = object.plan.get_random_recipe(
            object.recipe.meal_type, object.date
        )
        object.recipe = recipe
        object.save()

        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    @docs.plan_meal_refresh
    def post(self, request, *args, **kwargs):
        return self.refresh_meal(request, *args, **kwargs)
