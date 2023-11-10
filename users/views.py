from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.services import (EmailVerificationHandler, check_last_first_name,
                            user_update_first_last_name)

from .models import User
from .serializers import UserSerializer


class EmailVerificationAndUserUpdateView(APIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        email_verification_handler = EmailVerificationHandler(
            code=kwargs.get("code"), email=kwargs.get("email")
        )
        email_result, user = email_verification_handler.proccess_email_verification()
        try:
            if email_result:
                request.session["user_id"] = user.id
                return Response({"EmailVerification": user.is_verified_email})
            return Response(
                {"EmailVerification": "EmailVerification is expired or not exists"}
            )
        except Exception:
            return Response({"EmailVerification": "Произошла ошибка"})

    def patch(self, request, *args, **kwargs):
        user_id = request.session.get(
            "user_id",
        )
        # Проверяем наличие 'first_name' и 'last_name' в данных
        if check_last_first_name(request):
            return Response(
                {"message": "Имя и Фамилия обязательны"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_update_first_last_name(user_id, request)
        return Response(
            {"message": "Имя и Фамилия добавлены"}, status=status.HTTP_200_OK
        )