from django.contrib import admin

from .models import Animals, FormAnimals, Images


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ("name", "image")
    ordering = ("name",)


@admin.register(Animals)
class AnimalsAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "species")
    ordering = ("species",)
    filter_horizontal = ["images"]


class FormAnimalAdmin(admin.TabularInline):
    model = FormAnimals
    fields = ("animal", "phone")
    extra = 0
