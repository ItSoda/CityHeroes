from rest_framework.views import APIView

from users.models import Users
from .models import Room
from rest_framework.response import Response
from rest_framework import status
from .serializers import RoomSerializer, RoomCreateSerializer


class CreateRoom(APIView):
    serializer_class = RoomCreateSerializer
    def post(self, request, uuid):
        username = self.request.POST.get("username", "")
        url = self.request.POST.get("url", "")

        Room.objects.create(uuid=uuid, client=username, url=url)
        
        return Response({"message": "room created"}, status=status.HTTP_201_CREATED)


class ChatAdmin(APIView):
    serializer_class = RoomSerializer
    def get(self, request, *args, **kwargs):
        rooms = Room.objects.all()
        users = Users.objects.filter(is_stuff=True)

        return Response({"rooms": rooms, "users": users}, status=status.HTTP_200_OK)
    

class Room(APIView):
    serializer_class = RoomSerializer
    def get(self, request, uuid,  *args, **kwargs):
        room = Room.objects.get(uuid=uuid)

        if room.status == Room.WAITING:
            room.status = Room.ACTIVE
            room.agent = self.request.user
            room.save()

        return Response({"room": room}, status=status.HTTP_200_OK)
        



