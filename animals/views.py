from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from .models import Animals
from .permissions import IsCompanyUser
from .serializers import AnimalSerializer
from .services import animal_search


class AnimalModelViewSet(ModelViewSet):
    queryset = Animals.objects.all()
    serializer_class = AnimalSerializer

    def get_permissions(self):
        if self.action == "create" or self.action == "destroy":
            permission_classes = [IsCompanyUser, IsAdminUser]
        elif self.action == "list":
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

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
