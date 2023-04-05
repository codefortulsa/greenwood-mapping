import logging

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


street_type_map = dict(zip(StreetTypes.labels, StreetTypes.values))


def silent(type: models.TextChoices, value):
    if value is None:
        return ""
    try:
        return type(value).label
    except ValueError:
        return ""


class Street(models.Model):
    name = models.CharField(_("Name"), max_length=120)
    type = models.CharField(_("Type"), max_length=4,
                            blank=True, null=True, choices=StreetTypes.choices)
    direction = models.CharField(
        _("Direction"), max_length=1, blank=True, null=True, choices=Directions.choices
    )

    def __str__(self) -> str:
        return f"{self.name} {silent(Directions, self.direction)} {silent(StreetTypes, self.type)}".strip()

    @classmethod
    def get_or_create_from_name(cls, name: str):
        def prim(bad_name: str):
            return bad_name.strip().title()
        try:
            (split_name, direction) = name.split("-")
            direction = direction.strip().upper()
            assert direction in allowed_directions
            return cls.objects.get_or_create(
                name=prim(split_name), direction=direction
            )
        except ValueError:
            logger.debug("%s", name, exc_info=e)
        except AssertionError as e:
            logger.debug("Assertion failure on: %s", name, exc_info=e)
        finally:
            # Always get or create with provided name if we haven't returned yet
            return cls.objects.get_or_create(name=prim(name), direction=None)


class Address(models.Model):
    """Addresses store a unique street/number combo for an active range"""
    number = models.DecimalField(_("Number"), max_digits=10, decimal_places=2)
    number_additional = models.CharField(max_length=120, null=True, blank=True)
    street = models.ForeignKey(
        Street, blank=False, null=False, on_delete=models.PROTECT)
    
    def __str__(self) -> str:
        return f"{self.number:} {self.number_additional} {self.street}"

    @classmethod
    def get_or_create_from_unique(cls, street: Street = None, number: str = None, **kwargs):
        def split(s: str):
            return (''.join(c for c in s if c.isdigit()) or None,
                    ''.join(c for c in s if c.isalpha() or c.isspace()) or None)

        # TODO? Handle case where additional information is places
        # TODO move this validation into some sort of input basemodel?
        if number is None or street is None:
            raise Exception("didn't define unique values.")

        split_number, letters = split(number)

        return cls.objects.get_or_create(street=street, number=split_number, number_additional=letters, defaults=kwargs)


outline = models.PolygonField(_("Outline"), blank=True, null=True)
