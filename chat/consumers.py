import json

from asgiref.sync import sync_to_async, async_to_sync
from channels.db import database_sync_to_async
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from djangochannelsrestframework import mixins
from djangochannelsrestframework.observer.generics import (
    ObserverModelInstanceMixin,
    action,
)
from djangochannelsrestframework.observer import model_observer

from django.db.models import Q

from .models import Room, Message, PersonalMessage
from users.models import Users
from .serializers import MessageSerializer, RoomSerializer, UserSerializer


class RoomConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = "pk"

    async def disconnect(self, code):
        if hasattr(self, "room_subscribe"):
            await self.remove_user_from_room(self.room_subscribe)
            await self.notify_users()
        await super().disconnect(code)

    @action()
    async def join_room(self, pk, **kwargs):
        self.room_subscribe = pk
        await self.add_user_to_room(pk)
        await self.notify_users()

    @action()
    async def leave_room(self, pk, **kwargs):
        await self.remove_user_from_room(pk)

    @action()
    async def create_message(self, message, image=None, **kwargs):
        room: Room = await self.get_room(pk=self.room_subscribe)
        await database_sync_to_async(Message.objects.create)(
            room=room, sender=self.scope["user"], text=message, image=image
        )

    @action()
    async def subscribe_to_messages_in_room(self, pk, **kwargs):
        await self.message_activity.subscribe(room=pk)

    @model_observer(Message)
    async def message_activity(self, message, observer=None, **kwargs):
        await self.send_json(message)

    @message_activity.groups_for_signal
    def message_activity(self, instance: Message, **kwargs):
        yield f"room__{instance.room_id}"
        yield f"pk__{instance.pk}"

    @message_activity.groups_for_consumer
    def message_activity(self, room=None, **kwargs):
        if room is not None:
            yield f"room__{room}"

    @message_activity.serializer
    def message_activity(self, instance: Message, action, **kwargs):
        return dict(
            data=MessageSerializer(instance).data, action=action.value, pk=instance.pk
        )

    async def notify_users(self):
        room: Room = await self.get_room(self.room_subscribe)
        for group in self.groups:
            await self.channel_layer.group_send(
                group,
                {"type": "update_users", "usuarios": await self.current_users(room)},
            )

    async def update_users(self, event: dict):
        await self.send(text_data=json.dumps({"usuarios": event["usuarios"]}))

    @database_sync_to_async
    def get_room(self, pk: int) -> Room:
        return Room.objects.get(pk=pk)

    @database_sync_to_async
    def current_users(self, room: Room):
        return [UserSerializer(user).data for user in room.current_users.all()]

    @database_sync_to_async
    def remove_user_from_room(self, room):
        user: Users = self.scope["user"]
        user.current_rooms.remove(room)

    @database_sync_to_async
    def add_user_to_room(self, pk):
        user: Users = self.scope["user"]
        if not user.current_rooms.filter(pk=self.room_subscribe).exists():
            user.current_rooms.add(Room.objects.get(pk=pk))


class UserConsumer(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.PatchModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    mixins.DeleteModelMixin,
    GenericAsyncAPIConsumer,
):
    queryset = Users.objects.all()
    serializer_class = UserSerializer


import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import PersonalMessage


# class PersonalChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data['message']
#         sender_id = data['sender_id']
#         receiver_id = data['receiver_id']

#         # Save the message to the database
#         await self.save_message(sender_id, receiver_id, message)

#         # Send the message to the receiver's personal chat
#         await self.send_personal_message(sender_id, receiver_id, message)

#     @sync_to_async
#     def save_message(self, sender_id, receiver_id, message):
#         sender = Users.objects.get(id=sender_id)
#         receiver = Users.objects.get(id=receiver_id)

#         Message.objects.create(sender=sender, receiver=receiver, text=message)

#     @sync_to_async
#     def get_user_channel_name(self, user_id):
#         # Generate a unique channel name for the user
#         return f"user{user_id}"

#     async def send_personal_message(self, sender_id, receiver_id, message):
#         receiver_channel_name = await self.get_user_channel_name(receiver_id)

#         # Send the message to the receiver's channel
#         await self.channel_layer.send(
#             receiver_channel_name,
#             {
#                 'type': 'personal.message',
#                 'message': message,
#                 'sender_id': sender_id,
#             }
#         )

#     async def personal_message(self, event):
#         message = event['message']
#         sender_id = event['sender_id']

#         # Send the message to the connected client
#         await self.send(text_data=json.dumps({
#             'message': message,
#             'sender_id': sender_id,
#         }))