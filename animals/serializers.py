from tempfile import NamedTemporaryFile
from urllib.request import urlopen

from django.core.files import File
from rest_framework import serializers
from .models import Animal


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = "__all__"
