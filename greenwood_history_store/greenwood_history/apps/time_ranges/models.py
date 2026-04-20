from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _
from entities.models import Entity
from addresses.models import Address


class TimeRangeQuerySet(models.QuerySet):
    def date_in(self, date: datetime) -> "TimeRangeQuerySet":
        return self.filter(start_time__lte=date, end_time__gte=date)


class TimeRange(models.Model):
    name = models.CharField(_("Name"), max_length=120, unique=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    entities = models.ManyToManyField(
        Entity,
        through="EntityAddressTimeRangeThrough",
        related_name="ranges",
        related_query_name="range",
    )

    objects = TimeRangeQuerySet.as_manager()

    def __str__(self) -> str:
        return f"{self.name} {self.start_time:%Y-%m-%d} {self.end_time:%Y-%m-%d}"


# TODO: rename to something simpler
class EntityAddressTimeRangeThrough(models.Model):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    time_range = models.ForeignKey(TimeRange, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("entity", "time_range", "address")

    def __str__(self) -> str:
        return f"{self.entity} {self.address} {self.time_range}"
