from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import FormAnimalSerializer


class FormAnimalsCreateAPIView(CreateAPIView):
    serializer_class = FormAnimalSerializer
    permission_classes = (IsAuthenticated,)
