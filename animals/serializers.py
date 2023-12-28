from rest_framework import serializers

from users.models import Users
from users.serializers import ImageFieldFromURL, UserSerializer

from .models import Animals, FormAnimals, Images


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


class AnimalShortSerializer(serializers.Serializer):
    user = UserSerializer()
    images = ImageSerializer(many=True)

    class Meta:
        model = Animals
        fields = ("id", "name", "images", "user")


class FormAnimalCreateSerializer(serializers.ModelSerializer):
    animal = serializers.IntegerField(write_only=True)
    user = serializers.IntegerField(write_only=True)

    class Meta:
        model = FormAnimals
        fields = "__all__"

    def create(self, validated_data):
        user_id = validated_data.pop("user")
        animal_id = validated_data.pop("animal")

        user = Users.objects.get(id=user_id)
        animal = Animals.objects.get(id=animal_id)

        instance = FormAnimals.objects.create(
            user=user, animal=animal, **validated_data
        )

        return instance


class FormAnimalSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    animal = AnimalSerializer()

    class Meta:
        model = FormAnimals
        fields = "__all__"
