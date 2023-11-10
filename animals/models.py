from django.db import models


class Animal(models.Model):
    """Model for one animal"""

    name = models.CharField("Имя", max_length=120)
    species = models.CharField("Порода", max_length=200)
    age = models.PositiveIntegerField(default=0)
    content = models.TextField()
    image = models.ImageField(upload_to="animals_images")

    class Meta:
        verbose_name = "животное"
        verbose_name_plural = "Животные"

    def __str__(self) -> str:
        return f"Name: {self.name} | species: {self.species}"
