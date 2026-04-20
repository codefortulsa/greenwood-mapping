"""Seed overlays.HistoricalShape from known GeoJSON files.

Idempotent — keyed by `name`. Safe to run repeatedly.
"""
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon
from django.core.management.base import BaseCommand

from overlays.models import HistoricalShape


DATA_DIR = Path(settings.BASE_DIR).parent / "data" / "greenwood_assets"


@dataclass
class Seed:
    path: str
    name: str
    kind: str
    source: str
    start_earliest: Optional[datetime] = None
    start_latest: Optional[datetime] = None
    end_earliest: Optional[datetime] = None
    end_latest: Optional[datetime] = None
    notes: str = ""


SEEDS: list[Seed] = [
    Seed(
        path="tulsa-burned-area.geojson",
        name="1921 Tulsa destruction zone",
        kind=HistoricalShape.Kind.DESTRUCTION_ZONE,
        source="codefortulsa/gathering_greenwood: public/tulsa-burned-area.geojson",
        start_earliest=datetime(1921, 5, 31, tzinfo=timezone.utc),
        start_latest=datetime(1921, 6, 1, tzinfo=timezone.utc),
        notes="Polygon of area destroyed during the Tulsa Race Massacre, "
        "May 31–June 1, 1921. End date left null — semantically the "
        "'zone existed' from then forward; rebuild progression is a "
        "separate HistoricalShape.",
    ),
]


class Command(BaseCommand):
    help = "Seed overlays.HistoricalShape from known GeoJSON files in data/greenwood_assets/."

    def handle(self, *args, **options):
        for seed in SEEDS:
            path = DATA_DIR / seed.path
            if not path.exists():
                self.stderr.write(self.style.ERROR(f"missing file: {path}"))
                continue

            raw = json.loads(path.read_text())
            geom = self._to_multipolygon(raw)

            obj, created = HistoricalShape.objects.update_or_create(
                name=seed.name,
                defaults=dict(
                    kind=seed.kind,
                    geom=geom,
                    source=seed.source,
                    notes=seed.notes,
                    start_earliest=seed.start_earliest,
                    start_latest=seed.start_latest,
                    end_earliest=seed.end_earliest,
                    end_latest=seed.end_latest,
                ),
            )
            verb = "created" if created else "updated"
            self.stdout.write(self.style.SUCCESS(f"{verb}: {obj}"))

    @staticmethod
    def _to_multipolygon(raw: dict) -> MultiPolygon:
        """Accept a FeatureCollection or single Feature; promote to MultiPolygon."""
        if raw.get("type") == "FeatureCollection":
            geoms = [GEOSGeometry(json.dumps(f["geometry"])) for f in raw["features"]]
        elif raw.get("type") == "Feature":
            geoms = [GEOSGeometry(json.dumps(raw["geometry"]))]
        else:
            geoms = [GEOSGeometry(json.dumps(raw))]

        polys: list = []
        for g in geoms:
            if g.geom_type == "MultiPolygon":
                polys.extend(list(g))
            elif g.geom_type == "Polygon":
                polys.append(g)
            else:
                raise ValueError(f"unexpected geometry type: {g.geom_type}")
        return MultiPolygon(polys, srid=4326)
