import logging
from enum import Enum
from typing import Optional

from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from pydantic import BaseModel
from django_pydantic_field import SchemaField

from addresses.models import Address


logger = logging.getLogger(__name__)


class BuildingTypes(str, Enum):
    FRAME = "frame"
    BRICK = "brick"
    STUCCO = "stucco"


class BuildingMeta(BaseModel):
    style: Optional[BuildingTypes] = BuildingTypes.FRAME.value
    floors: Optional[int] = 1


default_building_meta = lambda: BuildingMeta(style=BuildingTypes.FRAME.value, floors=1)


class Building(models.Model):
    """Model that represents basic building information and outline."""

    # map_id = models.  # TODO: unique ID reference to source data for outline
    name = models.CharField(_("Name"), max_length=120, null=True, blank=True)
    size = ArrayField(models.SmallIntegerField(_("ft")), size=2, default=list)
    outline = models.PolygonField(_("Outline"), blank=True, null=True)
    meta: BuildingMeta = SchemaField()
    address = models.ForeignKey(
        Address, blank=False, null=False, on_delete=models.PROTECT)

    def __str__(self) -> str:
        if self.name is not None:
            return f"{self.name} {self.address}"
        return f"{self.meta.style} {self.address}"
