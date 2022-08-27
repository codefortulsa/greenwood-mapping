"""
Plot information stores

Current data structres/architecture

Demolished/lost structures

Street:
name
direction/side

Location/Residence:
Optionally building name
house/building number with fractions?
Street
short building description
Size/dimenions
Business name
Value

Businesses:
Business name
Owner(s)

People:
Name
Job/Occupation

Goals:
Events/occupancy tracked over time.
Source of the information is tracked. similar imports are merged or told to combine?
Names are unified and recorded 

"""

from django.db import models
from django.contrib.gis.db import models


class Building(models.Model):
    pass


class Plot(models.Model):
    meta = models.JSONField("Metadata associated with a plot")


