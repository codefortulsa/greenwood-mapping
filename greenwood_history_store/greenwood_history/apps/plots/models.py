"""
Plot information stores

Current data structures/architecture

Demolished/lost structures

Street:
name
direction/side

Location/Residence:
Optionally building name
house/building number with fractions?
Street
short building description
Size/dimensions
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


Current line item data
Residence/building name
building number
building size
additional location information (tacked on to number, fractions and floor numbers) 
    Fractions
    Frame, stucco or brick house
    Floor count
connected businesses/owners, homes/apartments
loss value
"""

from django.contrib.gis.db import models


class Plot(models.Model):
    meta = models.JSONField("Metadata associated with a plot")
