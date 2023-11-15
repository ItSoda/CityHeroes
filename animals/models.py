from django.db import models

from companies.models import Companies, Images


class Animals(models.Model):
    """Model for one animal"""

    name = models.CharField("Имя", max_length=120)
    species = models.CharField("Порода", max_length=200)
    age = models.PositiveIntegerField(default=0)
    content = models.TextField()
    images = models.ManyToManyField(to=Images)
    company = models.ForeignKey(to=Companies, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "животное"
        verbose_name_plural = "Животные"

    def __str__(self) -> str:
        return f"Name: {self.name} | species: {self.species}"
