from django.urls import path

from .views import (
    PlanViewSet,
)
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("plans/", PlanViewSet.as_view({"get": "list", "post": "create"})),
    path("plans/<uuid:pk>/", PlanViewSet.as_view({"get": "retrieve", "put": "update"})),
]

if settings.DEBUG:
    # Serve static files from development server
    urlpatterns += staticfiles_urlpatterns()
