from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.timezone import now


# MODELS METHODS
# EMAIL VERIFICATION
def send_verification_email(user_email, code):
    link = reverse("users:email_verify", kwargs={"email": user_email, "code": code})
    full_link = f"{settings.DOMAIN_NAME}{link}"
    subjects = f"Подтверждение учетной записи для {user_email}"
    message = "Для подтверждения электронной почты {} перейдите по ссылке: {}.".format(
        user_email,
        full_link,
    )
    send_mail(
        subject=subjects,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False,
    )


def is_expired(self):
    if now() >= self.expiration:
        self.delete()
        self.save()
        return True
    return False


# VIEWS
class EmailVerificationHandler:
    def __init__(self, code, email):
        self.code = code
        self.email = email

    def proccess_email_verification(self):
        from users.models import EmailVerifications, Users

        user = get_object_or_404(Users, email=self.email)
        email_verifications = EmailVerifications.objects.filter(
            code=self.code, user=user
        )
        try:
            if (
                email_verifications.exists()
                and not email_verifications.last().is_expired()
            ):
                user.is_verified_email = True
                user.save()
                return True, user
            return False
        except Exception as e:
            return False


# YOOKASSA PAYMENT
def create_payment(user, request):
    from django.conf import settings
    from yookassa import Configuration, Payment

    # Настройте ключи доступа
    Configuration.account_id = settings.YOOKASSA_SHOP_ID
    Configuration.secret_key = settings.YOOKASSA_SECRET_KEY
    # Создайте объект платежа
    payment = Payment.create(
        {
            "amount": {"value": "2000.00", "currency": "RUB"},
            "payment_method_data": {"type": "bank_card"},
            "confirmation": {
                "type": "redirect",
                "return_url": settings.YOOKASSA_REDIRECT_URL,
            },
            "capture": True,
            "description": f"Платеж для пользователя {user.email}",
            "save_payment_method": True,
            "metadata": {"user_id": str(request.user.id)},
        }
    )
    return payment.confirmation.confirmation_url


def user_save_yookassa_payment_id(user_id, notification):
    from users.models import Users

    user = Users.objects.get(id=user_id)

    user.yookassa_payment_id = notification.object.payment_method.id
    user.save()
    return user


def create_auto_payment(user):
    from datetime import datetime, timedelta

    from yookassa import Configuration, Payment

    Configuration.account_id = settings.YOOKASSA_SHOP_ID
    Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

    start_date = (datetime.utcnow() + timedelta(days=30)).isoformat()
    auto_payment = Payment.create(
        {
            "amount": {"value": "100.00", "currency": "RUB"},
            "payment_method_id": f"{user.yookassa_payment_id}",
            "description": f"Подписка на услугу для пользователя {user.email}",
            "interval": "month",
            "start_date": start_date,
            "metadata": {"user_id": str(user.id)},
        }
    )
