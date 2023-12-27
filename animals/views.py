from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Animals
from .permissions import IsCompanyUser
from .serializers import (AnimalCreateSerializer, AnimalSerializer,
                          AnimalShortSerializer, FormAnimalCreateSerializer)
from .services import animal_search


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


class AnimalSearchView(ListAPIView):
    serializer_class = AnimalSerializer

    def get_queryset(self):
        query = self.request.query_params.get(
            "query", ""
        )  # Получите параметр запроса "query"
        # Используйте фильтр для поиска товаров по имени (или другим полям) по запросу
        queryset = animal_search(query)
        return queryset


class FormAnimalsCreateAPIView(CreateAPIView):
    serializer_class = FormAnimalCreateSerializer
    permission_classes = (IsAuthenticated,)
