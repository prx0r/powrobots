# AGENTS.md — POWRobots ↔ POWOps Wiring

## How POWOps Monitors POWRobots

POWOps reads the `collector_run` table in `warehouse/powrobots.db` via the
`collector_db` health check type. Every time a collector runs, it logs a row
with timing, counts, HTTP stats, and errors. POWOps queries the latest row
per source and reports status.

### The data flow

```
powrobots collect <source>
       │
       ▼
BaseCollector.run()
       │
       ├── check_source_rights() → allowed?
       │
       ├── _fetch_url() → HTTP GET → store_raw() → store_acquisition()
       │
       ├── parse() → insert_source_record() → upsert_*()
       │
       └── log_run() → INSERT INTO collector_run
                           │
                           ▼
                    warehouse/powrobots.db
                           │
                    ┌──────┴──────┐
                    │             │
               powops reads   powrobots CLI
               via garden.py  reads directly
               collector_db
                    │
                    ▼
              SourceStatus
                    │
          ┌─────────┼─────────┐
          │         │         │
       CLI table  MCP tools  Web API
```

### What POWOps checks

For each source in `sources.yaml`, powops:
1. Looks up the `health.check` type — for powrobots it's `collector_db`
2. Opens `warehouse/powrobots.db`
3. Queries `collector_run` for the latest row matching `source_id`
4. Compares `started_at` against `max_staleness` (72h for most powrobots sources)
5. Returns a `SourceStatus` with: status, age, records, error, evidence_level

### Status values

| Status | Meaning | What powops sees |
|--------|---------|-----------------|
| `ok` | Last run within max_staleness, no errors | `collector_run.status = 'ok'` and age < 72h |
| `stale` | Last run exceeded max_staleness | `collector_run.status = 'ok'` but age > 72h |
| `error` | Last run had errors | `collector_run.status = 'error'` |
| `no_key` | API key env var not set | `source.api_key_env` not in environment |
| `unknown` | No runs recorded | No rows in `collector_run` for this source |
| `not_installed` | Source marked not installed | `source.status = 'not_installed'` in sources.yaml |

### Evidence levels

| Level | Meaning | Sources |
|-------|---------|---------|
| `strong` | Data-validated (heartbeat or collector_db) | All 15 powrobots sources |
| `weak` | File mtime or PID only | Not used by powrobots |

---

## Source Inventory — 15 Sources

### Category A: Active collectors (no auth, fetches live data)

These 10 sources are fully wired. They fetch live data from public endpoints,
store raw blobs, and log collector_run rows. POWOps sees them as `ok`.

| Source ID | Authority | What it does | Parser quality | Raw stored |
|-----------|-----------|-------------|----------------|------------|
| `hmrc_traders` | HMRC | Searches for HS 847950 (robot) traders | Stub — raw HTML | ~160KB |
| `hmrc_trade` | HMRC | Trade statistics index page | Stub — raw HTML | ~65KB |
| `ukri_gtr` | UKRI | Research projects XML API | **Real parser** — extracts project IDs, titles, lead orgs | ~83KB |
| `contracts_finder` | Contracts Finder | Government procurement search | Metadata only — stores search terms + raw HTML | ~1.2MB |
| `opss_safety` | OPSS | Product safety alerts (machinery) | Stub — raw HTML | ~170KB |
| `bara_directory` | BARA | Automate UK member directory | Stub — raw HTML | ~114B |
| `bgs_minerals` | BGS | World Mineral Statistics page | Stub — raw HTML | ~80KB |
| `ons_ppi` | ONS | Inflation/price indices page | Stub — raw HTML | ~70KB |
| `find_apprenticeship` | ESFA | Apprenticeship search page | Stub — raw HTML | ~68KB |
| `rbtx` | RBTX/igus | Robot marketplace (UK + China) | Metadata only — stores market + raw HTML | ~478KB |

**Total raw data collected:** ~1.8MB across 20 blobs, 14 source records

### Category B: API-key sources (parser complete, fetch not implemented)

These 5 sources have complete parsers that extract structured data, but their
`fetch()` methods return `None` — they don't make API calls yet. When the API
key is set, powops will show `no_key` instead of `error`.

| Source ID | Authority | Env var needed | Parser does | Entity graph |
|-----------|-----------|---------------|-------------|--------------|
| `companies_house` | Companies House | `COMPANIES_HOUSE_API_KEY` | Extracts company number, name, status, address | `upsert_organisation` |
| `mouser` | Mouser Electronics | `MOUSER_API_KEY` | Extracts MPN, brand, price, stock, status | `upsert_component` |
| `farnell` | Farnell/element14 | `FARNELL_API_KEY` | Extracts MPN, brand, price, stock, lead time | `upsert_component` |
| `lcsc` | LCSC Electronics | `LCSC_API_KEY` | Extracts MPN, brand, price, stock, grade | `upsert_component` |
| `ebay_uk` | eBay UK | `EBAY_APP_ID` | Extracts item ID, title, price, condition, seller | `insert_source_record` |

**To activate:** Set the env var, then `fetch()` must be implemented in each
collector. The parsers are ready — they just need real HTTP calls.

---

## Database Schema (what powops reads)

### collector_run table

```sql
-- This is the table powops queries via collector_db health check
CREATE TABLE collector_run (
    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id TEXT NOT NULL,          -- matches sources.yaml id
    started_at TEXT NOT NULL,         -- ISO timestamp
    finished_at TEXT,                 -- ISO timestamp
    status TEXT DEFAULT 'running',    -- 'ok', 'error', 'blocked'
    raw_fetched INTEGER DEFAULT 0,    -- blobs fetched
    raw_new INTEGER DEFAULT 0,        -- new (not deduped)
    source_records_new INTEGER DEFAULT 0,
    source_records_updated INTEGER DEFAULT 0,
    source_records_invalid INTEGER DEFAULT 0,
    error TEXT,                       -- JSON-encoded error list
    duration_seconds REAL
);
```

POWOps queries:
```sql
SELECT started_at, status, error, duration_seconds,
       source_records_new, raw_new
FROM collector_run
WHERE source_id = ?
ORDER BY run_id DESC LIMIT 1
```

### source_rights table

Controls which collectors are allowed to run:
- `open` — collector runs without auth
- `approved` — collector needs API key (key present = allowed)
- `terms_review` — blocked until terms reviewed
- `blocked` — never collect

### source_registry table

Metadata about each source (authority, category, cadence, tier).
Currently populated with all 15 sources.

---

## How to run collectors

```bash
# Single source
python3 -m powrobots.cli collect hmrc_traders

# All sources
python3 -m powrobots.cli collect all

# Check what powops sees
python3 -m powrobots.cli health

# Full status
python3 -m powrobots.cli status

# Validate everything is wired
python3 -m powrobots.cli validate
```

### Systemd timer

```bash
# Install
cp deploy/systemd/*.service ~/.config/systemd/user/
cp deploy/systemd/*.timer ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now powrobots-collect.timer

# Check
systemctl --user status powrobots-collect.timer
systemctl --user status powrobots-collect.service
journalctl --user -u powrobots-collect.service -f
```

Runs all collectors every 6 hours. First run 5min after boot.

---

## How POWOps exposes powrobots data

### CLI

```bash
# See all 15 powrobots sources
python3 -m powops status | grep powrobots

# See details for one source
python3 -m powops check hmrc_traders

# Full check with history
python3 -m powops full

# History for powrobots sources
python3 -m powops history --garden powrobots

# Uptime stats
python3 -m powops uptime --source hmrc_traders
```

### MCP tools (for pi agent)

```python
# All powrobots sources
powops_status(garden="powrobots")

# One source detail
powops_source(source_id="hmrc_traders")

# Coverage breakdown
powops_coverage()

# History
powops_history(garden="powrobots", days=7)

# Incidents
powops_incidents(status="open")

# Events
powops_events(garden="powrobots", days=1)
```

### Web API

```
GET /api/status                          # all sources including powrobots
GET /api/history?garden=powrobots        # powrobots history
GET /api/uptime                          # uptime per source
GET /api/volume                          # volume stats
GET /api/incidents                       # open incidents
GET /api/events?garden=powrobots         # powrobots events
GET /api/repos                           # GitHub CI status
```

All require `?token=<TOKEN>`.

---

## What POWOps knows about each source

| Source | Status | Last Good | Records | Error | Category |
|--------|--------|-----------|---------|-------|----------|
| hmrc_traders | ok | <1h ago | 1 | — | uk_trade |
| hmrc_trade | ok | <1h ago | 1 | — | uk_trade |
| ukri_gtr | ok | <1h ago | 0 | — | grants |
| contracts_finder | ok | <1h ago | 3 | — | procurement |
| opss_safety | ok | <1h ago | 1 | — | safety |
| bara_directory | ok | <1h ago | 1 | — | integrators |
| bgs_minerals | ok | <1h ago | 1 | — | minerals |
| ons_ppi | ok | <1h ago | 1 | — | prices |
| find_apprenticeship | ok | <1h ago | 1 | — | labour |
| rbtx | ok | <1h ago | 2 | — | marketplace |
| companies_house | no_key | — | — | Missing COMPANIES_HOUSE_API_KEY | corporate |
| mouser | no_key | — | — | Missing MOUSER_API_KEY | components |
| farnell | no_key | — | — | Missing FARNELL_API_KEY | components |
| lcsc | no_key | — | — | Missing LCSC_API_KEY | components |
| ebay_uk | no_key | — | — | Missing EBAY_APP_ID | aftermarket |

---

## How to add a new source

1. Create collector in `powrobots/collectors/`
2. Set `SOURCE_ID` and implement `fetch()` + `parse()`
3. Add to `COLLECTORS` dict in `cli.py`
4. Run `powrobots seed` (idempotent — skips existing)
5. Add entry to powops `sources.yaml` under `powrobots` garden
6. Set `health.check: collector_db`, `health.source_id: <SOURCE_ID>`, `health.max_staleness: 72h`
7. Run `powrobots collect <source>` — powops will see it immediately

---

## Known issues

1. **9 of 15 collectors are stubs** — they fetch raw HTML but don't parse structured data. They're "working" from powops' perspective (data flows, collector_run logs success) but the data quality is low.

2. **5 API-key collectors have fetch() stubs** — parsers are ready but `fetch()` returns `None`. Need implementation to make actual API calls.

3. **No pagination** — ukri_gtr gets 10 results, contracts_finder searches 3 terms, hmrc_traders queries 1 commodity code.

4. **source_health table exists but nothing computes into it** — powops reads collector_run directly instead.

5. **No manufacturer seed on VPS** — the seed_loader.py hasn't been run, so robot_manufacturer, robot_model, component tables are empty. This doesn't affect powops monitoring.
