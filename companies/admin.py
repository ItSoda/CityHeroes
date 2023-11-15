from django.contrib import admin

from .models import Companies, Images


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ("name", "image")
    ordering = ("name",)


@admin.register(Companies)
class CompaniesAdmin(admin.ModelAdmin):
    list_display = ("name",)
    ordering = ("name",)
    filter_horizontal = ["users", "images"]
