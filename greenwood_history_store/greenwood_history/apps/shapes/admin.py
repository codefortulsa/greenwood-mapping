from django.contrib import admin

from shapes.models import Parcels, Quarters, Townships


@admin.register(Parcels)
class ParcelsAdmin(admin.ModelAdmin):
    pass


@admin.register(Quarters)
class QuartersAdmin(admin.ModelAdmin):
    pass


@admin.register(Townships)
class TownshipsAdmin(admin.ModelAdmin):
    pass
