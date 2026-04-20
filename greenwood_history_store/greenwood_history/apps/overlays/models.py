from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from core.mixins import FuzzyDateRangeMixin


class HistoricalShape(FuzzyDateRangeMixin, models.Model):
    """A polygon layer tied to a (possibly fuzzy) time window.

    Covers one-off overlays that aren't modeled as Buildings or parcels:
    the 1921 destruction zone, rebuild progression regions, historical
    neighborhood boundaries, georectified Sanborn map areas, etc.
    """

    class Kind(models.TextChoices):
        DESTRUCTION_ZONE = "destruction_zone", _("Destruction zone")
        REBUILD_PROGRESSION = "rebuild_progression", _("Rebuild progression")
        NEIGHBORHOOD_BOUND = "neighborhood_bound", _("Neighborhood boundary")
        SANBORN_AREA = "sanborn_area", _("Sanborn map area")
        OTHER = "other", _("Other")

    name = models.CharField(_("Name"), max_length=120)
    kind = models.CharField(_("Kind"), max_length=32, choices=Kind.choices)
    geom = models.MultiPolygonField(_("Geometry"), srid=4326)
    source = models.CharField(_("Source"), max_length=255, blank=True)
    notes = models.TextField(_("Notes"), blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["kind"]),
        ]

    def __str__(self) -> str:
        return f"{self.get_kind_display()}: {self.name}"
