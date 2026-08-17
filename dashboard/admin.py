from django.contrib import admin
from .models import UserAddressModel


@admin.register(UserAddressModel)
class UserAddressModelAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "state", "city", "phone_number")


