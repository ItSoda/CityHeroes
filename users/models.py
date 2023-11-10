from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from users.services import is_expired, send_verification_email

from .managers import CustomUserManager


# User Model
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_verified_email = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "пользователя"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"Пользователь {self.email} | {self.first_name}"


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f"EmailVerification object for {self.user.email}"

    def send_verification_email(self):
        send_verification_email(self.user.email, self.code)

    def is_expired(self):
        is_expired(self)