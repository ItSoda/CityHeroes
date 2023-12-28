from django.urls import include, path
from rest_framework import routers

from .views import (AnimalModelViewSet, AnimalSearchView,
                    FormAnimalsCreateAPIView)

app_name = "animals"

router = routers.DefaultRouter()
router.register(r"animals", AnimalModelViewSet, basename="animals")

urlpatterns = [
    path("", include(router.urls)),
    path("animals/search/", AnimalSearchView.as_view({"get": "search"}), name="search"),
    path("formanimal/create/", FormAnimalsCreateAPIView.as_view(), name="form-create"),
]
