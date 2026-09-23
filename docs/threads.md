# Open Threads

All unresolved work, blockers, and decisions that need attention.

Updated 2026-09-23 with global devplan gap analysis.

---

## Gap analysis: devplan.md vs reality

### Checkpoint 1: Collecting

| Requirement | Status | Gap |
|-------------|--------|-----|
| All 7 gardens discovered | Partial | powrobots is wired, other gardens vary |
| Every collector produces run receipt | Done | collector_run + source_health populated |
| Dashboard shows real status | Done | powops shows 10/15 ok, 5/15 no_key |
| No false-green health signals | Done | evidence_level, staleness checks working |

### Checkpoint 2: Verified data (powrobots portion)

| Requirement | Status | Gap |
|-------------|--------|-----|
| 10 robot models with exact BOMs | 123 models, 0 BOMs | Need BOM parsing from vendor repos |
| BOM for Dreame L10s Ultra | Not started | No consumer robot data at all |
| BOM for Roborock S7 | Not started | No consumer robot data at all |
| BOM for SO-101 | Not started | Need to parse ODRI/LeRobot repos |
| 3 substitution types | Not started | Need compatibility evidence |

### Garden 1: UK robot intelligence (commercial2.md)

| Requirement | Status | Gap |
|-------------|--------|-----|
| Discover consumer robots entering UK | Not started | No consumer robot detection |
| Exact models and revisions | Industrial only | Need Dreame, Roborock, iRobot, Husqvarna |
| Parts, manuals, accessories | Seed-level only | Need manufacturer doc parsing |
| Robot-to-parts graph | 29 seed relations | Need BOM parsing for real relations |

### Spare parts first transaction (goldmoat2.md)

| Part | Status | Gap |
|------|--------|-----|
| Dreame pump 20020100005232 | Not tracked | Need supplier monitoring |
| Dreame solenoid 20020100009618 | Not tracked | Need supplier monitoring |
| Roborock contacts 9.01.0248 | Not tracked | Need supplier monitoring |
| Roborock S7 LiDAR motor | Not tracked | Need supplier monitoring |

---

## Thread 1: Consumer robot registration

**Status:** Not started
**What:** Register Dreame L10s Ultra, Roborock S7, iRobot Roomba, Husqvarna Automower with exact models, revisions, gear ratios, motor configs
**Why:** devplan.md Phase 1 requires 10 robot models with exact BOMs. Current 123 models are all industrial (ABB, FANUC, KUKA, UR). Zero consumer robots.
**Effort:** 5-7 days
**Priority:** P0 — blocks Phase 1 commercial milestone
**Depends on:** Manufacturer documentation access, teardown data

---

## Thread 2: BOM parsing from vendor repos

**Status:** 7 repos cloned, not parsed
**What:** Parse URDF/XACRO files from ABB, FANUC, KUKA, Universal Robot, MuJoCo Menagerie to extract robot specs and component relationships
**Why:** Need "10 robot models with exact BOMs" for Checkpoint 2
**Effort:** 5-7 days
**Priority:** P0 — highest value unbuilt collector
**Depends on:** lxml (installed), URDF format knowledge

---

## Thread 3: SO-101 complete BOM

**Status:** Not started
**What:** Get SO-101 BOM from LeRobot/ODRI repos, document exact gear ratios per joint, map to supplier parts
**Why:** devplan.md says SO-101 is the first reference design for kits
**Effort:** 3-5 days
**Priority:** P0 — first kit product foundation
**Depends on:** ODRI/LeRobot repo access, servo specification data

---

## Thread 4: Robot vacuum spare parts monitoring

**Status:** Not started
**What:** Track Dreame, Roborock, iRobot parts with exact part numbers, pricing, UK availability
**Why:** goldmoat2.md identifies 6 specific parts with observable UK supply gaps
**Effort:** 5-7 days
**Priority:** P0 — first commercial transaction
**Depends on:** Supplier API access (eBay, FixPart, manufacturer stores)

---

## Thread 5: Mouser fetch() implementation

**Status:** Parser ready, fetch stub
**Blocker:** Need MOUSER_API_KEY env var
**API:** Mouser Search API (free, 1000 req/day)
**Effort:** 2-3 days
**Priority:** P0 — component pricing for BOM resolution

---

## Thread 6: Farnell fetch() implementation

**Status:** Parser ready, fetch stub
**Blocker:** Need FARNELL_API_KEY env var
**API:** element14 Product Search API (free key)
**Effort:** 2-3 days
**Priority:** P0 — UK component pricing

---

## Thread 7: LCSC fetch() implementation

**Status:** Parser ready, fetch stub
**Blocker:** Need LCSC_API_KEY env var
**API:** LCSC Open API
**Effort:** 2-3 days
**Priority:** P0 — China component pricing

---

## Thread 8: eBay UK fetch() implementation

**Status:** Parser ready, fetch stub + location bug
**Blocker:** Need EBAY_APP_ID + OAuth 2.0 setup
**Bug:** `location` mapped to `itemEndDate`
**Effort:** 3-4 days
**Priority:** P1 — used market + spare parts pricing

---

## Thread 9: Mouser/Farnell component pricing for SO-101

**Status:** Depends on Threads 5-7
**What:** Price the SO-101 BOM components across UK (Farnell), global (Mouser), China (LCSC)
**Why:** First kit product needs UK-delivered quote
**Effort:** 2-3 days after API keys
**Priority:** P0 — first kit pricing

---

## Thread 10: Cross-repo integration

**Status:** Not started
**What:** Share component identity with powproducts, link repair data to robot models, route BOMs to suppliers via powphysical
**Why:** devplan.md Phase 2 requires cross-garden data flow
**Effort:** 1-2 weeks
**Priority:** P1 — Phase 2 foundation

---

## Thread 11: powrobots → powuk data dependency

**Status:** Not started
**What:** powrobots needs UK business data from powuk for context
**Why:** DEVMAP Priority 5.1
**Effort:** 2 days
**Priority:** P2 — enriches UK business intelligence

---

## Thread 12: Consumer robot detection from UK market

**Status:** Not started
**What:** Monitor new consumer robots entering UK market (Dreame, Roborock, Ecovacs, iRobot, Husqvarna)
**Why:** commercial2.md Garden 1 requirement
**Effort:** 3-5 days
**Priority:** P1 — expanding beyond industrial robots

---

## Thread 13: Repair outcome tracking

**Status:** Not started
**What:** Record which parts actually fail, which repairs work, which substitutions are verified
**Why:** repair-outcome-vision.md — the data moat
**Effort:** Ongoing — needs real technician relationships
**Priority:** P1 — long-term defensibility

---

## Thread 14: JS-rendered pages (BARA, RBTX, apprenticeships)

**Status:** Structural blocker
**What:** Find API endpoints or use browser automation
**Effort:** Unknown
**Priority:** P2 — can work around for now

---

## Thread 15: HMRC trade statistics parser

**Status:** Raw HTML stored, no structured parsing
**What:** Parse trade statistics (values, volumes, trends) — not just trader list
**Effort:** 2-3 days
**Priority:** P1 — trade flow data

---

## Thread 16: ONS PPI parser

**Status:** Navigation page, no inline data
**What:** Follow links to producer price inflation datasets, parse time series
**Effort:** 2-3 days
**Priority:** P1 — UK price signals

---

## Thread 17: No MCP server in powrobots

**Status:** By design — powops is the operational surface
**What:** If needed, add powrobots-specific MCP tools for entity graph queries
**Effort:** 2-3 days
**Priority:** P2 — powops MCP covers health, not entity graph

---

## Thread 18: powops can't query entity graph

**Status:** powops only reads collector_run and source_health
**What:** Could add summary view or powrobots-specific MCP tools
**Workaround:** Use powrobots CLI (`powrobots robots`, `powrobots models`)
**Effort:** 1-2 days
**Priority:** P2 — nice to have for agent visibility

---

## Thread 19: DuckDB analytical layer

**Status:** Deferred per review.md
**When:** When SQLite query complexity demands it
**Effort:** High
**Priority:** Phase 3+

---

## Thread 20: UN Comtrade collector

**Status:** Not implemented
**What:** Global trade flow data for robotics commodity codes
**Effort:** High
**Priority:** Phase 4 — global flow garden

---

## Decision log

### 2026-09-23: CSV over HTML for HMRC traders
HMRC provides CSV download endpoint. Decided to fetch CSV instead of parsing HTML tables. More reliable, structured, and includes all 564 traders.

### 2026-09-23: Skip JS-rendered pages
BARA, RBTX, and apprenticeships all require JavaScript. Decided to accept as evidence-only for now rather than introduce browser automation dependency.

### 2026-09-23: Collection receipt format aligned with roadmap
Added collector_sha, cursor_before/after, validation_passed, schema_version to collector_run.

### 2026-09-23: source_health auto-computed
Decided to compute source_health automatically in log_run() rather than requiring separate computation step.

### 2026-09-23: Consumer robots are the priority
The global devplan (devplan.md, goldmoat2.md, commercial2.md) makes clear that consumer robot spare parts (Dreame, Roborock, iRobot) are the first commercial opportunity, not industrial robots. Current powrobots data is 100% industrial. This is the biggest gap.

### 2026-09-23: BOM parsing is the highest value unbuilt collector
The vendor repos (ABB, FANUC, KUKA, UR, MuJoCo) are cloned but not parsed. Parsing URDF files would populate the entity graph with real robot→component relationships from actual hardware, not just seeds.
