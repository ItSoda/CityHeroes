from django.contrib import admin

from .models import FormAnimals


class FormAnimalAdmin(admin.TabularInline):
    model = FormAnimals
    fields = ("animal", "phone")
    extra = 0
