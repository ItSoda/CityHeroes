from django.urls import include, path
from rest_framework import routers

from .views import (
    EmailVerificationAndUserUpdateView,
    SubscriptionCreateView,
    YookassaWebhookView,
    UserViewSet,
    UserSearchView
)

app_name = "users"

router = routers.DefaultRouter()
router.register("users", UserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
    path("users/search/", UserSearchView.as_view(), name="search"),
    path(
        "verify/<str:email>/<uuid:code>/",
        EmailVerificationAndUserUpdateView.as_view(),
        name="email_verify",
    ),
    path("payment/create/", SubscriptionCreateView.as_view(), name="payment-create"),
    path("yookassa/webhook/", YookassaWebhookView.as_view(), name="yookassa-webhook"),
]
