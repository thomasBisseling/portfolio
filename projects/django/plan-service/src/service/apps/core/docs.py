from vitaleey.core.docs import api_doc, get_responses

from .serializers import (
    PlanCalculateSerializer,
    PlanMealSerializer,
    PlanSerializer,
)

# Plan API schemas

plan_list = api_doc(
    responses=get_responses(
        {
            200: PlanSerializer(many=True),
        }
    ),
)

plan_detail = api_doc(
    responses=get_responses(
        {
            200: PlanSerializer(),
        }
    ),
    parameters=[
        {
            "name": "id",
            "description": "Plan ID",
        }
    ],
)

plan_create_single = api_doc(
    responses=get_responses(
        {
            201: PlanSerializer(),
        }
    ),
    request_body=PlanSerializer,
)

plan_update_single = api_doc(
    responses=get_responses(
        {
            200: PlanSerializer(),
        }
    ),
    request_body=PlanSerializer,
    parameters=[
        {
            "name": "id",
            "description": "Plan ID",
        }
    ],
)

plan_partial_update_single = api_doc(
    responses=get_responses(
        {
            200: PlanSerializer(),
        }
    ),
    request_body=PlanSerializer,
)

plan_delete_single = api_doc(
    responses=get_responses(
        {
            204: None,
        }
    ),
    parameters=[
        {
            "name": "id",
            "description": "Plan ID",
        }
    ],
)

plan_calculate = api_doc(
    responses=get_responses(
        {
            200: PlanCalculateSerializer(),
        }
    ),
)

plan_meal_refresh = api_doc(
    responses=get_responses(
        {
            200: PlanMealSerializer(),
        }
    ),
    parameters=[
        {
            "name": "id",
            "description": "Plan Meal ID",
        }
    ],
)
