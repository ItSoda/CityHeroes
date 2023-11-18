from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .models import Animals
from .serializers import AnimalSerializer
from .services import animal_search


class AnimalsListAPIView(ListAPIView):
    queryset = Animals.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = (AllowAny,)

    @method_decorator(cache_page(70))
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class AnimalSearchView(ListAPIView):
    serializer_class = AnimalSerializer

    def get_queryset(self):
        query = self.request.query_params.get(
            "query", ""
        )  # Получите параметр запроса "query"
        # Используйте фильтр для поиска товаров по имени (или другим полям) по запросу
        queryset = animal_search(query)
        return queryset


class AnimalRetrieveAPIView(RetrieveAPIView):
    queryset = Animals.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = (AllowAny,)
