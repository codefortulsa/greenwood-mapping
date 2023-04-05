from django.contrib import admin

from buildings.models import Building


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    pass