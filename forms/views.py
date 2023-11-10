from rest_framework.generics import CreateAPIView
from .serializers import FormAnimalSerializer
from rest_framework.permissions import IsAuthenticated


class FormAnimalCreateAPIView(CreateAPIView):
    serializer_class = FormAnimalSerializer
    permission_classes = (IsAuthenticated,)
