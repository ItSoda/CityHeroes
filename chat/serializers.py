from rest_framework import serializers

from users.models import Users
from users.serializers import ImageFieldFromURL, UserSerializer

from .models import Message, Room


class MessageSerializer(serializers.ModelSerializer):
    created_at_formatted = serializers.SerializerMethodField()
    created_by = UserSerializer()

    class Meta:
        model = Message
        exclude = []
        depth = 1

    def get_created_at_formatted(self, obj: Message):
        return obj.created_at.strftime("%d-%m-%Y %H:%M:%S")


class RoomCreateSerializer(serializers.ModelSerializer):
    agent = serializers.IntegerField(write_only=True)
    messages = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    class Meta:
        model = Room
        fields = "__all__"
        depth = 1
        read_only_fields = [
            "messages",
        ]

    def create(self, validated_data):
        messages_ids = validated_data.pop("messages")
        agent_id = validated_data.pop("agent")
        agent = Users.objects.get(pk=agent_id)

        instance = Room.objects.create(agent=agent, **validated_data)
        instance.messages.set(messages_ids)

        return instance


class RoomSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    agent = UserSerializer()

    class Meta:
        model = Room
        fields = "__all__"
        depth = 1
        read_only_fields = [
            "messages",
        ]
