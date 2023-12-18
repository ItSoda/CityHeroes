import json

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from yookassa.domain.notification import WebhookNotificationFactory
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView

from .serializers import UserSerializer
from users.services import (
    EmailVerificationHandler,
    create_auto_payment,
    create_payment,
    user_save_yookassa_payment_id,
    users_search,
)
from .models import Users


class UserViewSet(ModelViewSet):
    queryset = Users.object.all()
    serializer_class = UserSerializer


class UserSearchView(ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        query = self.request.query_params.get(
            "query", ""
        )  # Получите параметр запроса "query"
        # Используйте фильтр для поиска товаров по имени (или другим полям) по запросу
        queryset = users_search(query)
        return queryset


class EmailVerificationAndUserUpdateView(APIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        email_verification_handler = EmailVerificationHandler(
            code=kwargs.get("code"), email=kwargs.get("email")
        )
        email_result, user = email_verification_handler.proccess_email_verification()
        try:
            if email_result:
                return Response({"EmailVerification": user.is_verified_email})
            return Response(
                {"EmailVerification": "EmailVerification is expired or not exists"}
            )
        except Exception:
            return Response({"EmailVerification": "Произошла ошибка"})


class SubscriptionCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = self.request.user
        payment_url = create_payment(user, request)
        # Перенаправка пользователя на страницу оплаты Юкассы
        return Response(
            {
                "payment_url": payment_url,
            }
        )


class YookassaWebhookView(APIView):
    def post(self, request):
        event_json = json.loads(request.body.decode("utf-8"))
        user_id = event_json["object"]["metadata"].get("user_id")
        try:
            notification = WebhookNotificationFactory().create(event_json)
            # Проверяем статус платежа
            if notification.object.status == "succeeded":
                # Проверяем сохранен ли метод оплаты
                if notification.object.payment_method.saved:
                    # Добавляем yookassa_payment_id пользователю
                    user = user_save_yookassa_payment_id(user_id, notification)
                    create_auto_payment(user)
        except Exception as e:
            # Обработка ошибок при разборе уведомления
            return Response(
                {"message": "Payment ID не создан. Произошла ошибка"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"message": "Payment ID сохранен успешно"}, status=status.HTTP_200_OK
        )
