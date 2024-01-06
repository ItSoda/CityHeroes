from django.urls import include, path
from rest_framework import routers

from .views import (AnimalFavouriteUserViewSet, AnimalModelViewSet,
                    FormAnimalViewSet)

app_name = "animals"

router = routers.DefaultRouter()
router.register(r"animals", AnimalModelViewSet, basename="animals")
router.register(r"forms", FormAnimalViewSet, basename="forms")

urlpatterns = [
    path("", include(router.urls)),
    # path("animal/search/", AnimalSearchView.as_view({"get": "list"}), name="search"),
    path(
        "animal/favourite/<int:animal_id>/",
        AnimalFavouriteUserViewSet.as_view(),
        name="animal-favourite",
    ),
]
