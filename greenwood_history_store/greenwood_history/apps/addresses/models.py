import logging
import re
from typing import Optional

from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

# Date ranges addresses existed
# Provide model that tracks larger segments when addresses existed


class ActiveRanges:
    """What date ranges this information was active for."""

    pass


logger = logging.getLogger(__name__)


class Directions(models.TextChoices):
    NORTH = "N", _("North")
    WEST = "W", _("West")
    SOUTH = "S", _("South")
    EAST = "E", _("East")


allowed_directions = Directions.values


class StreetTypes(models.TextChoices):
    AVE = "ave", _("Avenue")
    BLVD = "blvd", _("Boulevard")
    ST = "st", _("Street")
    PL = "pl", _("Place")


allowed_types = StreetTypes.values

street_type_map = dict(zip(StreetTypes.labels, StreetTypes.values))


def silent(type: models.TextChoices, value):
    if value is None:
        return ""
    try:
        return type(value).label
    except ValueError:
        return ""


street_pattern = re.compile(
    r"^(?i)(?P<street_name>[a-z]+)(?:-(?P<direction1>N|S|E|W))?(?:\s+(?P<street_type>[A-Za-z]+\.?)?)?(?:-(?P<direction2>N|S|E|W)?)?$"
)


def parse_street_name(name: str):
    def prim(bad_name: str):
        return bad_name.strip().title()

    matches = street_pattern.match(name)

    if matches:
        name, direction1, street_type, direction2 = matches.group(
            "street_name", "direction1", "street_type", "direction2"
        )
        direction = direction1 or direction2
        direction = None if direction is None else direction.upper()
        street_type = (
            StreetTypes.ST.value
            if street_type is None
            else prim(street_type).lower().removesuffix(".")
        )
        return (prim(name), direction, street_type)
    return None


class Street(models.Model):
    name = models.CharField(_("Name"), max_length=120)
    type = models.CharField(
        _("Type"),
        max_length=4,
        blank=True,
        null=True,
        choices=StreetTypes.choices,
        default=StreetTypes.ST.value,
    )
    direction = models.CharField(
        _("Direction"), max_length=1, blank=True, null=True, choices=Directions.choices
    )

    def __str__(self) -> str:
        return f"{self.name} {silent(StreetTypes, self.type)} {silent(Directions, self.direction)}".strip()

    @classmethod
    def get_or_create_from_name(cls, name: str):
        orig_name = name
        extra = dict()
        parts = parse_street_name(name)
        try:
            if parts is not None:
                (name, direction, street_type) = parts
                if street_type is not None:
                    assert street_type in allowed_types, "bad type"
                if direction is not None:
                    assert direction in allowed_directions, "bad direction"
                extra = dict(direction=direction, type=street_type)
        except AssertionError as e:
            logger.debug(f"Bad parse of name {orig_name}", exc_info=e)
        return cls.objects.get_or_create(name=name, **extra)


class Address(models.Model):
    """Addresses store a unique street/number combo for an active range"""

    number = models.DecimalField(
        _("Number"), max_digits=10, decimal_places=2, null=True, blank=True
    )
    number_additional = models.CharField(max_length=120, null=True, blank=True)
    street = models.ForeignKey(Street, blank=False, null=False, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f"{self.number:} {self.number_additional} {self.street}"

    @classmethod
    def get_or_create_from_unique(
        cls, street: Optional[Street] = None, number: Optional[str] = None, **kwargs
    ):
        def split(s: str):
            return (
                "".join(c for c in s if c.isdigit()) or None,
                "".join(c for c in s if c.isalpha() or c.isspace()) or None,
            )

        # TODO? Handle case where additional information is places
        # TODO move this validation into some sort of input basemodel?
        if number is None or street is None:
            raise Exception("didn't define unique values.")

        split_number, letters = split(number)
        # number additional may include "rear" phrases to indicate a back door.

        return cls.objects.get_or_create(
            street=street, number=split_number, number_additional=letters, defaults=kwargs
        )


outline = models.PolygonField(_("Outline"), blank=True, null=True)
