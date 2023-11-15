from rest_framework import serializers

from .models import FormAnimals


class FormAnimalSerializer(serializers.ModelSerializer):
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
