from django.urls import path

from .views import AnimalRetrieveAPIView, AnimalSearchView, AnimalsListAPIView

app_name = "animals"


urlpatterns = [
    path("animals/", AnimalsListAPIView.as_view(), name="animals"),
    path("animal/<int:pk>/", AnimalRetrieveAPIView.as_view(), name="animal-retrieve"),
    path("animals/search/", AnimalSearchView.as_view(), name="search"),
]
