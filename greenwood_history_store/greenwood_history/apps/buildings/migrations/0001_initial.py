# Generated by Django 4.2 on 2023-04-07 02:23

import buildings.models
import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django_pydantic_field.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("addresses", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Building",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "name",
                    models.CharField(blank=True, max_length=120, null=True, verbose_name="Name"),
                ),
                (
                    "size",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.SmallIntegerField(verbose_name="ft"),
                        default=list,
                        size=2,
                    ),
                ),
                (
                    "outline",
                    django.contrib.gis.db.models.fields.PolygonField(
                        blank=True, null=True, srid=4326, verbose_name="Outline"
                    ),
                ),
                (
                    "meta",
                    django_pydantic_field.fields.PydanticSchemaField(
                        config=None, schema=buildings.models.BuildingMeta
                    ),
                ),
                (
                    "address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="addresses.address"
                    ),
                ),
            ],
        ),
    ]
