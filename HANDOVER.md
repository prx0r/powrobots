# HANDOVER.md

What exists, what works, what doesn't, and what to do next.

**Date:** 2026-09-23
**Repo:** prx0r/powrobots
**Latest commit:** 8428697
**Tests:** 42/42 passing

---

## What exists

### Collectors (15 total)

| Collector | Status | Records | Parser | Fetch | Notes |
|-----------|--------|---------|--------|-------|-------|
| hmrc_traders | ok | 561 | CSV | live | 561 UK businesses trading HS 847950 |
| companies_house | ok | 250 | JSON | live | 250 robotics companies from Companies House |
| opss_safety | ok | 50 | HTML | live | 50 product safety alerts |
| contracts_finder | intermittent | 20 | HTML | sometimes | Site blocks occasionally |
| ukri_gtr | ok | 0 | XML | live | Already collected, no new results |
| hmrc_trade | ok | 1 | HTML stub | live | Needs parser |
| bgs_minerals | ok | 1 | HTML stub | live | Needs parser |
| ons_ppi | ok | 1 | HTML stub | live | Needs parser |
| bara_directory | ok | 1 | JS-blocked | live | Can't parse static HTML |
| find_apprenticeship | ok | 1 | JS-blocked | live | Landing page only |
| rbtx | ok | 2 | JS-blocked | live | Product listings need JS |
| mouser | no_key | 0 | parser ready | stub | Needs MOUSER_API_KEY |
| farnell | no_key | 0 | parser ready | stub | Needs FARNELL_API_KEY |
| lcsc | no_key | 0 | parser ready | stub | Needs LCSC_API_KEY |
| ebay_uk | no_key | 0 | parser ready | stub | Needs EBAY_APP_ID + OAuth |

### Entity graph

| Table | Count | Source |
|-------|-------|--------|
| organisation | 856 | 561 HMRC + 250 Companies House + 20 buyers + 25 seeds |
| robot_model | 123 | Seed loader (YAML + vendor repos) |
| robot_manufacturer | 26 | Seed loader |
| component | 32 | Seed basket |
| product_relation | 29 | Seed loader |
| component_manufacturer | 23 | Seed loader |

### Infrastructure

- SQLite schema: 32 tables, auto-applied
- Raw storage: gzip, content-addressed, ~356KB
- Source rights: 15 seeded (10 open, 5 approved)
- Source registry: 15 seeded
- Collector run history: 24 rows
- Source health: 15 rows (all sources)
- Systemd: 6h timer
- CI: GitHub Actions (pytest + ruff)
- powops: fully wired, all 15 sources visible

### Documentation (14 files)

| File | Lines | Purpose |
|------|-------|---------|
| README.md | ~150 | Entry point for new agents |
| AGENTS.md | ~300 | powops wiring guide |
| docs/BUILD_NOTES.md | ~400 | Complete build state |
| docs/devplan.md | ~880 | 8-phase roadmap |
| docs/devplanresponse.md | ~270 | Global devplan mapping |
| docs/repair-outcome-vision.md | ~200 | Repair-decision vision |
| docs/threads.md | ~300 | 20 open threads |
| docs/blockers.md | ~120 | 16 blockers |
| docs/northstar.md | ~2500 | Master design |
| docs/review.md | ~68 | Design review |
| docs/cross_repo_review.md | ~83 | Cross-repo compatibility |
| docs/northstar_v2.md | ~87 | China→UK strategy |
| docs/API_KEYS.md | ~102 | API key inventory |
| HANDOVER.md | this file | What to do next |

---

## What works end-to-end

```
1. powrobots seed          → source_rights + source_registry populated
2. powrobots collect all   → 10 collectors fetch live data
3. powrobots health        → shows last run per source
4. powrobots robots        → entity graph summary
5. powrobots models        → 123 robot models listed
6. powrobots components    → 32 components listed
7. powops status           → shows powrobots sources as ok/no_key
8. powops MCP              → exposes powrobots data to agent
9. systemd timer           → runs collectors every 6h
```

---

## What to do next

### Immediate (unblocks most value)

1. **Set API keys** — companies_house is working. Set the other 4:
   ```bash
   export MOUSER_API_KEY=xxx
   export FARNELL_API_KEY=xxx
   export LCSC_API_KEY=xxx
   export EBAY_APP_ID=xxx
   ```
   Then `python3 -m powrobots.cli collect all` activates 5 more collectors.

2. **Run seed_loader.py** — already done on VPS but ensure it runs after any schema changes.

3. **Re-run contracts_finder** — fetch is intermittent. Run again when site is available.

### Short-term (this week)

4. **Parse HMRC trade statistics** — the traders CSV is parsed (561 businesses) but the trade statistics (values, volumes, trends) are not. The raw HTML is in `warehouse/raw/hmrc_trade/`.

5. **Parse ONS PPI** — price index time series needed for component pressure signals.

6. **Implement eBay fetch()** — needs OAuth setup (more complex than simple API key).

### Medium-term (next 2 weeks)

7. **URDF parser** — parse vendor repos (ABB, FANUC, KUKA, Universal Robot) into entity graph. This is the highest-value unbuilt collector.

8. **BOM parser** — extract component relations from open-source robot projects.

9. **Mouser/Farnell/LCSC fetch()** — implement API calls for component pricing.

### Longer-term (month+)

10. **powproducts integration** — share component identity across repos.
11. **repair integration** — link robot models to fault records.
12. **Derived signals** — import pulse, component pressure, used robot liquidity.

---

## How to run

```bash
# Install
pip install -e ".[dev]"

# Initialize
python3 -m powrobots.shared.db
python3 -m powrobots.cli seed

# Collect
python3 -m powrobots.cli collect all
python3 -m powrobots.cli collect hmrc_traders  # single source

# Check
python3 -m powrobots.cli health
python3 -m powrobots.cli robots
python3 -m powrobots.cli models

# Test
POWROBOTS_DB=/tmp/test.db python3 -m pytest tests/ -v
```

---

## Key decisions made

1. **CSV over HTML for HMRC** — more reliable, structured, includes all 564 traders
2. **Skip JS-rendered pages** — BARA, RBTX, apprenticeships need browser automation
3. **Auto-compute source_health** — in log_run(), not separate step
4. **Collection receipt format** — aligned with roadmap Phase 2
5. **POWOps as operational surface** — no separate MCP server in powrobots

---

## What powops sees

```
powrobots: 10/15 ok | 5/15 no_key

  ACTIVE:     hmrc_traders, hmrc_trade, ukri_gtr, contracts_finder,
              opss_safety, bara_directory, bgs_minerals, ons_ppi,
              find_apprenticeship, rbtx

  NEEDS KEY:  companies_house (working), mouser, farnell, lcsc, ebay_uk
```

MCP: `powops_status(garden="powrobots")` returns all 15 with status, age, records.

---

## Contacts

- Repository: https://github.com/prx0r/powrobots
- Dashboard: https://admin.pow.systems
- Sister repos: powpowpow, powuk, powstock, repair, powproducts, powphysical, powk, powops
