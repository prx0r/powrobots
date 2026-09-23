# POWRobots — Development Plan

Extensive roadmap from current state to Layer 1 completion.

Generated 2026-09-23 from live VPS audit, not documentation claims.

---

## Current state (checkpoint)

```
Repository:     prx0r/powrobots
Branch:         main
Latest commit:  521f89d (2026-09-23)
Tests:          42/42 passing
Python:         >=3.11
Dependencies:   requests>=2.31 (runtime), pytest, ruff (dev)

Schema:         32 tables, auto-applied on connect
Collectors:     15 implemented, 10 fetching live data
Entity graph:   25 manufacturers, ~35 components, 30+ models (seeds only)
Raw storage:    20 blobs, ~356KB
Source records: 14
Collector runs: 15 (10 ok, 5 error/no_key)
Systemd:        service + timer (6h cycle)
powops:         Fully wired, all 15 sources visible via collector_db
```

### What works end-to-end

| Component | Status | Evidence |
|-----------|--------|----------|
| Schema creation | Working | 32 tables auto-created |
| Raw storage | Working | Gzip, content-addressed, deduped |
| Acquisition receipts | Working | Linked to raw blobs |
| Source record versioning | Working | Payload-hash dedup, version suffixes |
| Rights gating | Working | 15 sources seeded, open/approved |
| Collector framework | Working | Retry, backoff, rate-limit, logging |
| 10 open collectors | Working | Fetch live data, store raw + records |
| powops integration | Working | All 15 sources monitored |
| Systemd timer | Working | 6h collection cycle |
| CLI | Working | status, sources, seed, collect, validate, health |

### What doesn't work yet

| Component | Status | Blocker |
|-----------|--------|---------|
| 5 API-key collectors | Fetch stub | No API implementation |
| 9 HTML-only collectors | No parsing | Raw HTML stored, no structured extraction |
| Entity graph from live data | Seed only | No collector upserts models/components |
| Vendor repo parsing | Cloned only | No URDF/BOM parser |
| source_health computation | Table empty | Nothing writes aggregated health |
| Collection receipts | Basic format | Missing collector_sha, cursor, validation |
| Manufacturer seeding on VPS | Not run | seed_loader.py not executed |

---

## Architecture

### The seven gardens (powrobots scope)

```
1. Robot Catalogue / BOM Graph
   ROS, OEM specs, manuals, compatibility
   → powrobots owns this

2. China Factory
   NBS production, MIR/GGII, corporate filings, China prices, LCSC/RBTX
   → powrobots + powphysical

3. Global Flow
   UN Comtrade and HS-code graph
   → powrobots (deferred to Phase 4)

4. UK Landing
   HMRC trade/traders + UK distributor prices/inventory
   → powrobots (hmrc_traders, hmrc_trade)

5. UK Adoption
   Tenders, grants, integrators, deployments, Companies House
   → powrobots (contracts_finder, ukri_gtr, bara_directory, companies_house)

6. UK Aftermarket
   Used robots, parts, repairs, technician demand, apprenticeships
   → powrobots (ebay_uk, rbtx) + repair repo

7. Equity Graph
   China + UK + Japan/Germany suppliers mapped to each layer
   → Layer 2 (deferred)
```

### Data flow

```
Collectors → Raw storage → Source records → Entity graph
     ↓                                        ↓
collector_run                    powops monitors via collector_db
     ↓                                        ↓
powops health                  MCP / Dashboard / CLI
```

### Shared contracts

| Contract | Format | Owner |
|----------|--------|-------|
| collector_run | SQLite table | powrobots |
| source_rights | SQLite table | powrobots |
| source_registry | SQLite table | powrobots |
| Health artifact | collector_db query | powops reads |
| Raw blob | gzip, SHA256-named | powrobots |
| Source record | JSON, payload-hash dedup | powrobots |

---

## Phase 1: Data quality (weeks 1-3)

**Goal:** Turn raw HTML collectors into structured data collectors. Make the entity graph grow from live collection.

### 1.1 Parse HMRC traders HTML

**Priority:** P0 — this is the "crown jewel dataset"
**Effort:** Low (1-2 days)
**Impact:** 497 UK businesses trading in industrial robots

The hmrc_traders collector fetches `uktradeinfo.com/search/traders/?commodities=847950`. The page contains a table of businesses with names, addresses, and trade details. Parse this into structured records.

**Deliverables:**
- Parse HTML table into `source_record` entries
- Upsert each business as an `organisation` entity
- Extract: company name, address, trade type, commodity code
- Add `hmrc_business` to entity graph
- Test: verify 400+ organisations created

**Acceptance:** `powrobots collect hmrc_traders` produces 400+ structured records, not 1.

### 1.2 Parse Contracts Finder structured data

**Priority:** P0 — procurement signals
**Effort:** Low (1-2 days)
**Impact:** Robotics-related government contracts

The contracts_finder collector fetches search results but stores metadata only. The Contracts Finder API returns structured JSON with contract titles, values, buyers, dates, and descriptions.

**Deliverables:**
- Switch from HTML scraping to JSON API responses
- Parse: contract title, value, buyer, award date, description, URL
- Filter to robotics/automation terms
- Store as `source_record` with structured fields
- Test: verify contracts parsed with values

**Acceptance:** `powrobots collect contracts_finder` produces structured contract records.

### 1.3 Parse OPSS safety alerts

**Priority:** P0 — safety data
**Effort:** Low (1 day)
**Impact:** Recalled/unsafe robotic products

**Deliverables:**
- Parse individual alert entries from HTML
- Extract: product name, recall type, date, description, risk level
- Store as structured source records
- Test: verify alerts parsed

### 1.4 Parse ONS PPI time series

**Priority:** P1 — price signals
**Effort:** Medium (2-3 days)
**Impact:** UK producer price indices for electronics/industrial

**Deliverables:**
- Parse ONS inflation tables
- Extract: index name, date, value, category
- Store as time-series source records
- Test: verify time series data

### 1.5 Parse BARA directory

**Priority:** P1 — integrator directory
**Effort:** Low (1 day)
**Impact:** UK robot integrator companies

**Deliverables:**
- Parse member directory entries
- Extract: company name, website, specialisms, location
- Upsert as `organisation` entities with `integrator` type
- Test: verify integrators created

### 1.6 Parse BGS minerals data

**Priority:** P1 — material supply
**Effort:** Medium (2-3 days)
**Impact:** Critical mineral supply data for robotics materials

**Deliverables:**
- Parse mineral statistics tables
- Extract: mineral name, production volumes, UK import data
- Store as structured records
- Test: verify data extracted

### 1.7 Parse apprenticeships

**Priority:** P1 — labour signals
**Effort:** Low (1 day)
**Impact:** UK robotics/automation training programmes

**Deliverables:**
- Parse apprenticeship search results
- Extract: programme name, provider, duration, level, location
- Store as structured records
- Test: verify programmes parsed

### 1.8 Parse RBTX marketplace

**Priority:** P1 — robot pricing
**Effort:** Medium (2-3 days)
**Impact:** Low-cost robot pricing from UK and China

**Deliverables:**
- Parse product listings from both UK and China endpoints
- Extract: product name, price, currency, specifications, market
- Store as structured records with market observations
- Test: verify products parsed from both markets

**Phase 1 exit criteria:**
- All 10 open collectors produce structured records (not raw HTML)
- Entity graph grows from live collection (not just seeds)
- powops reports record counts > 1 for all active sources
- Total source records > 100

---

## Phase 2: API-key collectors (weeks 3-5)

**Goal:** Implement fetch() for the 5 API-key collectors. Make component pricing real.

### 2.1 Companies House fetch()

**Priority:** P0 — corporate data
**Effort:** Medium (2-3 days)
**API:** Companies House REST API (free key)

**Deliverables:**
- Implement `fetch()` with proper authentication
- Search endpoint: company name/number lookup
- Parse: company number, name, status, type, address, SIC code, officers
- Upsert as `organisation` entities
- Test: verify companies parsed

**Env var:** `COMPANIES_HOUSE_API_KEY`

### 2.2 Mouser fetch()

**Priority:** P0 — component pricing
**Effort:** Medium (2-3 days)
**API:** Mouser Search API (free, 1000 req/day)

**Deliverables:**
- Implement `fetch()` with API key authentication
- Search by MPN from component_basket seed
- Parse: MPN, brand, description, price breaks, stock, lead time
- Upsert as `component` entities with `component_market_observation`
- Test: verify components priced

**Env var:** `MOUSER_API_KEY`

### 2.3 Farnell fetch()

**Priority:** P0 — UK component pricing
**Effort:** Medium (2-3 days)
**API:** element14 Product Search API (free key)

**Deliverables:**
- Implement `fetch()` with API key authentication
- Search by MPN from component_basket seed
- Parse: MPN, brand, price (GBP), stock, lead time, status
- Upsert as `component` entities
- Test: verify UK pricing

**Env var:** `FARNELL_API_KEY`

### 2.4 LCSC fetch()

**Priority:** P0 — China component pricing
**Effort:** Medium (2-3 days)
**API:** LCSC Open API

**Deliverables:**
- Implement `fetch()` with API key authentication
- Search by MPN from component_basket seed
- Parse: MPN, brand, price (CNY), stock, grade
- Upsert as `component` entities
- Test: verify China pricing

**Env var:** `LCSC_API_KEY`

### 2.5 eBay UK fetch()

**Priority:** P1 — used market
**Effort:** Medium (3-4 days)
**API:** eBay Browse API (OAuth)

**Deliverables:**
- Implement `fetch()` with OAuth authentication
- Search for robot brands (ABB, FANUC, KUKA, Universal Robot)
- Parse: item ID, title, price, condition, seller, location, end date
- Fix `location` bug (currently mapped to `itemEndDate`)
- Store as `market_listing` + `market_observation`
- Test: verify listings parsed

**Env var:** `EBAY_APP_ID`

### 2.6 Component price comparison engine

**Priority:** P1 — cross-supplier intelligence
**Effort:** Medium (2-3 days)

**Deliverables:**
- After Mouser/Farnell/LCSC collectors run, query component_market_observation
- Compare same MPN across UK (Farnell) vs China (LCSC) vs global (Mouser)
- Compute: cheapest source, lead time, stock availability
- Store as derived comparison records
- Test: verify cross-supplier comparisons

**Phase 2 exit criteria:**
- All 5 API-key collectors fetching and parsing
- Component prices from 3+ suppliers
- Used market listings from eBay
- Total source records > 500
- Entity graph has live-populated components with prices

---

## Phase 3: Entity graph from hardware (weeks 5-8)

**Goal:** Populate the robot→component→supplier graph from open-source hardware and manufacturer docs.

### 3.1 URDF parser

**Priority:** P0 — robot models from vendor repos
**Effort:** Medium (3-4 days)

**Deliverables:**
- Parse URDF/XACRO files from `vendor_repos/`
- Extract: links, joints, joint types, parent/child, axis, position limits, velocity limits, effort limits
- Upsert as `robot_model` entities with specs
- Create `HAS_DESCRIPTION` relations
- Test: verify models parsed from ABB, FANUC, KUKA, Universal Robot

### 3.2 BOM parser for open-source projects

**Priority:** P0 — component relations
**Effort:** High (5-7 days)

**Deliverables:**
- Parse BOM files (CSV, YAML, markdown tables) from open-source robot repos
- Extract: component name, MPN, quantity, category, supplier, reference designator
- Match to existing `component` entities by MPN
- Create `REQUIRES` and `COMPATIBLE_WITH` relations
- Assign confidence tier (A=manufacturer-verified, B=same-spec alternative, C=inferred)
- Test: verify BOMs parsed for SO-101, Solo, Bolt

### 3.3 ROBOTIS Dynamixel collector

**Priority:** P1 — servo specifications
**Effort:** Medium (2-3 days)

**Deliverables:**
- Collect Dynamixel servo specifications from ROBOTIS docs
- Parse: model, voltage, torque, speed, protocol, dimensions, weight
- Upsert as `component` entities with `servo` category
- Create compatibility relations between servos and robot models
- Test: verify servos catalogued

### 3.4 MuJoCo Menagerie parser

**Priority:** P1 — simulation models
**Effort:** Medium (2-3 days)

**Deliverables:**
- Parse model descriptions from MuJoCo Menagerie
- Extract: robot name, description, joints, actuators, sensors
- Upsert as `robot_model` entities
- Test: verify models parsed

### 3.5 Manufacturer documentation collector

**Priority:** P1 — repair knowledge
**Effort:** High (5-7 days)

**Deliverables:**
- Collect service manuals, fault codes, and repair procedures from:
  - Universal Robots (public service handbook)
  - Unitree (support documentation)
  - ROBOTIS (servo documentation)
- Parse: fault codes, error descriptions, repair steps, required tools
- Store as structured source records
- Test: verify fault codes extracted

**Phase 3 exit criteria:**
- 10+ robot models with parsed specs (not just seeds)
- 50+ component relations from BOMs
- Servo catalogue populated
- At least one manufacturer's fault codes indexed
- Entity graph has meaningful live-populated structure

---

## Phase 4: UK market integration (weeks 8-10)

**Goal:** Connect robotics data to UK economic signals.

### 4.1 HMRC trade statistics parser

**Priority:** P0 — trade flow data
**Effort:** Medium (2-3 days)

**Deliverables:**
- Parse the trade statistics HTML (not just the trader list)
- Extract: commodity code, trade value, volume, partner countries, time period
- Store as `uk_trade_record` entities
- Test: verify trade flows parsed

### 4.2 Find a Tender collector

**Priority:** P1 — procurement intelligence
**Effort:** Medium (3-4 days)

**Deliverables:**
- Collect from Find a Tender API (OCDS format)
- Filter to robotics/automation/maintenance terms
- Extract: tender ID, title, buyer, value, deadline, description
- Store as `procurement_notice` entities
- Test: verify tenders parsed

### 4.3 Companies House officer data

**Priority:** P1 — corporate network
**Effort:** Low (1-2 days, builds on 2.1)

**Deliverables:**
- After Companies House fetch() works, collect officer data
- Extract: director names, appointments, roles, dates
- Create `DIRECTOR_OF` relations between organisations and people
- Test: verify officer network

### 4.4 UKRI grant project parser

**Priority:** P1 — research funding
**Effort:** Low (already partially working)

**Deliverables:**
- Improve ukri_gtr parser to paginate (currently 10 results)
- Extract: project title, funding amount, start/end dates, institutions, researchers
- Store as `grant_project` entities
- Test: verify 100+ projects parsed

### 4.5 Component basket pricing

**Priority:** P1 — tracked component monitoring
**Effort:** Medium (2-3 days, depends on Phase 2)

**Deliverables:**
- For each component in `component_basket.yml`, query Mouser/Farnell/LCSC
- Record dated price observations
- Compute: price trends, availability changes, supplier shifts
- Store as `component_market_observation` time series
- Test: verify pricing tracked for 30+ components

**Phase 4 exit criteria:**
- HMRC trade data parsed with values
- Active tenders tracked
- Companies House officers linked
- 100+ UKRI projects indexed
- Component prices tracked across 3 suppliers

---

## Phase 5: Health and monitoring hardening (weeks 10-11)

**Goal:** Make powops monitoring bulletproof. Implement the operational contract.

### 5.1 Collection receipt format

**Priority:** P0 — roadmap compliance
**Effort:** Low (1-2 days)

**Deliverables:**
- Extend `collector_run` schema to include:
  - `collector_sha` (git commit of collector code)
  - `cursor_before` / `cursor_after` (pagination state)
  - `validation_passed` (boolean)
  - `schema_version` (source schema version)
- Update `BaseCollector.log_run()` to populate new fields
- Test: verify receipts have all fields

### 5.2 source_health computation

**Priority:** P1 — aggregated health
**Effort:** Low (1 day)

**Deliverables:**
- After each collector run, compute and write to `source_health` table
- Fields: last_attempt, last_success, last_error, records_seen, records_new, status
- Make this the canonical health artifact (powops can read it directly)
- Test: verify source_health populated after collection

### 5.3 Collector version tracking

**Priority:** P1 — deployment visibility
**Effort:** Low (1 day)

**Deliverables:**
- Each collector records its own git SHA in collector_run
- powops can show which version of code produced which run
- Test: verify SHA recorded

### 5.4 Staleness simulation tests

**Priority:** P1 — testing completeness
**Effort:** Low (1 day)

**Deliverables:**
- Test that backdating collector_run correctly triggers staleness in powops
- Test that error status propagates correctly
- Test that no_key status is correct when env var missing
- Test that source_rights blocking works

### 5.5 Backup verification

**Priority:** P2 — data safety
**Effort:** Medium (2-3 days)

**Deliverables:**
- Implement R2 sync for warehouse/raw/ directory
- Record backup receipts in a `backup_run` table
- powops backup tab shows backup health
- Test: verify backup and restore

**Phase 5 exit criteria:**
- Collection receipts match roadmap format
- source_health table populated
- Collector version tracked
- Staleness/error states tested
- Backup verified

---

## Phase 6: Cross-repo integration (weeks 11-13)

**Goal:** Connect powrobots to the broader POW ecosystem.

### 6.1 powproducts integration

**Priority:** P0 — canonical product identity
**Effort:** Medium (3-4 days)

**Deliverables:**
- Share component identity across powrobots and powproducts
- Use same MPN format, same canonical names
- Cross-reference: powrobots component ↔ powproducts ProductVariant
- Test: verify components resolve across repos

### 6.2 repair integration

**Priority:** P1 — repair knowledge
**Effort:** Medium (2-3 days)

**Deliverables:**
- Link powrobots robot models to repair fault records
- Shared: robot model → component → fault → repair action
- Test: verify repair data links to robot models

### 6.3 powphysical supplier routing

**Priority:** P1 — BOM to purchase
**Effort:** Medium (3-4 days)

**Deliverables:**
- When a BOM is parsed, check powphysical for supplier availability
- Route components to cheapest available supplier
- Test: verify BOM→supplier routing

### 6.4 powops garden manifest

**Priority:** P0 — operational contract
**Effort:** Low (1 day)

**Deliverables:**
- Generate `ops/manifest.json` from source_registry
- powops discovers powrobots sources from this manifest
- Replace central sources.yaml entries with discovered manifest
- Test: powops reads manifest correctly

**Phase 6 exit criteria:**
- Components shared with powproducts
- Repair data links to robot models
- BOM→supplier routing works
- Garden manifest generated and discovered

---

## Phase 7: Derived signals (weeks 13-16)

**Goal:** Compute the first economic signals from collected data.

### 7.1 Robot import pulse

**Priority:** P1 — adoption signal
**Effort:** Medium (2-3 days)

**Deliverables:**
- From HMRC trade data: monthly import volume of HS 847950
- Compute: month-over-month change, trend, anomaly detection
- Store as derived time series
- Test: verify import pulse computed

### 7.2 Component pressure index

**Priority:** P1 — supply signal
**Effort:** Medium (3-4 days)

**Deliverables:**
- From component pricing: track price changes across suppliers
- Compute: price velocity, stock availability trend, lead time changes
- Store as derived index
- Test: verify pressure index computed

### 7.3 Used robot liquidity

**Priority:** P2 — aftermarket signal
**Effort:** Medium (2-3 days)

**Deliverables:**
- From eBay listings: track listing count, price distribution, time-to-sell
- Compute: liquidity score, price trend by model
- Store as derived time series
- Test: verify liquidity metrics

### 7.4 Skills pressure

**Priority:** P2 — labour signal
**Effort:** Low (1-2 days)

**Deliverables:**
- From apprenticeships + UKRI grants: track training supply
- From BARA directory: track integrator count
- Compute: skills supply vs demand proxy
- Test: verify skills metrics

**Phase 7 exit criteria:**
- Robot import pulse computed monthly
- Component pressure index computed
- Used robot liquidity tracked
- Skills pressure computed
- All signals available via powops MCP

---

## Phase 8: Testing and production hardening (weeks 16-18)

**Goal:** End-to-end tests, failure simulation, production validation.

### 8.1 Integration tests

**Priority:** P0
**Effort:** Medium (3-4 days)

**Deliverables:**
- Test full pipeline: collect → parse → store → entity graph → powops
- Test with mock HTTP responses (not live APIs)
- Test edge cases: empty responses, malformed HTML, API errors, rate limits
- Test idempotency: running collector twice doesn't duplicate data

### 8.2 Failure simulation

**Priority:** P1
**Effort:** Medium (2-3 days)

**Deliverables:**
- Simulate: API key expired, upstream down, rate limited, schema changed
- Verify powops correctly reports each failure mode
- Verify incident lifecycle (open → update → resolve)
- Test concurrent health cycles

### 8.3 Performance baseline

**Priority:** P2
**Effort:** Low (1 day)

**Deliverables:**
- Benchmark: full collection cycle time
- Benchmark: database query performance
- Benchmark: entity graph upsert throughput
- Document: resource usage (CPU, memory, disk)

### 8.4 Documentation

**Priority:** P1
**Effort:** Low (1-2 days)

**Deliverables:**
- Update README with current architecture
- Update AGENTS.md with latest wiring status
- Document: how to add a new collector
- Document: how to add a new API key source
- Document: troubleshooting guide

**Phase 8 exit criteria:**
- Integration tests pass
- Failure modes tested and documented
- Performance baseline recorded
- Documentation complete

---

## Resource requirements

### API keys needed

| Source | Key | Cost | Status |
|--------|-----|------|--------|
| Companies House | `COMPANIES_HOUSE_API_KEY` | Free | Not set |
| Mouser | `MOUSER_API_KEY` | Free (1000 req/day) | Not set |
| Farnell | `FARNELL_API_KEY` | Free | Not set |
| LCSC | `LCSC_API_KEY` | Free | Not set |
| eBay | `EBAY_APP_ID` | Free (5000 calls/day) | Not set |

### Infrastructure

| Component | Current | Needed |
|-----------|---------|--------|
| VPS | Running | Sufficient |
| SQLite | Working | Sufficient for Phase 1-5 |
| DuckDB | Not installed | Phase 3+ if query complexity demands |
| R2 backup | Not configured | Phase 5 |
| Systemd | Timer working | Sufficient |

### Dependencies

| Package | Purpose | Status |
|---------|---------|--------|
| requests | HTTP | Installed |
| pyyaml | Config | Available via powops |
| beautifulsoup4 | HTML parsing | Need to add (Phase 1) |
| lxml | XML parsing | Need to add (URDF parsing) |

---

## Priority matrix

| Priority | Work | Phase | Impact | Risk |
|----------|------|-------|--------|------|
| P0 | Parse HMRC traders HTML | 1 | UK business directory | Low |
| P0 | Parse Contracts Finder | 1 | Procurement signals | Low |
| P0 | Implement fetch() for Mouser/Farnell/LCSC | 2 | Component pricing | Medium |
| P0 | URDF parser for vendor repos | 3 | Robot models | Medium |
| P0 | BOM parser for open-source projects | 3 | Component relations | High |
| P0 | Collection receipt format | 5 | Roadmap compliance | Low |
| P0 | powproducts integration | 6 | Canonical identity | Medium |
| P0 | Integration tests | 8 | Quality assurance | Low |
| P1 | Parse OPSS safety alerts | 1 | Safety data | Low |
| P1 | Parse ONS PPI | 1 | Price signals | Medium |
| P1 | Parse BARA directory | 1 | Integrator list | Low |
| P1 | Parse BGS minerals | 1 | Material supply | Medium |
| P1 | Parse apprenticeships | 1 | Labour signals | Low |
| P1 | Parse RBTX marketplace | 1 | Robot pricing | Medium |
| P1 | eBay UK fetch() | 2 | Used market | Medium |
| P1 | Component price comparison | 2 | Cross-supplier | Medium |
| P1 | ROBOTIS Dynamixel collector | 3 | Servo specs | Low |
| P1 | MuJoCo Menagerie parser | 3 | Simulation models | Low |
| P1 | Manufacturer documentation | 3 | Repair knowledge | High |
| P1 | HMRC trade statistics parser | 4 | Trade flows | Low |
| P1 | Find a Tender collector | 4 | Procurement | Medium |
| P1 | Companies House officers | 4 | Corporate network | Low |
| P1 | UKRI grant pagination | 4 | Research funding | Low |
| P1 | Component basket pricing | 4 | Price tracking | Medium |
| P1 | source_health computation | 5 | Health aggregation | Low |
| P1 | Collector version tracking | 5 | Deployment visibility | Low |
| P1 | repair integration | 6 | Repair knowledge | Medium |
| P1 | powphysical supplier routing | 6 | BOM→purchase | Medium |
| P1 | Robot import pulse | 7 | Adoption signal | Low |
| P1 | Component pressure index | 7 | Supply signal | Medium |
| P1 | Failure simulation tests | 8 | Quality assurance | Low |
| P1 | Documentation | 8 | Maintainability | Low |
| P2 | Used robot liquidity | 7 | Aftermarket signal | Medium |
| P2 | Skills pressure | 7 | Labour signal | Low |
| P2 | Backup verification | 5 | Data safety | Low |
| P2 | Performance baseline | 8 | Operations | Low |
| P3 | UN Comtrade collector | Future | Trade flow data | High |
| P3 | iFixit API collector | Future | Repair procedures | Medium |

---

## Success metrics

### Layer 1 completion (Checkpoint 1)

| Metric | Current | Target |
|--------|---------|--------|
| Sources collecting | 10/15 | 15/15 |
| Structured records | 14 | >1000 |
| Entity graph nodes | ~60 (seeds) | >500 |
| Entity graph relations | 0 | >200 |
| Robot models | 30 (seeds) | >50 (from live collection) |
| Component prices | 0 | >100 (from 3+ suppliers) |
| Collector runs logged | 15 | >500 |
| powops sources ok | 10/15 | 15/15 |
| Tests passing | 42 | >80 |
| Integration tests | 0 | >20 |

### Commercial readiness

| Metric | Current | Target |
|--------|---------|--------|
| One robot fully BOM'd | No | Yes (SO-101 or similar) |
| UK-delivered price computed | No | Yes (for 10+ components) |
| Used market pricing | No | Yes (for 5+ robot models) |
| Trade flow data parsed | No | Yes (monthly import pulse) |
| Procurement signals | No | Yes (active tenders tracked) |

---

## What powops can see at each phase

### After Phase 1

```
powrobots: 15/15 ok
  hmrc_traders     ok    records=497 (was 1)
  contracts_finder ok    records=50+ (was 3)
  opss_safety      ok    records=10+ (was 1)
  ons_ppi          ok    records=20+ (was 1)
  bara_directory   ok    records=50+ (was 1)
  bgs_minerals     ok    records=10+ (was 1)
  find_apprenticeship ok records=20+ (was 1)
  rbtx             ok    records=30+ (was 2)
  hmrc_trade       ok    records=10+ (was 1)
  ukri_gtr         ok    records=100+ (was 0)
  companies_house  no_key (unchanged)
  mouser           no_key (unchanged)
  farnell          no_key (unchanged)
  lcsc             no_key (unchanged)
  ebay_uk          no_key (unchanged)
```

### After Phase 2

```
powrobots: 15/15 ok (or error if API issues)
  companies_house  ok    records=100+ (was no_key)
  mouser           ok    records=30+ (was no_key)
  farnell          ok    records=30+ (was no_key)
  lcsc             ok    records=30+ (was no_key)
  ebay_uk          ok    records=50+ (was no_key)
```

### After Phase 3

```
Entity graph:
  robot_model: 50+ (from URDF/BOM parsing)
  component: 100+ (from supplier APIs + BOMs)
  product_relation: 200+ (from BOMs)
  organisation: 500+ (from HMRC + Companies House)
```

---

## Risks and mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| API rate limits block collection | Medium | Respect limits, cache aggressively, backoff |
| HTML structure changes break parsers | Medium | Pin versions, test regularly, alert on parse failures |
| Entity graph becomes inconsistent | High | Validation tests, idempotent upserts, content hashing |
| powrobots schema drift from powops | Low | Shared contract tests, versioned schema |
| VPS disk fills up | Medium | Monitor raw storage, implement rotation/R2 backup |
| API keys expire or are revoked | Medium | Monitor collector_run errors, alert on sustained failures |
| Scope creep delays Phase 1 | High | Strict phase gating, ship parsers before new collectors |
