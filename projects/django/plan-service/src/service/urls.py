
from django.urls import path, include

from service.apps.core.urls import urlpatterns as core_urls
from django.http import HttpResponse

urlpatterns = [
    path(
        "__healthcheck__/", lambda request: HttpResponse("200 OK"), name="healthcheck"
    ),
    path('', include(core_urls)),
]
