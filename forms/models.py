from django.db import models

from animals.models import Animals
from users.models import Users


class FormAnimals(models.Model):
    """Model for one FormAnimals"""

    phone = models.CharField(max_length=15)
    animal = models.ForeignKey(to=Animals, on_delete=models.CASCADE)
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Заявку"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return (
            f"Phone: {self.phone} | Animal: {self.animal.name} | {self.animal.species}"
        )
