from typing import Optional
from django.db import models
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicModel
from nameparser import HumanName
import pgtrigger
import pghistory


@pghistory.track(
    pghistory.Snapshot(),
    model_name="EntityEvent",
    fields=("name", "meta", "canonical"),
    context_field=pghistory.ContextForeignKey(related_query_name="entity_events"),
)
class Entity(PolymorphicModel):
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=120)
    meta = models.JSONField(default=dict, blank=True)
    canonical = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ("-id",)
        # TODO: trigger to manage only updating canonical and restricts to only updates if canonical
        # is not set on the target, canonical also must be on the same type only.
        triggers = [
            pgtrigger.ReadOnly(name="read_only_fields", fields=["name"]),
            pgtrigger.Protect(name="protect_deletes", operation=pgtrigger.Delete),
        ]
        verbose_name_plural = "entities"

    def __str__(self) -> str:
        return self.name

    # def record_losses(self):
    #     pass


@pghistory.track(
    pghistory.Snapshot(),
    model_name="PersonEvent",
    fields=("name_parsed",),
    context_field=pghistory.ContextForeignKey(related_query_name="person_events"),
)
class Person(Entity):
    """Entity that represents a unique person."""

    _parsed_name_field = "parsed_name"
    name_parsed = models.BooleanField(default=False)

    @property
    def full_name(self):
        name_meta = self.meta.get(self._parsed_name_field)
        return f'{name_meta.get("first")} {name_meta.get("last")}'

    def update_name_meta(self, name: Optional[HumanName] = None):
        if name is None:
            name = HumanName(self.name)
        self.meta.update({self._parsed_name_field: name.as_dict()})
        return self

    def update_name_meta_from_parts(self, **parts):
        # first=None, middle=None, last=None, title=None, suffix=None
        # HumanName._members
        name = HumanName(**parts)
        self.meta.update({self._parsed_name_field: name.as_dict()})
        return self

    def name_from_parts(self, first, middle, last):
        name = HumanName()
        name.first = first
        name.middle = middle
        name.last = last
        self.name = name.full_name
        self.update_name_meta(name)
        return name

    def save(self, *args, **kwargs):
        # Temp, update meta name data on save.
        self.update_name_meta()
        self.name_parsed = True
        super().save(*args, **kwargs)


@pghistory.track(
    pghistory.Snapshot(),
    model_name="BusinessEvent",
    fields=("proprietor",),
    context_field=pghistory.ContextForeignKey(related_query_name="person_events"),
)
class Business(Entity):
    proprietor = models.ForeignKey(Person, null=True, blank=True, on_delete=models.SET_NULL)
