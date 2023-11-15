from django.urls import path

from .views import EmailVerificationAndUserUpdateView

app_name = "users"


urlpatterns = [
    path(
        "verify/<str:email>/<uuid:code>/",
        EmailVerificationAndUserUpdateView.as_view(),
        name="email_verify",
    ),
    path(
        "user/update/", EmailVerificationAndUserUpdateView.as_view(), name="user-update"
    ),
]
