# DevPlan Response — POWRobots

Full audit of every thread in the powrobots repo, mapped to the global POW devplan.

Generated 2026-09-23 from live VPS state, not documentation claims.

---

## Current state summary

```
42 tests passing
15 collectors implemented (10 fetching live data, 5 need API keys)
32 tables in SQLite schema
25 manufacturers seeded (from YAML)
~35 tracked components seeded
7 Chinese robotics stocks seeded
30+ robot models from ROS vendor repos
20 raw blobs collected (~356KB)
14 source records stored
15 collector_run rows logged
0 entity graph nodes from live collection (only seeds)
```

**powrobots is a working Layer 1 data collection framework in early production.** The schema, persistence, dedup, versioning, and collector infrastructure are solid. The gap is that 9 of 15 collectors store raw HTML without structured parsing, and 5 API-key collectors have fetch() stubs.

---

## Thread 1: Collector infrastructure

**Status: COMPLETE**

- `BaseCollector` with retry, backoff, rate-limit handling
- Raw storage: gzip-compressed, content-addressed (`warehouse/raw/<source>/<sha256>.gz`)
- Source record versioning with payload-hash dedup
- Acquisition receipts linking raw blobs to collection runs
- `collector_run` table logging timing, counts, HTTP stats, errors
- Rights-gated collection (source_rights table)

**What's valuable to global devplan:** The collector framework is the template for all Layer 1 gardens. The `collector_run` table schema is already compatible with powops' `collector_db` health check — no adapter changes needed. This is the reference implementation for the operational contract described in roadmap Phase 1.

**What's missing:** No `source_health` computation (table exists, nothing writes to it). No collection receipt in the JSON format proposed by roadmap Phase 2. The current `collector_run` row is close but lacks `collector_sha`, `cursor_before/after`, and `validation` fields.

---

## Thread 2: Source rights and registry

**Status: COMPLETE**

- 15 sources registered in `source_rights` (10 open, 5 approved)
- 15 sources registered in `source_registry` with authority, category, cadence, tier
- `check_source_rights()` gates all collection
- CLI `seed` command populates both tables idempotently

**What's valuable to global devplan:** This is the garden-owned manifest pattern that roadmap Phase 1 calls for. Each source has a clear access method, licence, and reliability tier. The registry could be extended to produce the `ops/manifest.json` format described in the roadmap.

**What's missing:** No `collection_status` field (planned/implemented/tested/deployed/collecting/backfilling/complete). No `health_artifact` path. No `schedule` object with backfill support. The registry is a flat table — it doesn't yet generate a machine-readable manifest for powops to discover.

---

## Thread 3: Entity graph

**Status: SEED ONLY**

- 25 robot manufacturers from `manufacturers.yml`
- 25 component categories from `component_categories.yml`
- ~35 tracked components from `component_basket.yml`
- 7 Chinese robotics stocks from `chinese_stocks.yml`
- 12 HS codes from `hs_codes.yml`
- 5 ROS/URDF repos from `ros_repositories.yml`
- 30+ robot models loaded from vendor repos via `seed_loader.py`

**What's valuable to global devplan:** The entity graph is the foundation for the "robotics procurement graph" described in powvision.md. The schema covers manufacturers, models, components, distributors, relations, market listings, and observations. This is what makes POW's data moat defensible — verified compatibility relationships that can't be scraped from a single catalogue.

**What's missing:** No live collection populates the entity graph. The `ukri_gtr` collector calls `upsert_organisation` but no collector calls `upsert_robot_manufacturer`, `upsert_robot_model`, or `insert_relation`. The seed data is static — it doesn't grow from collection. The `seed_loader.py` hasn't been run on the VPS (robot_manufacturer table is empty in production).

---

## Thread 4: Open-source robot hardware

**Status: VENDOR REPOS CLONED, NOT PARSED**

- `vendor_repos/` contains 7 cloned repos: ABB, awesome-robot-descriptions, FANUC, KUKA, MuJoCo Menagerie, Universal Robot, urdf_files_dataset
- No collector parses these into the entity graph
- `robot_description` table exists but is empty

**What's valuable to global devplan:** This is the "fastest historical backfill" described in nextsteps.md. Open-source robot projects publish complete BOMs, mechanical drawings, assembly instructions, and tool requirements. Parsing these would populate robot models, components, and compatibility relations without needing API access. The ODRI (Open Dynamic Robot Initiative) Solo and Bolt projects are especially valuable — they identify specific bearings, screws, motors, encoders, and distributors.

**What's missing:** A collector that parses URDF/XACRO files, extracts links/joints/specs, and upserts into the entity graph. A BOM parser that reads project READMEs or structured BOM files and creates component + relation nodes. This is the highest-value unbuilt collector.

---

## Thread 5: Chinese sourcing and pricing

**Status: SEED ONLY**

- 7 Chinese robotics stocks tracked (in seed YAML)
- China production statistics tracked (in seed YAML)
- `lcsc` collector exists but needs API key
- `rbtx` collector fetches from both UK and China endpoints

**What's valuable to global devplan:** The China→UK procurement chain is the core commercial thesis. LCSC's documented API supports component discovery, pricing, and order workflows. The rbtx collector already hits both `rbtx.co.uk` and `rbtx.igus.cn`. The `component_market_observation` table is designed for dated price snapshots from multiple suppliers.

**What's missing:** LCSC fetch() is a stub. No collector hits 1688/AliExpress. No UN Comtrade collector for trade flow data. The HMRC trade data (HS 847950) is stored as raw HTML without parsing actual trader names, volumes, or values. The "crown-jewel dataset" (497 businesses trading in industrial robots) is not extracted.

---

## Thread 6: UK market signals

**Status: PARTIAL — RAW HTML ONLY**

- `hmrc_traders` — fetches trader search page, stores HTML
- `hmrc_trade` — fetches trade statistics index, stores HTML
- `contracts_finder` — searches procurement, stores metadata + HTML
- `opss_safety` — fetches safety alerts, stores HTML
- `bara_directory` — fetches integrator directory, stores HTML
- `ons_ppi` — fetches price indices, stores HTML
- `find_apprenticeship` — fetches apprenticeship search, stores HTML
- `bgs_minerals` — fetches mineral statistics, stores HTML

**What's valuable to global devplan:** These are the UK-side data sources that connect robotics to the physical economy. The roadmap calls for "UK repair businesses, qualifications, service opportunities and local demand signals." Contracts Finder has actual robotics-related procurement (United Utilities robotic inspection tender). OPSS safety alerts track recalled/unsafe products. BARA directory lists UK robot integrators.

**What's missing:** Every one of these collectors stores raw HTML without structured parsing. The HMRC traders page contains a table of 497 businesses — none are extracted. Contracts Finder results contain contract titles, values, buyers, and dates — none are parsed. The gap between "fetched" and "parsed" is the biggest data quality issue in the repo.

---

## Thread 7: Component sourcing and pricing

**Status: PARSER READY, FETCH STUB**

- `mouser` — parser extracts MPN, brand, price, stock, status. Fetch returns None.
- `farnell` — parser extracts MPN, brand, price, stock, lead time. Fetch returns None.
- `lcsc` — parser extracts MPN, brand, price, stock, grade. Fetch returns None.

**What's valuable to global devplan:** These are the structured supplier integrations that powvision.md identifies as critical. Mouser's 1,000 requests/day allowance is enough for an initial component watchlist. Farnell provides UK regional pricing. LCSC provides China pricing. Together they enable the "cheapest reliable way to complete a physical job" measurement.

**What's missing:** fetch() implementations for all three. The parsers are complete and tested — they just need HTTP calls. The `api_key_env` values in sources.yaml don't match what the collectors expect (sources.yaml says `MOUSER_API_KEY` but the collector needs to know the actual API endpoint and authentication method).

---

## Thread 8: eBay and used market

**Status: PARSER READY, FETCH STUB**

- `ebay_uk` — parser extracts item ID, title, price, condition, seller. Fetch returns None.
- `ebay_uk` also in powrobots source_registry with `EBAY_APP_ID`

**What's valuable to global devplan:** The used robot market is the "UK Aftermarket" garden. eBay listings for ABB/FANUC/KUKA robots, teach pendants, servo motors, and replacement parts provide real pricing and availability data. The `market_listing` and `market_observation` tables are designed for this.

**What's missing:** eBay Browse API implementation. The parser has a bug: `location` is mapped to `itemEndDate` (auction end date, not location). No entity graph upserts for sellers or robot listings.

---

## Thread 9: powops integration

**Status: COMPLETE AND VERIFIED**

- All 15 sources in powops `sources.yaml` under `powrobots` garden
- Health check type: `collector_db` against `warehouse/powrobots.db`
- `collector_run` table schema matches powops query exactly
- powops correctly reports: 10 `ok`, 5 `no_key`
- Systemd timer: 6h collection cycle
- MCP exposes all powrobots data via `powops_status(garden="powrobots")`
- Web API serves powrobots status, history, uptime, coverage
- Full end-to-end verified: collect → powops check → dashboard

**What's valuable to global devplan:** This is the reference implementation for garden↔powops wiring. The pattern (collector_run table → powops collector_db check → MCP/dashboard) works and should be replicated across all seven gardens.

---

## Thread 10: Tests and quality

**Status: SOLID FOUNDATION**

- 42 tests covering: FK enforcement, persistence, entity graph, robot ontology, rights, seeds, collectors, CLI, schema, replay, change events, deployment evidence, UK trade
- All collectors importable and testable
- Rights-gated collection tested (blocked, open, unknown)

**What's valuable to global devplan:** The test suite covers the infrastructure well. The `TestCollectors.test_collector_success_run` test proves the full fetch→parse→log pipeline works end-to-end. The `TestPersistence` tests prove dedup, immutability, and versioning work.

**What's missing:** No integration tests against live APIs. No tests for the powops wiring. No tests for the systemd deployment. No tests for the CLI `seed` or `health` commands. The `test_collector_success_run` test uses a mock — it doesn't verify actual HTTP fetches work.

---

## What the global devplan is missing for powrobots

### 1. BOM parser (highest value)

The devplan calls for "robot models, revisions, assemblies, BOMs and verified compatibility" but there is no collector that parses BOMs from open-source robot projects. The vendor repos are cloned but not parsed. This is the single highest-value unbuilt collector — it would populate the entity graph with real robot→component relationships from projects like SO-101, Solo, and Bolt.

**Effort:** Medium. URDF parsing is well-understood. BOM extraction from READMEs requires NLP or structured format detection.

### 2. HMRC data extraction (crown jewel)

The devplan references "497 businesses trading in HS 847950" as a key dataset. The collector fetches the page but stores raw HTML. Parsing the actual trader table would create the UK robotics business directory that connects to procurement, tenders, and service opportunities.

**Effort:** Low. The HTML table structure is likely consistent. BeautifulSoup parsing is straightforward.

### 3. Contracts Finder structured extraction

The collector fetches search results but stores metadata only. Parsing actual contract notices (title, value, buyer, date, description) would provide the robotics procurement signals that powvision.md identifies as commercially valuable.

**Effort:** Low. The Contracts Finder API returns structured JSON — the collector just needs to use it instead of scraping HTML.

### 4. Collection receipt format

The roadmap calls for a standardized JSON receipt per collector run. The current `collector_run` table is close but lacks `collector_sha`, `cursor_before/after`, and `validation` fields. Aligning with the receipt format would make powrobots a reference implementation.

**Effort:** Low. Add columns to collector_run, populate from BaseCollector.

### 5. Entity graph from live collection

No collector currently populates robot models, components, or relations from live data. The `ukri_gtr` collector upserts organisations, but that's it. The entity graph is seed-only. Building collectors that populate the graph from manufacturer docs, ROS packages, and BOM files would make the graph grow continuously.

**Effort:** High. Requires per-source parsers for URDF, BOM, manufacturer docs.

### 6. Vendor repo parsing

Seven robot description repos are cloned in `vendor_repos/` but nothing parses them. These contain URDF files, CAD models, and sometimes BOMs for ABB, FANUC, KUKA, Universal Robot, MuJoCo Menagerie, and community robots. A parser that extracts model specs, joint configurations, and component references would populate the entity graph without any API access.

**Effort:** Medium. URDF is XML with well-defined structure. The `robot_description` table already has columns for links, joints, types, axis, limits.

---

## Priority order for the devplan

| Priority | Work | Impact | Effort |
|----------|------|--------|--------|
| P0 | Parse HMRC traders HTML → extract 497 businesses | UK business directory | Low |
| P0 | Parse Contracts Finder → structured contract notices | Procurement signals | Low |
| P0 | Implement fetch() for Mouser/Farnell/LCSC | Component pricing | Medium |
| P1 | Parse vendor repo URDFs → entity graph | Robot models + specs | Medium |
| P1 | BOM parser for open-source projects | Component relations | Medium |
| P1 | Add collection receipt fields to collector_run | Roadmap compliance | Low |
| P2 | eBay Browse API implementation | Used market data | Medium |
| P2 | Parse ONS PPI HTML → price index time series | UK price signals | Low |
| P2 | Parse OPSS safety alerts → structured records | Safety data | Low |
| P3 | UN Comtrade collector | Trade flow data | High |
| P3 | ROBOTIS Dynamixel collector | Servo specifications | Medium |
| P3 | iFixit API collector | Repair procedures | Medium |

---

## Wiring status (what powops sees right now)

```
powrobots: 10/15 ok | 5/15 no_key

  ACTIVE (collecting, no auth needed):
    hmrc_traders     ok    HS 847950 trader search
    hmrc_trade       ok    Trade statistics index
    ukri_gtr         ok    Research projects (best parser)
    contracts_finder ok    Government procurement
    opss_safety      ok    Product safety alerts
    bara_directory   ok    Robot integrators
    bgs_minerals     ok    Mineral statistics
    ons_ppi          ok    Price indices
    find_apprenticeship ok Apprenticeships
    rbtx             ok    Robot marketplace UK+China

  NEEDS KEY (parser ready, fetch stub):
    companies_house  no_key  Set COMPANIES_HOUSE_API_KEY
    mouser           no_key  Set MOUSER_API_KEY
    farnell          no_key  Set FARNELL_API_KEY
    lcsc             no_key  Set LCSC_API_KEY
    ebay_uk          no_key  Set EBAY_APP_ID
```

Every source is visible to powops. Active ones show status, age, and record counts. Inactive ones show the specific missing credential. Nothing is hidden or unknown.
