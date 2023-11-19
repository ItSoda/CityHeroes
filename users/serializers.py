from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from .models import Users
from django.contrib.auth import get_user_model

class UserCompanyCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = get_user_model()
        fields = ("id", "email", "password", "name_company")
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ("email", "password")
        ref_name = "CustomUser"
