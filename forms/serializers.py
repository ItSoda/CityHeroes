from rest_framework import serializers
from animals.models import Animal

from users.models import User
from .models import FormAnimal


class FormAnimalSerializer(serializers.ModelSerializer):
    animal = serializers.IntegerField(write_only=True)
    user = serializers.IntegerField(write_only=True)

    class Meta:
        model = FormAnimal
        fields = "__all__"

    def create(self, validated_data):
        user_id = validated_data.pop("user")
        animal_id = validated_data.pop("animal")

        instance = FormAnimal.objects.create(
            user_id=user_id, animal_id=animal_id, **validated_data
        )

        return instance
