# POWRobots

UK-first physical-economy data garden for robotics.

Part of the [POW Systems](https://pow.systems) project.

## What this is

A data collection framework that monitors the physical economics of robotics in the UK: who makes robots, what parts they use, what they cost, who imports them, who repairs them, and where the bottlenecks are.

## What this is not

- A robotics news site
- A stock screener
- A dashboard
- An AI chatbot
- A robot comparison site

## Quick start

```bash
# Install
pip install -e ".[dev]"

# Initialize database
python3 -m powrobots.shared.db

# Seed source rights and registry
python3 -m powrobots.cli seed

# Run all collectors
python3 -m powrobots.cli collect all

# Check what powops sees
python3 -m powrobots.cli health

# Run tests
POWROBOTS_DB=/tmp/test.db python3 -m pytest tests/ -v
```

## Architecture

```
Collectors → Raw storage → Source records → Entity graph
     ↓                                        ↓
collector_run                    powops monitors via collector_db
     ↓                                        ↓
powops health                  MCP / Dashboard / CLI
```

### Key files

| Path | Purpose |
|------|---------|
| `powrobots/cli.py` | CLI entry point (15 collectors, seed/health/status) |
| `powrobots/collectors/base.py` | Base collector with retry/backoff/raw storage |
| `powrobots/collectors/*.py` | 15 source collectors |
| `powrobots/shared/db.py` | SQLite schema + seed data |
| `powrobots/shared/persist.py` | Storage + entity graph operations |
| `powrobots/core/enums.py` | Domain enums (RobotType, ComponentCategory) |
| `powrobots/seeds/*.yml` | Seed data (manufacturers, components, stocks) |
| `scripts/seed_loader.py` | Entity graph seeder |
| `tests/test_core.py` | 42 tests |
| `docs/` | Documentation |

### Collectors

| Source | Status | Records | Parser |
|--------|--------|---------|--------|
| hmrc_traders | ok | 561 | CSV |
| companies_house | ok | 250 | JSON API |
| opss_safety | ok | 50 | HTML |
| contracts_finder | ok | 20 | HTML |
| hmrc_trade | ok | 1 | HTML stub |
| ukri_gtr | ok | 0 | XML |
| bara_directory | ok | 1 | JS-blocked |
| bgs_minerals | ok | 1 | HTML stub |
| ons_ppi | ok | 1 | HTML stub |
| find_apprenticeship | ok | 1 | JS-blocked |
| rbtx | ok | 2 | JS-blocked |
| companies_house | no_key | — | Need API key |
| mouser | no_key | — | Need API key |
| farnell | no_key | — | Need API key |
| lcsc | no_key | — | Need API key |
| ebay_uk | no_key | — | Need API key |

### Entity graph

| Table | Count | Source |
|-------|-------|--------|
| organisation | 856 | 561 HMRC traders + 250 Companies House + 20 buyers + 25 seeds |
| robot_model | 123 | Seed loader (YAML + vendor repos) |
| robot_manufacturer | 26 | Seed loader |
| component | 32 | Seed loader (component basket) |
| product_relation | 29 | Seed loader |

### Database

SQLite at `warehouse/powrobots.db` with 32 tables:

- Data lake: `raw_blob`, `raw_acquisition`, `source_record`, `collector_run`, `source_health`
- Entity graph: `organisation`, `robot_manufacturer`, `robot_model`, `component`, `product_relation`
- Market: `market_listing`, `market_observation`, `component_market_observation`
- UK trade: `uk_trade_record`
- Government: `procurement_notice`, `grant_project`

## powops integration

POWOps monitors all 15 sources via `collector_db` health check against `warehouse/powrobots.db`.

```bash
# What powops sees
python3 -m powops status | grep powrobots

# MCP tool
powops_status(garden="powrobots")

# Web API
GET /api/status  # includes powrobots sources
```

## Documentation

| Document | Purpose |
|----------|---------|
| `AGENTS.md` | Wiring guide for powops agent |
| `docs/BUILD_NOTES.md` | Complete build notes and current state |
| `docs/devplan.md` | 8-phase development roadmap |
| `docs/devplanresponse.md` | Audit mapped to global POW devplan |
| `docs/repair-outcome-vision.md` | Repair-decision intelligence vision |
| `docs/blockers.md` | Tracked blockers with status |
| `docs/threads.md` | All open threads and decisions |
| `docs/northstar.md` | Master design document (2496 lines) |
| `docs/review.md` | Design review with phase gating |
| `docs/API_KEYS.md` | API key inventory |

## Running tests

```bash
# All tests (uses temp DB, no side effects)
POWROBOTS_DB=/tmp/test.db python3 -m pytest tests/ -v

# Specific test class
POWROBOTS_DB=/tmp/test.db python3 -m pytest tests/test_core.py::TestCollectors -v

# With ruff lint
ruff check powrobots/ tests/
```

## Deployment

```bash
# Systemd timer (6h collection cycle)
cp deploy/systemd/*.service ~/.config/systemd/user/
cp deploy/systemd/*.timer ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now powrobots-collect.timer
```

## How to add a new collector

1. Create `powrobots/collectors/<name>.py`
2. Subclass `BaseCollector`
3. Set `SOURCE_ID`, `DATASET`, `PARSER_ID`
4. Implement `fetch()` → return bytes or None
5. Implement `parse()` → call `insert_source_record()` + `upsert_*()`
6. Add to `COLLECTORS` dict in `cli.py`
7. Add to powops `sources.yaml` under `powrobots` garden
8. Run `python3 -m powrobots.cli seed`
9. Run `python3 -m powrobots.cli collect <source_id>`
