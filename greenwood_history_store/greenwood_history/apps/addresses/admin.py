from django.contrib import admin

from .models import Street, Address


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    list_display = ("name", "direction", "type")
    list_filter = ("direction", "type")


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass
