from django.contrib.gis import admin

from .models import HistoricalShape


@admin.register(HistoricalShape)
class HistoricalShapeAdmin(admin.GISModelAdmin):
    list_display = ("name", "kind", "start_earliest", "end_latest")
    list_filter = ("kind",)
    search_fields = ("name", "source", "notes")
