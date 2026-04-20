# Schema redesign

Design baked-in after the round of decisions on merge, address versioning,
fuzzy dates, and seed bootstrap. This doc drives the migration rebuild.

## Resolved decisions

| Area | Decision |
|---|---|
| Merge | Soft-merge via `Entity.canonical` + `Entity.active=False`; no delete, no FK repoint |
| Merge audit | `EntityMerge` table with `performed_by`/`reason`/`reverted_at`/`reverted_by`; no JSON snapshots |
| Merge UI | Django admin action only; no HTMX multi-step flow |
| Service layer | Skip — merge is a short admin handler; no `FK_REGISTRY` |
| Address versioning | `AddressHistoryEvent` (chain of events) |
| Fuzzy dates | Four fields per range: `start_earliest/start_latest/end_earliest/end_latest` |
| Fuzzy applies to | `TimeRange`, `Building`, `HistoricalShape` (new) — via abstract mixin |
| Building parent/child | Yes, `parent` self-FK for sub-units/tenants |
| Seeds | `seeds/` = curated fixtures + spatial pg_dump; `data/` = raw source |
| Workflows | `just bootstrap` (fast seed load) vs. `just reimport` (full pipeline rerun) |
| Migrations | **Zero out all existing app migrations**; regenerate fresh `0001_initial.py` per app |
| `performed_by` | `ForeignKey(django.contrib.auth.User)` for now |

## New model / field details

### `FuzzyDateRangeMixin` (abstract)

```python
class FuzzyDateRangeMixin(models.Model):
    start_earliest = models.DateTimeField(null=True, blank=True)
    start_latest   = models.DateTimeField(null=True, blank=True)
    end_earliest   = models.DateTimeField(null=True, blank=True)
    end_latest     = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    @property
    def start_is_estimated(self) -> bool:
        return (self.start_earliest or self.start_latest) and \
               self.start_earliest != self.start_latest

    @property
    def end_is_estimated(self) -> bool:
        return (self.end_earliest or self.end_latest) and \
               self.end_earliest != self.end_latest
```

Rendering/animation rules:

- **Exact:** `earliest == latest` → hard fade-in/out on that date.
- **Fuzzy:** `earliest != latest` → animate a gradient between the two dates.
- **Open-ended end (still exists/unknown):** both end fields `NULL`.
- **Clickable always** — fuzziness affects styling, not interactability.

### `Entity` (updated)

Keep existing polymorphic `Entity → Person, Business`. Keep `canonical` self-FK (existing) — now actively used for merge. Keep `active` boolean (existing). Keep `pgtrigger.Protect(delete)` and `pgtrigger.ReadOnly(name)` — soft-merge respects both.

Manager helper so queries auto-resolve through `canonical`:

```python
class EntityManager(PolymorphicManager):
    def resolved(self):
        # Follows canonical one hop; chains are disallowed by the merge action.
        return self.select_related("canonical")
```

Merge invariant (enforced in admin action): the survivor's `canonical` must be `None`. No chains.

### `EntityMerge` (new)

```python
class EntityMerge(models.Model):
    surviving_entity = models.ForeignKey(Entity, related_name="absorbed_merges", on_delete=models.PROTECT)
    merged_entity    = models.ForeignKey(Entity, related_name="merge_event", on_delete=models.PROTECT)
    reason           = models.TextField(blank=True)
    performed_by     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+")
    performed_at     = models.DateTimeField(auto_now_add=True)
    status           = models.CharField(choices=[("active","Active"),("reverted","Reverted")], default="active", max_length=10)
    reverted_at      = models.DateTimeField(null=True, blank=True)
    reverted_by      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+", null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["merged_entity"], condition=models.Q(status="active"),
                                    name="only_one_active_merge_per_entity"),
        ]
```

Admin actions:

- **"Merge selected into…"** — appears when ≥2 entities are selected. Prompts for survivor + reason, sets `canonical` and `active=False` on losers, writes one `EntityMerge` row each.
- **"Revert merge"** — on the `EntityMerge` changelist. Clears `canonical`, sets `active=True`, flips `status`.

### `AddressHistoryEvent` (new, in `addresses`)

```python
class AddressHistoryEvent(models.Model):
    class Reason(models.TextChoices):
        REBUILT_1921         = "rebuilt_1921",         _("Post-massacre rebuild (1921)")
        URBAN_RENEWAL        = "urban_renewal",        _("Urban Renewal")
        IDL_CONSTRUCTION     = "idl_construction",     _("I-244/IDL construction")
        STREET_RENAMED       = "street_renamed",       _("Street renamed")
        ROUTINE_RENUMBERING  = "routine_renumbering",  _("Routine renumbering")
        OTHER                = "other",                _("Other")

    from_address    = models.ForeignKey(Address, related_name="+", null=True, blank=True, on_delete=models.PROTECT)
    to_address      = models.ForeignKey(Address, related_name="+", null=True, blank=True, on_delete=models.PROTECT)
    effective_date  = models.DateField()
    reason          = models.CharField(max_length=32, choices=Reason.choices)
    source_document = models.CharField(max_length=255, blank=True)
    notes           = models.TextField(blank=True)
```

- Either endpoint may be null (address ceased to exist / appeared from nowhere).
- Walk forward/backward via recursive CTE or Python helper to map between eras.
- Most addresses carry zero events; events exist for historically disrupted ones.

### `Address` / `Street` (minor)

No structural change to `Address` (still `number` + `street`). `Street` keeps current fields. Historical transformations live in `AddressHistoryEvent`.

### `Building` (updated)

- Add `parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.PROTECT, related_name="sub_units")` — sub-tenants and apartment-style entries.
- Inherit `FuzzyDateRangeMixin` — fields become existence-window (`start_*` = built, `end_*` = destroyed/removed).
- Keep PostGIS `PolygonField` outline and pydantic `BuildingMeta`.

### `TimeRange` (updated)

- Drop the exact `start_time` / `end_time` fields.
- Inherit `FuzzyDateRangeMixin`.
- Seed migration (`0002_add_census_ranges` equivalent) populates `start_earliest == start_latest` and `end_earliest == end_latest` for known directory years.

### `HistoricalShape` (new app: `overlays`)

For the destruction zone, rebuild progression, and any future historical
polygon overlays (Sanborn map layers, neighborhood boundaries by year, etc.).

```python
class HistoricalShape(FuzzyDateRangeMixin, models.Model):
    class Kind(models.TextChoices):
        DESTRUCTION_ZONE    = "destruction_zone",    _("Destruction zone")
        REBUILD_PROGRESSION = "rebuild_progression", _("Rebuild progression")
        NEIGHBORHOOD_BOUND  = "neighborhood_bound",  _("Neighborhood boundary")
        OTHER               = "other",               _("Other")

    name   = models.CharField(max_length=120)
    kind   = models.CharField(max_length=32, choices=Kind.choices)
    geom   = models.MultiPolygonField(srid=4326)
    source = models.CharField(max_length=255, blank=True)
    notes  = models.TextField(blank=True)
```

Initial load: `tulsa-burned-area.geojson` → `HistoricalShape(kind=destruction_zone, start_earliest=1921-05-31, start_latest=1921-06-01, end_earliest=null, end_latest=null)`.

## Seed bootstrap

Two explicitly-distinct flows. The `just` recipes make the difference obvious.

### Directory layout

```
data/                       # raw source (xlsx, csv, shapefiles, geojson) — LFS
  Combined_PolkDirectory_1920.xlsx
  Combined_PolkDirectory_1921.xlsx
  Combined_PolkDirectory_1922.xlsx
  residents.csv
  businesstrr.csv
  shape/                    # county parcels/quarters/townships
  greenwood_assets/         # GeoJSON pulled from gathering_greenwood/public/
    tulsa-burned-area.geojson
    tulsa-building-footprints.geojson
    ...

seeds/
  relational/               # Django fixtures (dumpdata)
    streets.json
    addresses.json
    entities.json
    buildings.json
    time_ranges.json
    entity_address_time_range.json
    entity_merges.json
    address_history_events.json
    historical_shapes.json
  spatial/                  # pg_dump --data-only of unmanaged tables
    parcels.sql
    quarters.sql
    townships.sql
  README.md                 # "regenerated by just export-seeds; do not hand-edit"
```

### `just` recipes (the two flows are not interchangeable)

```just
# ------ Quick contributor bootstrap -----------------------------------
# Use this when you want a working dev database with curated data in ~30s.
# Does NOT re-run the import pipeline. Just loads pre-curated seeds.
bootstrap:
    docker compose up -d db redis
    just manage migrate
    just manage loaddata seeds/relational/*.json
    docker compose exec -T db psql -U postgres -d greenwood_history \
      < seeds/spatial/parcels.sql
    docker compose exec -T db psql -U postgres -d greenwood_history \
      < seeds/spatial/quarters.sql
    docker compose exec -T db psql -U postgres -d greenwood_history \
      < seeds/spatial/townships.sql

# ------ Full re-import from raw sources -------------------------------
# Use this when you change import logic, add source files, or want to
# verify the pipeline end-to-end. SLOW. Wipes the DB.
reimport: prune
    docker compose up -d db redis
    just manage migrate
    # shape imports via shp2pgsql
    just import-shapes
    # polk xlsx import pipeline
    just manage import_polk
    # residents/businesses csv
    just manage import_data
    # geojson assets into overlays + buildings
    just manage import_geojson data/greenwood_assets/

# ------ Export curated state back to seeds ----------------------------
# After a curation session (merges, edits), run this and commit seeds/.
export-seeds:
    just manage dumpdata \
      addresses entities buildings time_ranges overlays \
      --indent 2 --natural-foreign --natural-primary \
      -o seeds/relational/combined.json
    docker compose exec -T db pg_dump -U postgres --data-only \
      -t parcels    -d greenwood_history > seeds/spatial/parcels.sql
    docker compose exec -T db pg_dump -U postgres --data-only \
      -t quarters   -d greenwood_history > seeds/spatial/quarters.sql
    docker compose exec -T db pg_dump -U postgres --data-only \
      -t townships  -d greenwood_history > seeds/spatial/townships.sql
```

Commit rule: `seeds/` only changes via `just export-seeds`; hand edits are
forbidden. Reviewers diff fixtures to see what curation decisions a PR makes.

## Migration rebuild plan

Because the user has no database data to preserve, we restart migrations
cleanly after the module upgrade:

1. Upgrade deps (Python/Django/PostGIS/pydantic) and get `poetry install` green.
2. `git rm -r greenwood_history/apps/*/migrations/0*.py` — keep each app's
   `migrations/__init__.py`.
3. Edit models to the shape described above.
4. `poetry run python manage.py makemigrations` — one fresh
   `0001_initial.py` per app.
5. Add a `0002_seed_time_ranges.py` RunPython-style seed matching the
   previous census-year seed.
6. `poetry run python manage.py migrate` against a fresh PG17+PostGIS DB
   container — verify clean.
7. Populate `seeds/` with minimal fixtures so `just bootstrap` works
   end-to-end.

## Admin action spec (merge)

Short enough to live inline rather than in a service layer:

```python
@admin.action(description="Merge selected entities…")
def merge_entities(modeladmin, request, queryset):
    # Intermediate page: choose survivor + reason. On POST:
    survivor = Entity.objects.get(pk=request.POST["survivor"])
    reason = request.POST.get("reason", "")
    losers = queryset.exclude(pk=survivor.pk)
    with transaction.atomic():
        for loser in losers:
            EntityMerge.objects.create(
                surviving_entity=survivor, merged_entity=loser,
                reason=reason, performed_by=request.user,
            )
            loser.canonical = survivor
            loser.active = False
            loser.save()
    modeladmin.message_user(request, f"Merged {losers.count()} into {survivor}.")
```

Revert sits on the `EntityMerge` changelist as an inverse action.
