from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status, viewsets
# from .services import animal_search
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Animals
from .serializers import (AnimalCreateSerializer, AnimalSerializer,
                          AnimalShortSerializer, FormAnimalCreateSerializer)


class AnimalModelViewSet(ModelViewSet):
    queryset = Animals.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = (AllowAny,)

    @method_decorator(cache_page(100))
    def list(self, request, *args, **kwargs):
        self.get_serializer = AnimalShortSerializer
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        self.get_serializer = AnimalCreateSerializer
        return super().create(request, *args, **kwargs)


# class AnimalSearchView(viewsets.ModelViewSet):
#     queryset = Animals.objects.all()
#     serializer_class = AnimalSerializer

#     @action(detail=False, methods=['get'])
#     def search(self, request):
#         query = self.request.GET.get('query', '')
#         results = animal_search(query)

#         return Response({'results': results}, status=status.HTTP_200_OK)


class FormAnimalsCreateAPIView(CreateAPIView):
    serializer_class = FormAnimalCreateSerializer
    permission_classes = (IsAuthenticated,)
