from django.contrib.auth.models import AbstractUser
from django.db import models

from users.services import is_expired, send_verification_email

from .managers import CustomUserManager


# User Model
class Users(AbstractUser):
    """Model for Users"""

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    is_verified_email = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to="user_images", null=True, blank=True)
    yookassa_payment_id = models.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "пользователя"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"Пользователь {self.email} | {self.first_name}"


class EmailVerifications(models.Model):
    """Model for one EmailVerifications"""

    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f"EmailVerification object for {self.user.email}"

    def send_verification_email(self):
        send_verification_email(self.user.email, self.code)

    def is_expired(self):
        is_expired(self)
