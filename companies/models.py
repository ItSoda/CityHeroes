from django.db import models

from users.models import Users


class Images(models.Model):
    """Model for one images"""

    name = models.CharField("Название", max_length=100)
    image = models.ImageField(upload_to="all_images")

    class Meta:
        verbose_name = "Фотографию"
        verbose_name_plural = "Фотографии"

    def __str__(self):
        return f"Name: {self.name}"


class Companies(models.Model):
    """Model for one companies"""

    name = models.CharField("Название", max_length=150)
    description = models.TextField(default="Описание компании")
    users = models.ManyToManyField(to=Users)
    images = models.ManyToManyField(to=Images)

    class Meta:
        verbose_name = "Компанию"
        verbose_name_plural = "Компании"

    def __str__(self):
        return f"Name: {self.name} | main_user = {self.users.first()}"
