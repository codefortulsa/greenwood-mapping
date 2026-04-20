# Open design threads

Small, not-yet-resolved ideas that don't justify their own doc.
Collected from scratch notes (the former `greenwood_history_store/temp.py`)
and ad-hoc observations. Promote to the main design when ready.

## Occupation / profession controlled vocab (future)

HistoryForge uses a `Vocabulary` + `Term` pattern for controlled
vocabularies (occupations, race, place of birth, language). We
deferred this in the schema redesign as "nice-to-have." When we're
ready, the Polk directory occupation strings we've observed so far
are a natural seed list — many are abbreviated forms of the same
thing and would collapse nicely into canonical Terms:

- grocer / grocers
- tailor / tailors
- physician / physic / phsici
- restaurant / restaura / resta
- lawyer
- dressmaker / dressma
- soft drinks / softdr
- laundry
- barber
- shoeshiner / shoesh / shoemaker
- garage
- real estate / real est.
- contractor / contracto
- photographer / photo
- confectioner / confec. / conf
- druggist
- dentist
- plumber
- furniture / fumi
- billiards / bulliards
- cleaner / cleane / cleaners

For the import pipeline, apply these as aliases to a single canonical
`Term` per concept. Storing the original string on the through record
preserves source fidelity.

## Null-source-value normalization (already implemented)

Polk directories use several "no data" strings interchangeably:
`address not listed`, `not listed`, `street not listed`. The
interpretation of "street not listed" is ambiguous — could mean the
street is destroyed, gone, or didn't exist yet. Current import path
treats all three as null (see
`greenwood_history_store/notebooks/const.py` and the
`null_values` list in the `import_data` management command). Revisit
if we want to preserve the distinction (e.g. for the 1922 directory
where "street not listed" is more likely destruction-related).

## Fields we don't yet model (observed in plots/models.py docstring)

The vestigial `plots` app (to be deleted during the schema rebuild)
held a docstring with a few data points we haven't yet covered:

- **Loss value** — 1921 massacre loss-claim dollar amounts per
  building. Not in current schema. Would be a natural field on
  `Building` or a dedicated `LossClaim` model if we eventually ingest
  the Parrish / claim records.
- **Address fractions** (e.g. `123 1/2 N Greenwood`) — Polk sometimes
  uses these for alley units or rear addresses. `Address.number` is
  currently a `DecimalField(10,2)` so fractions serialize fine (123.50
  round-trips), but we should verify the import normalization
  preserves the `1/2` vs. treating it as `number_additional`.
- Frame/stucco/brick + floor count — already covered by
  `buildings.BuildingMeta.style` and `BuildingMeta.floors`.
- Source-of-information provenance — already broadly covered by
  `TimeRange` (per-source windows) and planned for
  `AddressHistoryEvent.source_document`; worth a once-over when we
  design import pipelines to make sure every fact has a traceable
  source row.

## EventType resolution (closed)

An earlier scratch note wanted a generic `EventType` enum with values
like `LOST` / `NOT_LISTED`. That concern is now covered by
`AddressHistoryEvent.reason` for address-level events and
`HistoricalShape.kind` for polygon-level events. Fuzzy date ranges
cover the "appeared sometime in X" case. No separate EventType model
needed.
