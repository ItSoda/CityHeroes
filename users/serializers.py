from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from .models import Users


class UserCompanySerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "name_company",
            "is_company",
            "description",
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"
        ref_name = "CustomUser"
