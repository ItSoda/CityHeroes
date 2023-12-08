from django.urls import include, path
from . import views

app_name = "chat"


urlpatterns = [
    path("<int:user_pk>/", views.personal_chat, name="ph"),
]