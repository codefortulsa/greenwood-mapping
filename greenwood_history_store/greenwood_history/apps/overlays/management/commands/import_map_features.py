"""Idempotent import of all known GeoJSON + shapefile sources into
`overlays.MapFeature`.

Single source of truth: every bulk-imported geometry lives as a
MapFeature row, keyed by (source, source_id) so re-running replaces
rather than duplicates. Reprojects to EPSG:4326 on load.

Sources are declared below; add new rows to `SOURCES` as more
datasets come in.
"""
from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
from django.core.management.base import BaseCommand
from django.db import transaction

from overlays.models import MapFeature


DATA_ROOT = Path(settings.BASE_DIR).parent / "data"
ASSETS = DATA_ROOT / "greenwood_assets"
SHAPES = DATA_ROOT / "shape"


@dataclass
class Source:
    path: Path
    kind: str
    source_label: str  # persisted as MapFeature.source

    # shapefiles without a reliable .prj need an override
    source_srs: Optional[str] = None

    # name / date handling
    name_field: Optional[str] = None  # read feature property as MapFeature.name
    default_name: str = ""  # used only when name_field is None or empty
    source_id_field: str = "RecNum"  # properties[<field>] -> source_id

    # fuzzy dates applied uniformly to every row from this source
    start_earliest: Optional[datetime] = None
    start_latest: Optional[datetime] = None
    end_earliest: Optional[datetime] = None
    end_latest: Optional[datetime] = None

    notes: str = ""
    # extra properties merged into each feature's .properties (source-wide)
    extra_properties: dict[str, Any] = field(default_factory=dict)


SOURCES: list[Source] = [
    # ---------- curated / historical overlays ----------
    Source(
        path=ASSETS / "tulsa-burned-area.geojson",
        kind=MapFeature.Kind.DESTRUCTION_ZONE,
        source_label="gathering_greenwood:tulsa-burned-area.geojson",
        default_name="1921 Tulsa destruction zone",
        start_earliest=datetime(1921, 5, 31, tzinfo=timezone.utc),
        start_latest=datetime(1921, 6, 1, tzinfo=timezone.utc),
        notes="Polygon of area destroyed during the Tulsa Race Massacre, 1921-05-31..06-01.",
    ),
    # ---------- historical bulk datasets ----------
    Source(
        path=ASSETS / "Greenwood_Buildings.json",
        kind=MapFeature.Kind.HISTORICAL_BUILDING,
        source_label="gathering_greenwood:Greenwood_Buildings.json",
    ),
    Source(
        path=ASSETS / "Greenwood_roads.json",
        kind=MapFeature.Kind.HISTORICAL_ROAD,
        source_label="gathering_greenwood:Greenwood_roads.json",
    ),
    Source(
        path=ASSETS / "poi-footprints.geojson",
        kind=MapFeature.Kind.POI_FOOTPRINT,
        source_label="gathering_greenwood:poi-footprints.geojson",
        name_field="name",
        source_id_field="building_id",
    ),
    # ---------- modern reference datasets ----------
    Source(
        path=ASSETS / "tulsa-building-footprints.geojson",
        kind=MapFeature.Kind.MODERN_BUILDING_FOOTPRINT,
        source_label="gathering_greenwood:tulsa-building-footprints.geojson",
    ),
    Source(
        path=SHAPES / "Parcels_20220929" / "PARCELS220929.shp",
        kind=MapFeature.Kind.PARCEL,
        source_label="tulsa_county:PARCELS220929",
        # The bundled .prj declares Oregon North SP — surprising for
        # Tulsa data, but trusting it (no -s_srs override) makes the
        # reprojection land exactly at Greenwood. Whoever built this
        # shapefile reprojected to Oregon SP math for reasons unknown;
        # the coordinates + .prj are self-consistent.
        source_id_field="OBJECTID",
    ),
    Source(
        path=SHAPES / "Quarters" / "quarter.shp",
        kind=MapFeature.Kind.QUARTER_SECTION,
        source_label="tulsa_county:quarter",
        source_srs="EPSG:2267",  # .prj says OK North SP but ogr resolved ESRI 102726
    ),
    Source(
        path=SHAPES / "Township" / "township.shp",
        kind=MapFeature.Kind.TOWNSHIP,
        source_label="tulsa_county:township",
    ),
]


class Command(BaseCommand):
    help = "Import all known GeoJSON + shapefile sources into overlays.MapFeature."

    def add_arguments(self, parser):
        parser.add_argument(
            "--only",
            nargs="*",
            help="Substring match on Source.source_label; limits to matching sources.",
        )
        parser.add_argument(
            "--clear-kind",
            action="store_true",
            help="Before inserting, delete existing MapFeature rows with the same kind.",
        )

    def handle(self, *, only=None, clear_kind=False, **_opts):
        for src in SOURCES:
            if only and not any(o in src.source_label for o in only):
                continue
            if not src.path.exists():
                self.stderr.write(self.style.ERROR(f"missing: {src.path}"))
                continue
            self._import_source(src, clear_kind=clear_kind)

    # ---------- internals ----------

    def _import_source(self, src: Source, *, clear_kind: bool):
        self.stdout.write(self.style.MIGRATE_HEADING(f"=== {src.source_label} ({src.kind}) ==="))

        # Normalize shapefiles to GeoJSON in EPSG:4326 via ogr2ogr so we
        # have one parsing path for the rest of this command.
        raw: dict
        if src.path.suffix.lower() == ".shp":
            raw = self._shp_to_geojson_dict(src)
        else:
            raw = json.loads(src.path.read_text())

        features = raw.get("features") or ([raw] if raw.get("type") == "Feature" else [])
        if not features:
            self.stderr.write(self.style.WARNING("  no features"))
            return

        if clear_kind:
            deleted, _ = MapFeature.objects.filter(kind=src.kind).delete()
            self.stdout.write(f"  cleared {deleted} existing rows of kind={src.kind}")

        with transaction.atomic():
            created = updated = 0
            for f in features:
                props = f.get("properties") or {}
                geom = GEOSGeometry(json.dumps(f["geometry"]), srid=4326)

                name = ""
                if src.name_field and props.get(src.name_field):
                    name = str(props[src.name_field])
                elif src.default_name:
                    name = src.default_name

                source_id = ""
                if props.get(src.source_id_field) is not None:
                    source_id = str(props[src.source_id_field])

                merged_props = {**src.extra_properties, **props}

                defaults = dict(
                    kind=src.kind,
                    name=name,
                    geom=geom,
                    notes=src.notes,
                    properties=merged_props,
                    start_earliest=src.start_earliest,
                    start_latest=src.start_latest,
                    end_earliest=src.end_earliest,
                    end_latest=src.end_latest,
                )

                if source_id:
                    obj, was_created = MapFeature.objects.update_or_create(
                        source=src.source_label,
                        source_id=source_id,
                        defaults=defaults,
                    )
                else:
                    # No stable key — dedupe by (source, name) if we have a
                    # name; otherwise always create.
                    if name:
                        obj, was_created = MapFeature.objects.update_or_create(
                            source=src.source_label,
                            name=name,
                            defaults=defaults,
                        )
                    else:
                        MapFeature.objects.create(source=src.source_label, **defaults)
                        created += 1
                        continue

                if was_created:
                    created += 1
                else:
                    updated += 1

        self.stdout.write(
            self.style.SUCCESS(f"  {created} created, {updated} updated")
        )

    def _shp_to_geojson_dict(self, src: Source) -> dict:
        """Use ogr2ogr to stream a shapefile to GeoJSON in 4326."""
        cmd = ["ogr2ogr", "-f", "GeoJSON", "/vsistdout/"]
        if src.source_srs:
            cmd += ["-s_srs", src.source_srs]
        cmd += ["-t_srs", "EPSG:4326", str(src.path)]

        proc = subprocess.run(cmd, capture_output=True, check=True)
        return json.loads(proc.stdout)
