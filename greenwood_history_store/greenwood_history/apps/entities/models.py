from email.policy import default
from typing import Optional
from django.db import models
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicModel
from nameparser import HumanName


# A person can belong to many addresses
# meta: age, occupation, notes, full name, occupation
# class 

# A business


# How to accomplish history? Maybe residential history 
# It looks like we have yearly granularity at the moment.

# import null values
# "address not listed",
# "not listed",
# "street not listed",  # could mean street is gone or destroyed or didn't exist yet.
# job mapping
jobs = [
    "grocer",
    "grocers",
    "tailors",
    "physician",
    "restaurant",
    "restaura",
    "resta",
    "laywer",
    "dressma",
    "softdr",
    "phsici",
    "laundry",
    "barber",
    "tailor",
    "shoeshiner",
    "shoesh",
    "garage",
    "real estate",
    "real est."
    "shoemaker",
    "contracto",
    "photo",
    "confectioner",
    "confec.",
    "conf",
    "druggist",
    "physician",
    "physic",
    "dentist",
    "plumber",
    "fumi",
    "bulliards",
    "cleane",
    "cleaner",
    "cleaners",
]

"""
A history item that logs when a state changes for a given entity. start stop dates or just a date records and type?
What would the query look like to capture a date that exists between two dates?  say you ask if it existed, 
do you just check that there is an existed event before a destroyed event and then allow that result to show up?
"""


class Entity(PolymorphicModel):
    name = models.CharField(max_length=120)
    meta = models.JSONField(default=dict, blank=True)
    canonical = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return self.name


class Person(Entity):
    _parsed_name_field = "parsed_name"
    "Handles name parsing and job + relations."
    name_parsed = models.BooleanField(default=True)

    def update_name_meta(self, name: Optional[HumanName] = None):
        if name is None:
            name = HumanName(self.name)
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

    # TODO: human name object from meta?


class Business(Entity):
    pass


class EventType(models.TextChoices):
    LOST = "L", _("Lost")
    NOT_LISTED = "NL", _("Not listed")


class Event(models.Model):
    date = models.DateField()
    type = models.CharField(max_length=2)


def import_entity(item):
    pass

"""
unique Id to call back and refer back to an entity that changes over time.
Start with a simple event structure, not too complex.
streets names changes
"""