from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from core.mixins import FuzzyDateRangeMixin


class MapFeature(FuzzyDateRangeMixin, models.Model):
    """Generic Django-managed geometry record.

    One row per feature — any geometry type (point, line, polygon,
    multi-*). Covers bulk imports (parcels, quarter sections, modern
    footprints) *and* curated named features (1921 destruction zone,
    neighborhood boundaries). Use `Building` instead when a feature is
    an individually-curated structure with a known address, floors,
    style, or sub-tenants — `MapFeature` is for everything else.

    Provenance:
      - `source`    — human-readable origin ("gathering_greenwood
                       public/Greenwood_Buildings.json").
      - `source_id` — external id within that source (RecNum, FID,
                       parcel objectid, etc.) for traceability.
      - `properties`— pass-through JSON from the source file; avoids
                       schema churn every time we ingest a new dataset.

    Lookup:
      - `address` — optional FK for curated records. Most bulk-imported
                     rows leave this null; they're queried spatially
                     via PostGIS.
    """

    class Kind(models.TextChoices):
        # curated overlays
        DESTRUCTION_ZONE = "destruction_zone", _("Destruction zone")
        REBUILD_PROGRESSION = "rebuild_progression", _("Rebuild progression")
        NEIGHBORHOOD_BOUND = "neighborhood_bound", _("Neighborhood boundary")
        SANBORN_AREA = "sanborn_area", _("Sanborn map area")
        # bulk historical datasets
        HISTORICAL_BUILDING = "historical_building", _("Historical building footprint")
        HISTORICAL_ROAD = "historical_road", _("Historical road")
        POI_FOOTPRINT = "poi_footprint", _("Featured POI footprint")
        # modern reference datasets (spatial lookup / context)
        MODERN_BUILDING_FOOTPRINT = "modern_building_footprint", _("Modern building footprint")
        PARCEL = "parcel", _("Parcel (modern)")
        QUARTER_SECTION = "quarter_section", _("PLSS quarter section")
        TOWNSHIP = "township", _("PLSS township")
        # escape hatch
        OTHER = "other", _("Other")

    name = models.CharField(_("Name"), max_length=255, blank=True)
    kind = models.CharField(_("Kind"), max_length=40, choices=Kind.choices)
    geom = models.GeometryField(_("Geometry"), srid=4326)
    source = models.CharField(_("Source"), max_length=255, blank=True)
    source_id = models.CharField(_("Source ID"), max_length=255, blank=True)
    properties = models.JSONField(_("Properties"), default=dict, blank=True)
    notes = models.TextField(_("Notes"), blank=True)

    address = models.ForeignKey(
        "addresses.Address",
        null=True,
        blank=True,
        related_name="map_features",
        on_delete=models.PROTECT,
        help_text="Curated address linkage. Bulk imports leave null and query spatially.",
    )

    class Meta:
        indexes = [
            models.Index(fields=["kind"]),
            # re-import lookup key
            models.Index(fields=["source", "source_id"]),
        ]

    def __str__(self) -> str:
        label = self.name or f"#{self.pk}"
        return f"{self.get_kind_display()}: {label}"
