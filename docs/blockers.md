# Blockers

Things I cannot do right now. Each entry has what's blocked, why, and what unblocks it.

---

## 1. API keys not configured

**Blocked:** Companies House, Mouser, Farnell, LCSC, eBay collectors
**Why:** No API keys set in environment
**Unblock:** Register for free API keys, set env vars:
```
COMPANIES_HOUSE_API_KEY=
MOUSER_API_KEY=
FARNELL_API_KEY=
LCSC_API_KEY=
EBAY_APP_ID=
```
**Status:** Open — registrations documented in docs/API_KEYS.md

---

## 2. seed_loader.py not run on VPS

**Blocked:** Manufacturer, model, component entity graph population from seeds
**Why:** Script exists but hasn't been executed in production
**Unblock:** `cd /home/ubuntu/powrobots && PYTHONPATH=/home/ubuntu python3 scripts/seed_loader.py`
**Note:** Tests use temp DB so seeds aren't in production warehouse

---

## 3. ~~No BeautifulSoup/lxml dependency~~ RESOLVED

**Status:** DONE — beautifulsoup4 and lxml installed and added to pyproject.toml

---

## 4. powops powuk/powstock paths permission error

**Blocked:** powops `check_all()` fails when encountering `/root/powuk` path
**Why:** New powops commit added gardens with paths we can't access
**Unblock:** Fix paths in powops sources.yaml to point to accessible locations, or add error handling in garden.py
**Status:** powrobots works fine — only affects powops full-system check

---

## 5. No integration tests against live APIs

**Blocked:** Verifying collectors actually work end-to-end with real HTTP
**Why:** No test infrastructure for live API testing
**Unblock:** Create test fixtures with recorded responses, or add live API tests behind a flag
**Status:** Mock tests pass — live testing is a Phase 8 item

---

## 6. No CI/CD pipeline

**Blocked:** Automated testing on push, deployment verification
**Why:** No .github/workflows directory
**Unblock:** Create GitHub Actions workflow for pytest + ruff
**Status:** Can be done now

---

## 7. No R2 backup configured

**Blocked:** Raw data archival and restore testing
**Why:** No r2_sync.sh script, no Cloudflare R2 credentials
**Unblock:** Set up R2 bucket, create sync script, configure credentials
**Status:** Phase 5 item

---

## 8. eBay API requires OAuth setup

**Blocked:** eBay Browse API fetch() implementation
**Why:** eBay uses OAuth 2.0 client credentials flow, not simple API key
**Unblock:** Register eBay developer account, create app, get client_id + client_secret
**Status:** More complex than other API keys

---

## 9. No DuckDB for analytical queries

**Blocked:** Complex analytical queries across large datasets
**Why:** SQLite is sufficient for now, DuckDB deferred per review.md
**Unblock:** Install DuckDB, create analytical layer when query complexity demands it
**Status:** Phase 3+ item — not needed yet

---

## 10. JS-rendered pages can't be parsed from static HTML

**Blocked:** BARA directory, RBTX marketplace, apprenticeships landing page
**Why:** These pages use JavaScript to render content — the raw HTML fetched by requests is just a shell/redirect
**Unblock:** Use a headless browser (playwright/selenium) or find API endpoints behind the JS
**Status:** Structural limitation — need to find API endpoints or use browser automation
**Workaround:** BARA has no usable data. RBTX product data requires API. Apprenticeships requires the search API at `findapprenticeship.service.gov.uk`.

## 11. ~~Companies House API key obtained~~ RESOLVED

**Status:** DONE — Companies House fetch() implemented, 250 companies parsed

---

## 12. Manufacturer documentation access varies

**Blocked:** Some manufacturer docs require customer/dealer login (FANUC MyPortal, Universal Robots parts catalogue)
**Why:** Not all repair documentation is public
**Unblock:** Partner with repair businesses who have access, or use publicly available subsets
**Status:** Structural limitation — work with what's public first

---

## 13. contracts_finder fetch intermittent failures

**Blocked:** Sometimes fetches fail (site blocks or is down)
**Why:** UK government sites may rate-limit or have uptime issues
**Impact:** procurement_notice table stays empty
**Workaround:** Re-run collector, or parse from existing raw blobs
**Status:** Intermittent — not a code bug

---

## 14. grant_project only populated on new results

**Blocked:** ukri_gtr returns 0 new results when already collected
**Why:** grant_project write only runs when parse() finds new projects
**Impact:** grant_project table empty despite data existing in source_record
**Workaround:** Backfill from existing source_records
**Status:** Design limitation — not a bug

---

## 15. No MCP server in powrobots

**Blocked:** powrobots has no own MCP server
**Why:** Relies on powops MCP for exposure
**Impact:** Agent can only query powrobots via powops, not directly
**Workaround:** Use powops MCP tools
**Status:** By design — powops is the operational surface

---

## 16. powops can't query entity graph

**Blocked:** powops only reads collector_run and source_health
**Why:** Entity graph tables (organisation, robot_model, component) not exposed via powops
**Impact:** powops can't show entity counts or model/component data
**Workaround:** Use powrobots CLI (`powrobots robots`, `powrobots models`)
**Status:** Could add powrobots-specific MCP tools or summary view
