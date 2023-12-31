import logging

from rest_framework import serializers

from users.models import Users
from users.serializers import ImageFieldFromURL, UserSerializer

from .models import Animals, FormAnimals, Images

logger = logging.getLogger("main")


class ImageSerializer(serializers.ModelSerializer):
    image = ImageFieldFromURL()

    class Meta:
        model = Images
        fields = ("id", "title", "image")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.image:
            representation['image'] = "http://red-store.site/media/" + str(instance.image)
        return representation


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


class AnimalShortSerializer(serializers.ModelSerializer):
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
        try:
            user = Users.objects.get(id=user_id)
            animal = Animals.objects.get(id=animal_id)
            instance = FormAnimals.objects.create(
                user=user, animal=animal, **validated_data
            )
            return instance
        except (Users.DoesNotExist, Animals.DoesNotExist):
            raise serializers.ValidationError("User or Animal does not exist.")


class FormAnimalSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    animal = AnimalSerializer()

    class Meta:
        model = FormAnimals
        fields = "__all__"


class UserProfile(UserSerializer):
    photo = ImageFieldFromURL()
    forms = FormAnimalSerializer(many=True)
    favourites = AnimalSerializer(many=True)
    class Meta(UserSerializer.Meta):
        model = Users
        fields = (
            "id",
            "email",
            "password",
            "username",
            "first_name",
            "last_name",
            "is_verified_email",
            "is_company",
            "description",
            "photo",
            "forms",
            "quantity_forms",
            "quantity_favourites",
            "favourites",
        )
        read_only_fields = ("password",)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.photo:
            representation['photo'] = "http://red-store.site/media/" + str(instance.photo)
        return representation
