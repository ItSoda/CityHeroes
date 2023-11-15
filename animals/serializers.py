from tempfile import NamedTemporaryFile
from urllib.request import urlopen

from django.core.files import File
from rest_framework import serializers

from .models import Animals


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animals
        fields = "__all__"
