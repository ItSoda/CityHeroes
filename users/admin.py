from django.contrib import admin
from .models import User, EmailVerification
from forms.admin import FormAnimalAdmin


class EmailVerificationAdmin(admin.TabularInline):
    model = EmailVerification
    fields = ("expiration",)
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name")
    inlines = (FormAnimalAdmin, EmailVerificationAdmin)
    readonly_fields = ("last_login", "date_joined")


