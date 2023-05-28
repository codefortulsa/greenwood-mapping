# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.gis.db import models


class Parcels(models.Model):
    gid = models.AutoField(primary_key=True)
    objectid = models.FloatField(blank=True, null=True)
    shape_length = models.DecimalField(
        db_column="shape_leng", max_digits=65535, decimal_places=65535, blank=True, null=True
    )
    shape_area = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    subdivision = models.CharField(db_column="subdivisio", max_length=254, blank=True, null=True)
    block = models.IntegerField(blank=True, null=True)
    lot = models.IntegerField(blank=True, null=True)
    geom = models.MultiPolygonField(srid=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "parcels"

    def __str__(self) -> str:
        return f"Parcel {self.gid} {self.objectid}"


class Quarters(models.Model):
    gid = models.AutoField(primary_key=True)
    area = models.FloatField(blank=True, null=True)
    perimeter = models.FloatField(blank=True, null=True)
    plotindex = models.FloatField(db_column="plotindex_", blank=True, null=True)
    plotindex_3 = models.FloatField(db_column="plotindex___3", blank=True, null=True)
    twprge = models.CharField(max_length=2, blank=True, null=True)
    sec = models.CharField(max_length=2, blank=True, null=True)
    qtrnum = models.CharField(max_length=2, blank=True, null=True)
    indchar = models.CharField(max_length=1, blank=True, null=True)
    mapnum = models.CharField(max_length=3, blank=True, null=True)
    qtrchar = models.CharField(max_length=2, blank=True, null=True)
    township = models.CharField(max_length=2, blank=True, null=True)
    range = models.CharField(max_length=2, blank=True, null=True)
    avtf = models.CharField(max_length=3, blank=True, null=True)
    geom = models.MultiPolygonField(srid=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "quarters"

    def __str__(self) -> str:
        return f"Quarter {self.gid} {self.area}"


class Townships(models.Model):
    gid = models.AutoField(primary_key=True)
    area = models.FloatField(blank=True, null=True)
    perimeter = models.FloatField(blank=True, null=True)
    tile_name = models.CharField(max_length=32, blank=True, null=True)
    twprge = models.CharField(max_length=5, blank=True, null=True)
    geom = models.MultiPolygonField(srid=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "townships"

    def __str__(self) -> str:
        return f"Township {self.gid} {self.area}"
