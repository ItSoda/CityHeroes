from django.urls import path, include
from rest_framework import routers

from .views import AnimalSearchView, AnimalModelViewSet

app_name = "animals"

router = routers.DefaultRouter()
router.register(r"animals", AnimalModelViewSet, basename="animals")

urlpatterns = [
    path("", include(router.urls)),
    path("animals/search/", AnimalSearchView.as_view(), name="search"),
]
