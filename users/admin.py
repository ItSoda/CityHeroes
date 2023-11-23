from django.contrib import admin

from animals.admin import FormAnimalAdmin

from .models import EmailVerifications, Users


class EmailVerificationAdmin(admin.TabularInline):
    model = EmailVerifications
    fields = ("expiration",)
    extra = 0


@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name")
    inlines = (FormAnimalAdmin, EmailVerificationAdmin)
    readonly_fields = ("last_login", "date_joined")
