from tempfile import NamedTemporaryFile
from urllib.request import urlopen

from django.core.files import File
from rest_framework import serializers

from users.models import Users
from users.serializers import UserSerializer
from .models import Animals, FormAnimals, Images


class ImageFieldFromURL(serializers.ImageField):
    def to_internal_value(self, data):
        # Проверяем, если data - это URL
        if data.startswith("http") or data.startswith("https"):
            # Открываем URL и читаем его содержимое
            response = urlopen(data)
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(response.read())
            img_temp.flush()
            # Создаем объект File из временного файла
            img = File(img_temp)
            # Возвращаем его как значение поля
            return img
        return super().to_internal_value(data)


class ImageSerializer(serializers.ModelSerializer):
    image = ImageFieldFromURL()

    class Meta:
        model = Images
        fields = "__all__"


class AnimalCreateSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(write_only=True)
    images = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    class Meta:
        model = Animals
        fields = "__all__"

    def create(self, validated_data):
        user_id = validated_data.pop("user")
        user_instance = Users.objects.get(id=user_id)
        images_ids = validated_data.pop("images")

        instance = Animals.objects.create(user=user_instance, **validated_data)
        instance.images.set(images_ids)
        return instance


class AnimalSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    images = ImageSerializer(many=True)

    class Meta:
        model = Animals
        fields = "__all__"


class FormAnimalCreateSerializer(serializers.ModelSerializer):
    animal = serializers.IntegerField(write_only=True)
    user = serializers.IntegerField(write_only=True)

    class Meta:
        model = FormAnimals
        fields = "__all__"

    def create(self, validated_data):
        user_id = validated_data.pop("user")
        animal_id = validated_data.pop("animal")

        instance = FormAnimals.objects.create(
            user_id=user_id, animal_id=animal_id, **validated_data
        )

        return instance


class FormAnimalSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    animal = AnimalSerializer()

    class Meta:
        model = FormAnimals
        fields = "__all__"
