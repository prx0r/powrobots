# Open Threads

All unresolved work, blockers, and decisions that need attention.

---

## Thread 1: Mouser fetch() implementation

**Status:** Parser ready, fetch stub
**Blocker:** Need API key set as `MOUSER_API_KEY` env var
**Parser:** Extracts MPN, brand, price, stock, status from JSON response
**API:** Mouser Search API (free, 1000 req/day)
**Effort:** 2-3 days
**Priority:** P0 — component pricing

When key is available:
1. Implement `fetch()` with API key auth
2. Search by MPN from `component_basket.yml` seed
3. Test end-to-end

---

## Thread 2: Farnell fetch() implementation

**Status:** Parser ready, fetch stub
**Blocker:** Need API key set as `FARNELL_API_KEY` env var
**Parser:** Extracts MPN, brand, price (GBP), stock, lead time from JSON
**API:** element14 Product Search API (free key)
**Effort:** 2-3 days
**Priority:** P0 — UK component pricing

Same pattern as Mouser. When key available, implement `fetch()`.

---

## Thread 3: LCSC fetch() implementation

**Status:** Parser ready, fetch stub
**Blocker:** Need API key set as `LCSC_API_KEY` env var
**Parser:** Extracts MPN, brand, price (CNY), stock, grade from JSON
**API:** LCSC Open API
**Effort:** 2-3 days
**Priority:** P0 — China component pricing

Same pattern as Mouser/Farnell. When key available, implement `fetch()`.

---

## Thread 4: eBay UK fetch() implementation

**Status:** Parser ready, fetch stub + location bug
**Blocker:** Need `EBAY_APP_ID` + OAuth 2.0 setup (more complex than simple API key)
**Parser:** Extracts item ID, title, price, condition, seller
**Bug:** `location` field mapped to `itemEndDate` instead of actual location
**Effort:** 3-4 days
**Priority:** P1 — used market data

eBay uses OAuth client credentials flow, not simple API key. Needs:
1. Register eBay developer account
2. Create app, get client_id + client_secret
3. Implement OAuth token fetch
4. Fix location bug in parser

---

## Thread 5: BARA directory — JS-rendered

**Status:** Structural blocker
**Current:** Raw HTML is a JavaScript redirect page (`window.location.href="/lander"`)
**URL:** automate.org.uk/member-directory
**Options:**
1. Find API endpoint behind the JS
2. Use headless browser (playwright/selenium)
3. Accept as evidence-only
**Effort:** Unknown — needs investigation
**Priority:** P2 — integrator directory

---

## Thread 6: RBTX marketplace — JS-rendered

**Status:** Structural blocker
**Current:** Product listings rendered by JavaScript, static HTML has no product data
**URL:** rbtx.co.uk, rbtx.igus.cn
**Options:**
1. Find API endpoint behind the JS
2. Use headless browser
3. Accept as evidence-only
**Effort:** Unknown — needs investigation
**Priority:** P2 — robot pricing

---

## Thread 7: Apprenticeships — JS-rendered landing page

**Status:** Structural blocker
**Current:** Landing page with links to search services, no actual listings in static HTML
**URL:** gov.uk/apply-apprenticeship
**Options:**
1. Use `findapprenticeship.service.gov.uk` search API directly
2. Use headless browser
**Effort:** Low if API found
**Priority:** P2 — labour signals

---

## Thread 8: HMRC trade statistics parser

**Status:** Raw HTML stored, no structured parsing
**Current:** Fetches uktradeinfo.com/trade-statistics/ page, stores HTML
**What's needed:** Parse trade statistics tables (commodity code, value, volume, partner countries)
**Effort:** 2-3 days
**Priority:** P1 — trade flow data

The traders CSV is parsed (561 businesses), but the trade statistics (values, volumes, trends) are not.

---

## Thread 9: ONS PPI parser

**Status:** Raw HTML stored, no structured parsing
**Current:** Fetches ONS inflation/price indices page, stores HTML
**What's needed:** Parse price index time series (index name, date, value, category)
**Effort:** 2-3 days
**Priority:** P1 — UK price signals

---

## Thread 10: BGS minerals parser

**Status:** Raw HTML stored, no structured parsing
**Current:** Fetches BGS World Mineral Statistics page, stores HTML
**What's needed:** Parse mineral statistics tables (mineral, production, UK imports)
**Effort:** 2-3 days
**Priority:** P2 — material supply

---

## Thread 11: powops /root/powuk permission error

**Status:** powops bug, not powrobots
**Error:** `PermissionError: [Errno 13] Permission denied: '/root/powuk'`
**Cause:** New powops commit added gardens at `/root/powuk` and `/root/powstock`
**Impact:** powops `check_all()` fails — doesn't affect powrobots
**Workaround:** Check powrobots specifically instead of full `check_all()`
**Fix:** Either fix paths in powops sources.yaml or add error handling in garden.py
**Priority:** Medium

---

## Thread 12: eBay parser location bug

**Status:** Bug in ebay_uk.py
**Line:** `ebay_uk.py` maps `location` to `itemEndDate`
**Impact:** Location data is wrong when eBay fetch() is implemented
**Fix:** Map `location` to `item.get('itemWebUrl', '')` or correct field
**Effort:** 5 minutes
**Priority:** Low (won't matter until fetch() is implemented)

---

## Thread 13: seed_loader.py on VPS

**Status:** Completed
**Action:** Run `scripts/seed_loader.py` on VPS to populate entity graph
**Result:** 123 models, 32 components, 29 relations populated
**Note:** This is done — no action needed

---

## Thread 14: No manufacturer seed component_categories

**Status:** Seed loader loaded 0 component categories
**Cause:** `component_categories.yml` format may not match loader expectations
**Impact:** component_category table is empty
**Effort:** Low — fix seed format or loader
**Priority:** Low

---

## Thread 15: powproducts CI failure

**Status:** External (powproducts repo)
**Issue:** Latest GitHub Actions test run failed in powproducts
**Impact:** Cross-repo integration may be affected
**Effort:** Investigate and fix in powproducts repo
**Priority:** Medium — blocks Phase 6 integration

---

## Thread 16: Vendor repo parsing

**Status:** 7 repos cloned, not parsed
**Repos:** ABB, awesome-robot-descriptions, FANUC, KUKA, MuJoCo Menagerie, Universal Robot, urdf_files_dataset
**What's needed:** URDF parser to extract robot specs, BOM parser for component relations
**Effort:** High (5-7 days for BOM parser)
**Priority:** P1 — entity graph from live data
**Value:** Highest — populates robot→component→supplier graph without API access

---

## Thread 17: No integration tests

**Status:** Tests exist but only use mocks
**What's needed:** Tests against recorded API responses or live APIs (behind flag)
**Effort:** Medium (3-4 days)
**Priority:** P1 — quality assurance

---

## Thread 18: No R2 backup

**Status:** Raw data not backed up to cloud
**What's needed:** R2 sync script, credentials, verification
**Effort:** Medium (2-3 days)
**Priority:** P2 — data safety

---

## Thread 19: DuckDB analytical layer

**Status:** Deferred per review.md
**When:** When SQLite query complexity demands it
**What:** Analytical queries across large datasets, Parquet export
**Effort:** High
**Priority:** Phase 3+

---

## Thread 20: UN Comtrade collector

**Status:** Not implemented
**What:** Global trade flow data for robotics commodity codes
**Effort:** High (needs API registration + complex data)
**Priority:** Phase 4 — global flow garden

---

## Decision log

### 2026-09-23: CSV over HTML for HMRC traders
HMRC provides CSV download endpoint. Decided to fetch CSV instead of parsing HTML tables. More reliable, structured, and includes all 564 traders (not paginated 50 per page).

### 2026-09-23: Skip JS-rendered pages
BARA, RBTX, and apprenticeships all require JavaScript. Decided to accept as evidence-only for now rather than introduce browser automation dependency. Revisit when API endpoints are discovered.

### 2026-09-23: Collection receipt format aligned with roadmap
Added collector_sha, cursor_before/after, validation_passed, schema_version to collector_run. This aligns with roadmap Phase 2 receipt format without breaking existing consumers.

### 2026-09-23: source_health auto-computed
Decided to compute source_health automatically in log_run() rather than requiring separate computation step. Ensures health is always up-to-date after every collection run.
