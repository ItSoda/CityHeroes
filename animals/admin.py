from django.contrib import admin

from .models import Animals


@admin.register(Animals)
class AnimalsAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "species")
    ordering = ("species",)
    filter_horizontal = ["images"]
