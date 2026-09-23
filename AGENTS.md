# AGENTS.md — POWRobots

## What this repo does

POWRobots collects, normalises, and preserves physical-economy data for the UK robotics market. It is a Layer 1 data garden — it captures reality, it doesn't model it.

## How to run

```bash
# Install
pip install -e ".[dev]"

# Initialize database
python3 -m powrobots.shared.db

# Seed source rights and registry
python3 -m powrobots.cli seed

# Run all collectors
python3 -m powrobots.cli collect all

# Check status
python3 -m powrobots.cli health
python3 -m powrobots.cli robots

# Run tests
POWROBOTS_DB=/tmp/test.db python3 -m pytest tests/ -v
```

## How POWOps monitors this repo

POWOps reads `collector_run` and `source_health` tables from `warehouse/powrobots.db` via the `collector_db` health check.

```yaml
# In powops sources.yaml:
powrobots:
  path: /home/ubuntu/powrobots
  health_check: collector_db
  db_path: warehouse/powrobots.db
```

### What powops checks

1. Opens `warehouse/powrobots.db`
2. Queries `collector_run` for latest row per source
3. Compares `started_at` against `max_staleness` (72h)
4. Returns status: ok, stale, error, no_key, unknown

### Status values

| Status | Meaning |
|--------|---------|
| ok | Last run within staleness, no errors |
| stale | Last run exceeded max_staleness |
| error | Last run had errors |
| no_key | API key env var not set |
| unknown | No runs recorded |

## CLI commands

| Command | Description |
|---------|-------------|
| `powrobots status` | Row counts per table |
| `powrobots sources` | List registered sources |
| `powrobots seed` | Seed source_rights + source_registry |
| `powrobots collect <source>` | Run a collector |
| `powrobots collect all` | Run all collectors |
| `powrobots health` | Last collector run per source |
| `powrobots robots` | Entity graph summary |
| `powrobots models` | List robot models |
| `powrobots components` | List components |
| `powrobots organisations` | List organisations |
| `powrobots validate` | Check everything is wired |

## Collectors

### Active (no auth, fetching live data)

| Source | Records | What it collects |
|--------|---------|-----------------|
| hmrc_traders | 561 | UK businesses trading HS 847950 (industrial robots) |
| opss_safety | 50 | Product safety alerts (machinery) |
| contracts_finder | 20 | Government procurement notices |
| hmrc_trade | 1 | Trade statistics index |
| ukri_gtr | 0 | Research projects (already collected) |
| bgs_minerals | 1 | Mineral statistics |
| ons_ppi | 1 | Price indices |
| bara_directory | 1 | Integrator directory (JS-blocked) |
| find_apprenticeship | 1 | Apprenticeship landing page (JS-blocked) |
| rbtx | 2 | Robot marketplace (JS-blocked) |

### Needs API key

| Source | Env var | Parser | Status |
|--------|---------|--------|--------|
| companies_house | COMPANIES_HOUSE_API_KEY | Complete | Working (250 companies) |
| mouser | MOUSER_API_KEY | Complete | Needs key |
| farnell | FARNELL_API_KEY | Complete | Needs key |
| lcsc | LCSC_API_KEY | Complete | Needs key |
| ebay_uk | EBAY_APP_ID | Complete (has bug) | Needs OAuth |

## Entity graph

| Table | Count | What |
|-------|-------|------|
| organisation | 856 | Companies, traders, buyers |
| robot_model | 123 | Robot models from seeds + vendor repos |
| robot_manufacturer | 26 | Manufacturer profiles |
| component | 32 | Tracked components (servos, controllers, etc.) |
| product_relation | 29 | Robot→component relationships |
| component_manufacturer | 23 | Component→manufacturer links |

### Query the entity graph

```bash
powrobots robots          # Summary
powrobots models          # All 123 models
powrobots components      # All 32 components
powrobots organisations   # First 50 organisations
```

## How to add a new collector

1. Create `powrobots/collectors/<name>.py`
2. Subclass `BaseCollector`
3. Set `SOURCE_ID`, `DATASET`, `PARSER_ID`
4. Implement `fetch()` → return bytes or None
5. Implement `parse(raw_content, raw_hash, result)` → call `insert_source_record()` + `upsert_*()`
6. Add to `COLLECTORS` dict in `cli.py`
7. Add to powops `sources.yaml` under `powrobots` garden with `health.check: collector_db`
8. Run `python3 -m powrobots.cli seed`
9. Run `python3 -m powrobots.cli collect <source_id>`
10. powops sees it immediately

## How to add a new API-key source

1. Register for API key
2. Set env var: `export COMPANIES_HOUSE_API_KEY=xxx`
3. Implement `fetch()` in the collector
4. Test: `python3 -m powrobots.cli collect <source_id>`
5. powops reports `no_key` until env var is set, then `ok`/`error`

## Key files

| File | Purpose |
|------|---------|
| `powrobots/cli.py` | CLI entry point |
| `powrobots/collectors/base.py` | Base collector + retry + raw storage |
| `powrobots/collectors/*.py` | 15 source collectors |
| `powrobots/shared/db.py` | SQLite schema + seed data |
| `powrobots/shared/persist.py` | Storage + entity graph + health |
| `powrobots/seeds/*.yml` | Seed data (manufacturers, components, stocks) |
| `tests/test_core.py` | 42 tests |
| `docs/BUILD_NOTES.md` | Complete build documentation |
| `docs/threads.md` | Open threads and decisions |
| `docs/blockers.md` | Tracked blockers |
| `HANDOVER.md` | What exists and what to do next |

## Blockers (see docs/blockers.md)

1. Mouser/Farnell/LCSC need API keys
2. eBay needs OAuth setup
3. BARA/RBTX/apprenticeships are JS-rendered
4. HMRC trade stats, ONS PPI need parsers
5. powops can't query entity graph (by design)

## Design principles

1. **Layer 1 only** — no economics, no modelling
2. **Raw preservation** — content-addressed, gzip, append-only
3. **Entity graph** — manufacturers, models, components, relations
4. **Rights-gated** — source_rights table controls collection
5. **POWOps integration** — collector_run + source_health tables
6. **Boring** — simple file reads, no ML, no dashboards-within-dashboards
