from django.contrib import admin

from .models import Address, AddressHistoryEvent, Street


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    list_display = ("name", "direction", "type")
    list_filter = ("direction", "type")
    search_fields = ("name",)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("number", "number_additional", "street")
    list_filter = ("number_additional", "street")
    search_fields = ("number", "street__name")
    autocomplete_fields = ("street",)


@admin.register(AddressHistoryEvent)
class AddressHistoryEventAdmin(admin.ModelAdmin):
    list_display = ("from_address", "to_address", "reason", "effective_date")
    list_filter = ("reason",)
    search_fields = ("source_document", "notes")
    autocomplete_fields = ("from_address", "to_address")
