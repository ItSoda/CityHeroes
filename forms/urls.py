from django.urls import path
from .views import FormAnimalCreateAPIView

app_name = "forms"

urlpatterns = [
    path("formanimal/create/", FormAnimalCreateAPIView.as_view(), name="form-create"),
]
