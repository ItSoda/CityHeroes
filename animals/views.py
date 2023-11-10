from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Animal
from .serializers import AnimalSerializer
from rest_framework.permissions import AllowAny
from .services import animal_search


class AnimalsListAPIView(ListAPIView):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = (AllowAny,)


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
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = (AllowAny,)
