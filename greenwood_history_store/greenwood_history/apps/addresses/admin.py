from django.contrib import admin

from .models import Street, Address


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    list_display = ("name", "direction", "type")
    list_filter = ("direction", "type")


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("number", "number_additional", "street")
    list_filter = ("number_additional", "street")
