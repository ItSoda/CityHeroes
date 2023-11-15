from django.urls import path

from .views import FormAnimalsCreateAPIView

app_name = "forms"

urlpatterns = [
    path("formanimal/create/", FormAnimalsCreateAPIView.as_view(), name="form-create"),
]
