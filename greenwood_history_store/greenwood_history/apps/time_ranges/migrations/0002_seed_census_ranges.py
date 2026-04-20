"""Seed TimeRange rows for directory/census years we ingest (1919-1923).

Exact dates: `start_earliest == start_latest`, `end_earliest == end_latest`.
The FuzzyDateRangeMixin fields treat equal earliest/latest as an exact date.
"""
from datetime import datetime, timezone

from django.db import migrations


SEED_YEARS = range(1919, 1924)


def seed(apps, schema_editor):
    TimeRange = apps.get_model("time_ranges", "TimeRange")
    for year in SEED_YEARS:
        start = datetime(year, 1, 1, tzinfo=timezone.utc)
        end = datetime(year + 1, 1, 1, tzinfo=timezone.utc)
        TimeRange.objects.get_or_create(
            name=str(year),
            defaults=dict(
                start_earliest=start,
                start_latest=start,
                end_earliest=end,
                end_latest=end,
            ),
        )


def unseed(apps, schema_editor):
    TimeRange = apps.get_model("time_ranges", "TimeRange")
    TimeRange.objects.filter(name__in=[str(y) for y in SEED_YEARS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("time_ranges", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
