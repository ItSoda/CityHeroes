from django.contrib import admin
from .models import FormAnimal


class FormAnimalAdmin(admin.TabularInline):
    model = FormAnimal
    fields = ("animal", "phone")
    extra = 0
