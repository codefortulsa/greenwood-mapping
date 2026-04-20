from django.contrib.gis import admin

from .models import MapFeature


@admin.register(MapFeature)
class MapFeatureAdmin(admin.GISModelAdmin):
    list_display = ("name", "kind", "source", "source_id", "start_earliest", "end_latest")
    list_filter = ("kind", "source")
    search_fields = ("name", "source", "source_id", "notes")
    autocomplete_fields = ("address",)
    readonly_fields = ()
