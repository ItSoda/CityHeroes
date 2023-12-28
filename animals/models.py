from django.db import models

from users.models import Users
from django_elasticsearch_dsl import Document, Index

class Images(models.Model):
    """Model for one images"""

    title = models.CharField("Название", max_length=100)
    image = models.ImageField(upload_to="all_images")

    class Meta:
        verbose_name = "Фотографию"
        verbose_name_plural = "Фотографии"

    def __str__(self):
        return f"Name: {self.title}"


class Animals(models.Model):
    """Model for one animal"""

    name = models.CharField("Имя", max_length=120)
    species = models.CharField("Порода", max_length=200)
    age = models.PositiveIntegerField(default=0)
    content = models.TextField()
    images = models.ManyToManyField(to=Images)
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "животное"
        verbose_name_plural = "Животные"

    def __str__(self) -> str:
        return f"Name: {self.name} | species: {self.species}"


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

# animals_index = Index("animals_index")
# animals_index.settings(number_of_shard=1, number_of_replicas=0)

# @animals_index.doc_type
# class AnimalDocument(Document):
#     class Django:
#         model = Animals
#         fields = ["name", "species", "content"]
