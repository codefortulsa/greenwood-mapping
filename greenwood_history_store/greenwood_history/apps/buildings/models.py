import logging
from enum import Enum
from typing import Optional

from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from django_pydantic_field import SchemaField
from pydantic import BaseModel

from addresses.models import Address
from core.mixins import FuzzyDateRangeMixin


logger = logging.getLogger(__name__)


class BuildingTypes(str, Enum):
    FRAME = "frame"
    BRICK = "brick"
    STUCCO = "stucco"


class BuildingMeta(BaseModel):
    style: Optional[BuildingTypes] = BuildingTypes.FRAME
    floors: Optional[int] = 1


def default_building_meta() -> BuildingMeta:
    return BuildingMeta(style=BuildingTypes.FRAME, floors=1)


class Building(FuzzyDateRangeMixin, models.Model):
    """A building with an outline, fuzzy existence window, and optional
    parent (for multi-unit / sub-tenant addresses)."""

    name = models.CharField(_("Name"), max_length=120, null=True, blank=True)
    size = ArrayField(models.SmallIntegerField(_("ft")), size=2, default=list)
    outline = models.PolygonField(_("Outline"), blank=True, null=True)
    meta: BuildingMeta = SchemaField(default=default_building_meta)

    address = models.ForeignKey(
        Address, blank=False, null=False, on_delete=models.PROTECT, related_name="buildings"
    )
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="sub_units",
        help_text="Parent building for sub-tenants / multi-unit addresses.",
    )

    def __str__(self) -> str:
        if self.name:
            return f"{self.name} ({self.address})"
        return f"{self.meta.style} @ {self.address}"
