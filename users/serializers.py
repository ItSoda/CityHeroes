from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from .models import Users


class UserCompanyCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = get_user_model()
        fields = ("id", "email", "password", "name_company", "is_company")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ("id", "email", "password")
        ref_name = "CustomUser"
