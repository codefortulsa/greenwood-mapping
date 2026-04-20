from typing import Optional

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicModel
from nameparser import HumanName
import pgtrigger
import pghistory


@pghistory.track(
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
    model_name="BusinessEvent",
    fields=("proprietor",),
    context_field=pghistory.ContextForeignKey(related_query_name="person_events"),
)
class Business(Entity):
    proprietor = models.ForeignKey(Person, null=True, blank=True, on_delete=models.SET_NULL)


class EntityMerge(models.Model):
    """Audit row for a soft-merge: absorbed entity -> surviving entity.

    The absorbed entity keeps all of its relationships — merging just
    sets `Entity.canonical` to the survivor and flips `Entity.active`
    to False on the loser. `Entity` deletes are blocked by pgtrigger,
    so no data goes away.

    Reverting clears `canonical`, re-activates the loser, and flips
    `status` to REVERTED. A single entity can only have one ACTIVE
    merge event; the UniqueConstraint enforces it.
    """

    class Status(models.TextChoices):
        ACTIVE = "active", _("Active")
        REVERTED = "reverted", _("Reverted")

    surviving_entity = models.ForeignKey(
        Entity,
        related_name="absorbed_merges",
        on_delete=models.PROTECT,
    )
    merged_entity = models.ForeignKey(
        Entity,
        related_name="merge_event",
        on_delete=models.PROTECT,
    )
    reason = models.TextField(_("Reason"), blank=True)

    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="entity_merges_performed",
        on_delete=models.PROTECT,
    )
    performed_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        _("Status"),
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    reverted_at = models.DateTimeField(null=True, blank=True)
    reverted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="entity_merges_reverted",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["merged_entity"],
                condition=models.Q(status="active"),
                name="only_one_active_merge_per_entity",
            ),
            models.CheckConstraint(
                condition=~models.Q(surviving_entity=models.F("merged_entity")),
                name="cannot_merge_entity_into_itself",
            ),
        ]

    def __str__(self) -> str:
        arrow = "→" if self.status == self.Status.ACTIVE else "↩"
        return f"{self.merged_entity} {arrow} {self.surviving_entity} ({self.status})"
