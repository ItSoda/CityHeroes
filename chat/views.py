from rest_framework.views import APIView

from users.models import Users
from .models import Room
from rest_framework.response import Response
from rest_framework import status
from .serializers import RoomSerializer, RoomCreateSerializer


class CreateRoom(APIView):
    serializer_class = RoomCreateSerializer
    def post(self, request, uuid):
        try:
            username = self.request.POST.get("username", "")
            url = self.request.POST.get("url", "")

            Room.objects.create(uuid=uuid, client=username, url=url)
            
            return Response({"data": "room created"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"data": f"error - {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


class ChatAdmin(APIView):
    serializer_class = RoomSerializer
    def get(self, request, *args, **kwargs):
        try:
            rooms = Room.objects.all()
            users = Users.objects.filter(is_stuff=True)

            return Response({"rooms": rooms, "users": users}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"data": f"error - {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    

class Room(APIView):
    serializer_class = RoomSerializer
    def get(self, request, uuid,  *args, **kwargs):
        try:
            room = Room.objects.get(uuid=uuid)

            if room.status == Room.WAITING:
                room.status = Room.ACTIVE
                room.agent = self.request.user
                room.save()

            return Response({"room": room}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"data": f"error - {str(e)}"}, status=status.HTTP_404_NOT_FOUND)
        



