from django.contrib.auth.models import AbstractUser
from django.db import models
from django_elasticsearch_dsl import Document, Index

from animals.services import send_form_email
from users.services import is_expired, send_verification_email

from .managers import CustomUserManager


# User Model
class Users(AbstractUser):
    """Model for Users"""

    AGENT = "agent"
    MANAGER = "manager"

    ROLES_CHOICES = (
        (AGENT, "Agent"),
        (MANAGER, "Manager"),
    )

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    is_verified_email = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to="user_images", null=True, blank=True)
    yookassa_payment_id = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLES_CHOICES, default=AGENT)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "пользователя"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"Пользователь {self.email} | {self.first_name}"


users_index = Index("users_index")
users_index.settings(number_of_shard=1, number_of_replicas=0)

@users_index.doc_type
class UsersDocument(Document):
    class Django:
        model = Users
        fields = ["username",]


class EmailVerifications(models.Model):
    """Model for one EmailVerifications"""

    code = models.UUIDField(unique=True, null=True, blank=True)
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"EmailVerification object for {self.user.email}"

    def send_verification_email(self):
        send_verification_email(self.user.email, self.code)

    def send_form_email(self):
        send_form_email(self.user.email)

    def is_expired(self):
        is_expired(self)
