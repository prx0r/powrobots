# BUILD_NOTES.md — POWRobots

Complete build notes from initial setup through current state.

---

## Environment

```
VPS:        ubuntu@<host>
Python:     3.12.3
OS:         Linux (ubuntu)
Repo:       /home/ubuntu/powrobots
DB:         /home/ubuntu/powrobots/warehouse/powrobots.db
Tests:      42/42 passing
```

### Dependencies

```
# Runtime
requests>=2.31
beautifulsoup4>=4.12
lxml>=5.0

# Dev
pytest>=7.0
ruff>=0.1
```

Install:
```bash
pip install --break-system-packages beautifulsoup4 lxml
pip install -e ".[dev]"
```

---

## What was built

### Phase 0: Kernel + Seeds (initial push)

**Schema** — 32 tables auto-applied on every `get_db()` call:
- Data lake: `raw_blob`, `raw_acquisition`, `source_record`, `source_cursor`, `collector_run`, `source_health`, `source_rights`
- Entity graph: `organisation`, `robot_manufacturer`, `robot_family`, `robot_model`, `component_manufacturer`, `component`, `component_category`, `distributor`
- BOM/relations: `product_relation`
- Market: `market_listing`, `market_observation`, `component_market_observation`
- UK trade: `uk_trade_record`
- Government: `procurement_notice`, `grant_project`
- Skills: `apprenticeship_listing`, `job_listing`
- Safety: `safety_notice`
- Corporate: `deployment_evidence`, `company_filing`
- Change: `change_event`
- ROS: `robot_description`

**Collectors** — 15 collectors implemented, all inheriting from `BaseCollector`:
- Retry with exponential backoff (3 attempts)
- Rate-limit detection (429)
- Raw storage: gzip-compressed, SHA256-named files
- Acquisition receipts linking raw blobs to collection runs
- Source record versioning with payload-hash dedup
- Rights-gated collection

**Seed data** — YAML files:
- `manufacturers.yml` — 25 robot manufacturers
- `component_categories.yml` — 25 BOM categories
- `component_basket.yml` — ~35 tracked components
- `hs_codes.yml` — 12 robotics-relevant HS codes
- `ros_repositories.yml` — 5 ROS/URDF repos
- `chinese_stocks.yml` — 7 Chinese robotics stocks
- `china_production.yml` — NBS production statistics
- `search_terms.yml` — search vocabulary

**Vendor repos** — 7 cloned:
- `abb/` — ABB ROS-Industrial
- `awesome-robot-descriptions/` — Community robot descriptions
- `fanuc_description/` — FANUC ROS descriptions
- `kuka_robot_descriptions/` — KUKA ROS2 descriptions
- `mujoco_menagerie/` — MuJoCo simulation models
- `universal_robot/` — Universal Robots ROS
- `urdf_files_dataset/` — URDF file collection

**Entity graph seed** — `scripts/seed_loader.py`:
- 30 organisations (manufacturers)
- 26 robot manufacturers
- 123 robot models (from YAML + vendor repos)
- 32 components (from component basket)
- 29 product relations

### Phase 1: POWOps wiring + Data quality

**POWOps integration:**
- All 15 sources added to `sources.yaml` under `powrobots` garden
- Health check type: `collector_db` against `warehouse/powrobots.db`
- `collector_run` table schema matches powops query exactly
- powops correctly reports: 10 `ok`, 5 `no_key`
- Systemd timer: 6h collection cycle
- Full end-to-end verified: collect → powops check → dashboard

**Source rights + registry:**
- 15 sources seeded in `source_rights` (10 open, 5 approved)
- 15 sources seeded in `source_registry` with authority, category, cadence, tier
- CLI `seed` command populates both tables idempotently
- CLI `health` command shows last collector run per source

**Systemd deployment:**
- `deploy/systemd/powrobots-collect.service` — oneshot, runs all collectors
- `deploy/systemd/powrobots-collect.timer` — 6h cycle, persistent
- `scripts/collect-all.sh` — wrapper script

**CI:**
- `.github/workflows/ci.yml` — pytest + ruff on Python 3.11/3.12

### Phase 1: Structured parsers (3 collectors rewritten)

**HMRC traders** (`hmrc_traders.py`):
- Before: Raw HTML stored as 1 evidence record
- After: CSV parser extracts 561 unique traders
- Each trader upserted as `organisation` entity with type `trader`
- CSV endpoint: `/umbraco/api/searchdownload/traders?commodities=847950`
- Dedup by company name (same company appears multiple times for different months)

**Contracts Finder** (`contracts_finder.py`):
- Before: Metadata-only records (search term + content length)
- After: HTML parser extracts 20 contract notices
- Fields: notice_id, title, buyer, url, procurement_stage, notice_status, closing_date, contract_location, contract_value, publication_date
- Each buyer upserted as `organisation` entity with type `buyer`

**OPSS safety** (`opss_safety.py`):
- Before: Raw HTML stored as 1 evidence record
- After: HTML parser extracts 50 safety alerts
- Fields: alert_id, title, alert_type, risk_level, product_category, date_published, url

---

## Current data state

```
organisation:              606 (561 HMRC + 24 seed + 20 buyers + 1 other)
robot_manufacturer:         26
robot_model:               123
component:                  32
product_relation:           29
source_record:             652
collector_run:              20
raw_blob:                   21 (~356KB)
```

### Per-source status

| Source | Status | Records | Parser | Notes |
|--------|--------|---------|--------|-------|
| hmrc_traders | ok | 561 | CSV | 561 UK businesses trading HS 847950 |
| hmrc_trade | ok | 1 | HTML stub | Trade statistics index page — needs parser |
| ukri_gtr | ok | 0 | XML | Fetches but no new results (already collected) |
| contracts_finder | ok | 20 | HTML | 20 procurement notices with buyer/value |
| opss_safety | ok | 50 | HTML | 50 safety alerts with type/risk/category |
| bara_directory | ok | 1 | HTML stub | JS-rendered — can't parse static HTML |
| bgs_minerals | ok | 1 | HTML stub | Minerals statistics page — needs parser |
| ons_ppi | ok | 1 | HTML stub | Price indices page — needs parser |
| find_apprenticeship | ok | 1 | HTML stub | Landing page — JS required |
| rbtx | ok | 2 | metadata | JS-rendered product listings — needs API |
| companies_house | no_key | 0 | fetch stub | Parser ready, fetch() not implemented |
| mouser | no_key | 0 | fetch stub | Parser ready, fetch() not implemented |
| farnell | no_key | 0 | fetch stub | Parser ready, fetch() not implemented |
| lcsc | no_key | 0 | fetch stub | Parser ready, fetch() not implemented |
| ebay_uk | no_key | 0 | fetch stub | Parser ready, fetch() not implemented |

---

## How collectors work

### Collection pipeline

```
1. check_source_rights(source_id)
   → source_rights table → allowed? (open/approved)

2. fetch()
   → HTTP GET with retry/backoff
   → store_raw(content, source_id) → warehouse/raw/<source>/<sha256>.gz
   → store_acquisition(...) → raw_acquisition table

3. parse(raw_content, raw_hash, result)
   → Decode HTML/CSV/JSON/XML
   → Extract structured fields
   → insert_source_record(...) → source_record table (dedup by payload hash)
   → upsert_*() → entity graph tables

4. log_run(source_id, status, ...)
   → collector_run table
```

### How powops reads it

```sql
-- powops queries this for each source
SELECT started_at, status, error, duration_seconds,
       source_records_new, raw_new
FROM collector_run
WHERE source_id = ?
ORDER BY run_id DESC LIMIT 1
```

Status resolution:
- `collector_run.status = 'ok'` AND age < max_staleness → `ok`
- `collector_run.status = 'ok'` AND age > max_staleness → `stale`
- `collector_run.status = 'error'` → `error`
- API key env var missing → `no_key` (checked before DB)
- No rows in collector_run → `unknown`

---

## Structural blockers

### JS-rendered pages (3 collectors)

| Collector | URL | Issue |
|-----------|-----|-------|
| bara_directory | automate.org.uk/member-directory | JavaScript redirect, no static content |
| rbtx | rbtx.co.uk | Product listings rendered by JS |
| find_apprenticeship | gov.uk/apply-apprenticeship | Landing page, search requires JS |

**Options:**
1. Find API endpoints behind the JS
2. Use headless browser (playwright/selenium)
3. Accept as evidence-only (raw HTML stored)

### API key collectors (5 collectors)

| Collector | Env var | Parser status | fetch() status |
|-----------|---------|---------------|----------------|
| companies_house | COMPANIES_HOUSE_API_KEY | Complete | Stub (returns None) |
| mouser | MOUSER_API_KEY | Complete | Stub |
| farnell | FARNELL_API_KEY | Complete | Stub |
| lcsc | LCSC_API_KEY | Complete | Stub |
| ebay_uk | EBAY_APP_ID | Complete (has bug) | Stub |

**eBay bug:** `location` field mapped to `itemEndDate` instead of actual location.

### powops path error

```
PermissionError: [Errno 13] Permission denied: '/root/powuk'
```

New powops commit added gardens at `/root/powuk` and `/root/powstock` which are inaccessible. This doesn't affect powrobots — only the powops `check_all()` function when it encounters these gardens. Workaround: check powrobots specifically instead of calling `check_all()`.

---

## CLI commands

```bash
# Status — row counts per table
python3 -m powrobots.cli status

# Sources — list registered sources
python3 -m powrobots.cli sources

# Seed — populate source_rights + source_registry
python3 -m powrobots.cli seed

# Collect — run a collector
python3 -m powrobots.cli collect <source_id>
python3 -m powrobots.cli collect all

# Health — last collector run per source
python3 -m powrobots.cli health

# Validate — check everything is wired
python3 -m powrobots.cli validate
```

---

## How to add a new collector

1. Create `powrobots/collectors/<name>.py`
2. Subclass `BaseCollector`
3. Set `SOURCE_ID`, `DATASET`, `PARSER_ID`
4. Implement `fetch()` → return bytes or None
5. Implement `parse(raw_content, raw_hash, result)` → call `insert_source_record()` + `upsert_*()`
6. Add to `COLLECTORS` dict in `cli.py`
7. Add to `powops/sources.yaml` under `powrobots` garden with `health.check: collector_db`
8. Run `python3 -m powrobots.cli seed` (idempotent)
9. Run `python3 -m powrobots.cli collect <source_id>`
10. powops sees it immediately

---

## How to add a new API-key source

1. Register for API key
2. Set env var: `export COMPANIES_HOUSE_API_KEY=xxx`
3. Implement `fetch()` in the collector
4. Test: `python3 -m powrobots.cli collect <source_id>`
5. powops reports `no_key` until env var is set, then `ok`/`error`

---

## Testing

```bash
# Run all tests (uses temp DB)
POWROBOTS_DB=/tmp/test.db python3 -m pytest tests/ -v

# Run specific test
POWROBOTS_DB=/tmp/test.db python3 -m pytest tests/test_core.py::TestCollectors -v
```

42 tests covering:
- FK enforcement
- Raw dedup, immutability, deterministic hashing
- Acquisition appending
- Source record versioning and dedup
- Entity graph operations (upsert, idempotent)
- Robot ontology (types, applications, categories)
- Rights gating (blocked, open, unknown)
- Seed YAML parsing
- Collector importability and run pipeline
- Schema validation
- Parser determinism
- Change events
- Deployment evidence
- UK trade records

---

## Key files

```
powrobots/
├── cli.py                      # CLI entry point (15 collectors, seed/health/status)
├── core/enums.py               # Domain enums (RobotType, Application, ComponentCategory)
├── collectors/
│   ├── base.py                 # BaseCollector + CollectorResult
│   ├── hmrc_traders.py         # CSV parser — 561 traders
│   ├── hmrc_trade.py           # HTML stub — needs parser
│   ├── contracts_finder.py     # HTML parser — 20 notices
│   ├── opss_safety.py          # HTML parser — 50 alerts
│   ├── ukri_gtr.py             # XML parser — research projects
│   ├── companies_house.py      # Parser ready, fetch stub
│   ├── mouser.py               # Parser ready, fetch stub
│   ├── farnell.py              # Parser ready, fetch stub
│   ├── lcsc.py                 # Parser ready, fetch stub
│   ├── ebay_uk.py              # Parser ready, fetch stub (location bug)
│   ├── bara_directory.py       # HTML stub — JS-rendered
│   ├── bgs_minerals.py         # HTML stub — needs parser
│   ├── ons_ppi.py              # HTML stub — needs parser
│   ├── apprenticeships.py      # HTML stub — JS-rendered
│   └── rbtx.py                 # Metadata stub — JS-rendered
├── shared/
│   ├── db.py                   # Schema + seed data + init
│   └── persist.py              # Storage + entity graph operations
├── seeds/                      # YAML seed files
├── docs/
│   ├── northstar.md            # Master design document
│   ├── review.md               # Design review with phase gating
│   ├── devplan.md              # 8-phase development roadmap
│   ├── devplanresponse.md      # Audit mapped to global devplan
│   ├── repair-outcome-vision.md # Repair-decision intelligence
│   ├── blockers.md             # Tracked blockers
│   ├── cross_repo_review.md    # Cross-repo compatibility
│   └── API_KEYS.md             # API key inventory
├── tests/test_core.py          # 42 tests
├── scripts/
│   ├── seed_loader.py          # Entity graph seeder
│   └── collect-all.sh          # Systemd wrapper
├── deploy/systemd/             # Service + timer
├── vendor_repos/               # 7 cloned robot description repos
└── warehouse/
    ├── powrobots.db            # SQLite database
    └── raw/                    # 21 blobs, ~356KB
```

---

## Deployment

### Systemd

```bash
# Install
cp deploy/systemd/*.service ~/.config/systemd/user/
cp deploy/systemd/*.timer ~/.config/systemd/user/
systemctl --user daemon-reload

# Enable
systemctl --user enable powrobots-collect.timer
systemctl --user enable powrobots-collect.service

# Start
systemctl --user start powrobots-collect.timer

# Check
systemctl --user status powrobots-collect.timer
journalctl --user -u powrobots-collect.service -f
```

### Manual collection

```bash
# All sources
python3 -m powrobots.cli collect all

# Single source
python3 -m powrobots.cli collect hmrc_traders

# Check what powops sees
python3 -m powrobots.cli health
```

---

## What powops sees

```
powrobots: 10/15 ok | 5/15 no_key

  ACTIVE:
    hmrc_traders     ok    records=561   age=<1h
    hmrc_trade       ok    records=1     age=<1h
    ukri_gtr         ok    records=0     age=<1h
    contracts_finder ok    records=20    age=<1h
    opss_safety      ok    records=50    age=<1h
    bara_directory   ok    records=1     age=<1h
    bgs_minerals     ok    records=1     age=<1h
    ons_ppi          ok    records=1     age=<1h
    find_apprenticeship ok records=1     age=<1h
    rbtx             ok    records=2     age=<1h

  NEEDS KEY:
    companies_house  no_key  Set COMPANIES_HOUSE_API_KEY
    mouser           no_key  Set MOUSER_API_KEY
    farnell          no_key  Set FARNELL_API_KEY
    lcsc             no_key  Set LCSC_API_KEY
    ebay_uk          no_key  Set EBAY_APP_ID
```

### MCP tools

```python
powops_status(garden="powrobots")      # All 15 sources
powops_source(source_id="hmrc_traders") # One source detail
powops_coverage()                        # Coverage breakdown
powops_history(garden="powrobots")       # Check history
powops_uptime(days=7)                    # Uptime stats
powops_incidents(status="open")          # Open incidents
powops_events(garden="powrobots")        # Event stream
```

### Web API

```
GET /api/status                          # All sources
GET /api/history?garden=powrobots        # History
GET /api/uptime                          # Uptime
GET /api/volume                          # Volume
GET /api/incidents                       # Incidents
GET /api/events?garden=powrobots         # Events
GET /api/repos                           # GitHub CI status
```

All require `?token=<TOKEN>`.
