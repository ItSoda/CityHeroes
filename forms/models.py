from django.db import models
from animals.models import Animal
from users.models import User


class FormAnimal(models.Model):
    animal = models.ForeignKey(to=Animal, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=25)
