from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (TokenBlacklistView,
                                            TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from .yasg import urlpatterns as doc_url

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("animals.urls")),
    path("api/", include("users.urls")),
    # Регистрация, авторизация
    path("auth/", include("djoser.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
]

urlpatterns += doc_url
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
