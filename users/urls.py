from django.urls import include, path
from rest_framework import routers

from .views import EmailVerificationAndUserUpdateView, UserModelViewSet

app_name = "users"

router = routers.DefaultRouter()
router.register("users", UserModelViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "verify/<str:email>/<uuid:code>/",
        EmailVerificationAndUserUpdateView.as_view(),
        name="email_verify",
    ),
    path(
        "user/update/", EmailVerificationAndUserUpdateView.as_view(), name="user-update"
    ),
]
