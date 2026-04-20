from datetime import datetime

from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from addresses.models import Address
from core.mixins import FuzzyDateRangeMixin
from entities.models import Entity


class TimeRangeQuerySet(models.QuerySet):
    def date_in(self, date: datetime) -> "TimeRangeQuerySet":
        """Return ranges whose (fuzzy) window contains `date`.

        Uses the widest interpretation: the date must be >= the earliest
        start and <= the latest end (nulls treated as open-ended).
        """
        return self.filter(
            Q(start_earliest__isnull=True) | Q(start_earliest__lte=date),
        ).filter(
            Q(end_latest__isnull=True) | Q(end_latest__gte=date),
        )


class TimeRange(FuzzyDateRangeMixin, models.Model):
    name = models.CharField(_("Name"), max_length=120, unique=True)

    entities = models.ManyToManyField(
        Entity,
        through="EntityAddressTimeRangeThrough",
        related_name="ranges",
        related_query_name="range",
    )

    objects = TimeRangeQuerySet.as_manager()

    def __str__(self) -> str:
        start = self.start_earliest.date() if self.start_earliest else "?"
        end = self.end_latest.date() if self.end_latest else "?"
        return f"{self.name} {start} — {end}"


class EntityAddressTimeRangeThrough(models.Model):
    """(entity × address × time_range) join — who lived/worked where, when."""

    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    time_range = models.ForeignKey(TimeRange, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("entity", "time_range", "address")

    def __str__(self) -> str:
        return f"{self.entity} @ {self.address} during {self.time_range}"
