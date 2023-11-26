from django.urls import include, path
from rest_framework import routers

from .views import (EmailVerificationAndUserUpdateView, SubscriptionCreateView,
                    UserModelViewSet, YookassaWebhookView)

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
    path("payment/create/", SubscriptionCreateView.as_view(), name="payment-create"),
    path("yookassa/webhook/", YookassaWebhookView.as_view(), name="yookassa-webhook"),
]
