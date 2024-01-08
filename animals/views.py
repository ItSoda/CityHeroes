import logging

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
# from .services import animal_search
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.models import Users

from .models import Animals
from .serializers import (AnimalCreateSerializer, AnimalSerializer,
                          AnimalShortSerializer, FormAnimalCreateSerializer,
                          FormAnimalSerializer)

logger = logging.getLogger("main")


class AnimalModelViewSet(ModelViewSet):
    queryset = Animals.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = (AllowAny,)

    # @method_decorator(cache_page(100))
    def list(self, request, *args, **kwargs):
        self.get_serializer = AnimalSerializer
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        self.serializer_class = AnimalCreateSerializer
        return super().create(request, *args, **kwargs)


# class AnimalSearchView(viewsets.ModelViewSet):
#     queryset = Animals.objects.all()
#     serializer_class = AnimalSerializer

#     @action(detail=False, methods=['get'])
#     def search(self, request):
#         query = self.request.GET.get('query', '')
#         results = animal_search(query)

#         return Response({'results': results}, status=status.HTTP_200_OK)


class FormAnimalViewSet(ModelViewSet):
    serializer_class = FormAnimalSerializer
    permission_classes = (IsAuthenticated,)

    @method_decorator(cache_page(100))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        self.serializer_class = FormAnimalCreateSerializer
        return super().create(request, *args, **kwargs)


class AnimalFavouriteUserViewSet(APIView):
    def post(self, request, animal_id, *args, **kwargs):
        try:
            logger.info("first")
            user = Users.objects.get(id=self.request.user.id)
            logger.info("user find")
            animal = Animals.objects.get(id=animal_id)
            logger.info("animal find")

            if animal in user.favourites.all():
                user.favourites.remove(animal)
                user.quantity_favourites -= 1
            else:
                user.favourites.add(animal)
                user.quantity_favourites += 1

            user.save()

        except Exception as e:
            # Обработка ошибок при разборе уведомления
            return Response(
                {"message": "Животное не добавлено в избранное. Произошла ошибка"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"message": "Животное добавлено или удалено успешно"},
            status=status.HTTP_200_OK,
        )
