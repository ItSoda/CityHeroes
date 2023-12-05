from collections import OrderedDict
from rest_framework.test import APITestCase
from chat.serializers import RoomSerializer, MessageSerializer
from users.serializers import UserSerializer
from chat.models import Room, Message
from users.models import Users


class ChatSerializerAPITestCase(APITestCase):
    """This test covers chat serializer"""

    def setUp(self):
        self.user = Users.objects.create_user(
            email="nikitashchegilskiy@gmail.com", password="nik140406"
        )
        self.room = Room.objects.create(
            name="Nikita",
            host=self.user,
        )
        self.room.current_users.add(self.user)

        self.message = Message.objects.create(
            room=self.room, text="GOGOGO", user=self.user
        )

    def test_serializer_room(self):
        data = RoomSerializer(self.room).data
        print(data)
        expected_data = {
            "pk": self.room.pk,
            "name": "Nikita",
            "host": OrderedDict(
                [("id", self.user.id), ("email", "nikitashchegilskiy@gmail.com")]
            ),
            "messages": [
                OrderedDict(
                    [
                        ("id", self.message.id),
                        (
                            "created_at_formatted",
                            self.message.created_at.strftime("%d-%m-%Y %H:%M:%S"),
                        ),
                        (
                            "user",
                            OrderedDict(
                                [
                                    ("id", self.user.id),
                                    ("email", "nikitashchegilskiy@gmail.com"),
                                ]
                            ),
                        ),
                        (
                            "text",
                            "GOGOGO",
                        ),
                        ("created_at", self.message.created_at.isoformat()),
                        (
                            "room",
                            OrderedDict(
                                [
                                    ("id", self.room.id),
                                    (
                                        "name",
                                        "Nikita",
                                    ),
                                    ("host", self.user.id),
                                    ("current_users", [self.user.id]),
                                ]
                            ),
                        ),
                    ]
                )
            ],
            "current_users": [
                OrderedDict(
                    [("id", self.user.id), ("email", "nikitashchegilskiy@gmail.com")]
                )
            ],
            "last_message": OrderedDict(
                [
                    ("id", self.message.id),
                    (
                        "created_at_formatted",
                        self.message.created_at.strftime("%d-%m-%Y %H:%M:%S"),
                    ),
                    (
                        "user",
                        OrderedDict(
                            [
                                ("id", self.user.id),
                                ("email", "nikitashchegilskiy@gmail.com"),
                            ]
                        ),
                    ),
                    ("text", "GOGOGO"),
                    ("created_at", self.message.created_at.isoformat()),
                    (
                        "room",
                        OrderedDict(
                            [
                                ("id", self.room.id),
                                (
                                    "name",
                                    "Nikita",
                                ),  # Замените, если у вас другое значение
                                ("host", self.user.id),
                                ("current_users", [self.user.id]),
                            ]
                        ),
                    ),
                ]
            ),
        }
        print()
        print(expected_data)
        self.assertDictEqual(data, expected_data)
