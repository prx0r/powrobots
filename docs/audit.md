# Audit — POWRobots Repository

Full inventory of every file. What it does, whether it's used, whether it's stale.

Generated 2026-09-23 from live code inspection.

---

## Quick status

| Category | Active | Stale/Unused |
|----------|--------|-------------|
| Core infrastructure | 8 files | 0 |
| Working collectors | 6 | 0 |
| Stub collectors (need fetch) | 4 | 0 |
| Limited collectors (JS-blocked) | 3 | 0 |
| Stub collectors (need parser) | 2 | 0 |
| BOM engine | 0 | 1 (resolve.py) |
| Placeholder packages | 0 | 3 |
| Seed data | 5 used | 3 unused |
| Scrapers | 2 (parallel system) | 0 |
| Tests | 1 | 0 |
| Deployment | 3 | 0 |
| Docs | 15 | 0 |

---

## Core infrastructure

### `powrobots/__init__.py`
**Status:** ACTIVE — package init

### `powrobots/cli.py` (301 lines)
**Status:** ACTIVE — CLI entry point, 10 commands, all 15 collectors registered
**Commands:** status, sources, seed, collect, validate, health, robots, models, components, organisations

### `powrobots/shared/db.py` (860 lines)
**Status:** ACTIVE — schema (32 tables), seed data, get_db(), seed_rights(), seed_registry()
**This is the foundation. Everything depends on it.**

### `powrobots/shared/persist.py` (328 lines)
**Status:** ACTIVE — store_raw(), insert_source_record(), log_run(), compute_source_health(), upsert_*(), insert_relation()

### `powrobots/core/enums.py` (143 lines)
**Status:** PARTIALLY USED — tests verify enums exist, but no collector uses them. Everything uses raw strings instead.
**Fix:** Collectors should reference enums instead of raw strings.

---

## Collectors

### Working (structured data extraction)

| File | Lines | Records | Status |
|------|-------|---------|--------|
| `hmrc_traders.py` | 108 | 561 | BEST — CSV parser, fully working |
| `companies_house.py` | 126 | 250 | WORKING — needs COMPANIES_HOUSE_API_KEY |
| `opss_safety.py` | 114 | 50 | WORKING — HTML parser |
| `contracts_finder.py` | 147 | 20 | WORKING — intermittent fetch failures |
| `ukri_gtr.py` | 110 | 0 | WORKING — no new results on re-runs |

### Stub (parser ready, fetch not implemented)

| File | Lines | Status | What's needed |
|------|-------|--------|---------------|
| `mouser.py` | 62 | STUB | MOUSER_API_KEY + fetch() implementation |
| `farnell.py` | 64 | STUB | FARNELL_API_KEY + fetch() implementation |
| `lcsc.py` | 61 | STUB | LCSC_API_KEY + fetch() implementation |
| `ebay_uk.py` | 65 | STUB | EBAY_APP_ID + OAuth + location bug fix |

### Limited (JS-blocked or stub parser)

| File | Lines | Status | Issue |
|------|-------|--------|-------|
| `rbtx.py` | 62 | JS-blocked | Product listings require JavaScript |
| `bara_directory.py` | 49 | JS-blocked | Directory page requires JavaScript |
| `apprenticeships.py` | 48 | JS-blocked | Landing page only |
| `ons_ppi.py` | 48 | Stub parser | Stores metadata, not actual PPI data |
| `bgs_minerals.py` | 45 | Stub parser | Stores metadata, not actual statistics |

---

## BOM engine (DEAD CODE)

### `powrobots/resolve.py` (247 lines) # STALE — not imported anywhere

**Status:** STALE — complete and well-designed, but zero imports. Not used by CLI, collectors, tests, or scripts.

**What it does:** `resolve_bom()`, `find_substitutes()`, `optimize_bom()` — BOM resolution and substitution engine.

**Why it's stale:**
- No CLI command exposes it
- No collector populates the `distributor` table it queries
- No API-key collectors populate `component_market_observation`
- No tests cover these functions

**What would make it live:**
1. Populate `distributor` table (Mouser, Farnell, LCSC, eBay entries)
2. Implement API-key collectors so pricing data exists
3. Add CLI commands: `powrobots resolve <model_id>`, `powrobots substitutes <component_id>`
4. Add tests for these functions
5. Wire to MCP for agent access

---

## Placeholder packages (ABANDONED)

### `powrobots/parsers/__init__.py` # STALE — empty placeholder
**Intended:** Dedicated parser modules extracted from collectors.
**Reality:** All parsing is done inline in each collector's `parse()` method.

### `powrobots/registry/__init__.py` # STALE — empty placeholder
**Intended:** Source registry logic.
**Reality:** Registry logic lives in `shared/db.py` (seed_registry(), SOURCES_SEED).

### `powrobots/layer1/__init__.py` # STALE — empty placeholder
**Intended:** Layer 1-specific derived signal code.
**Reality:** No code was ever written here.

---

## Seed data

### Used by seed_loader.py
| File | Records | Status |
|------|---------|--------|
| `manufacturers.yml` | 25 | ACTIVE |
| `component_categories.yml` | 24 | ACTIVE |
| `component_basket.yml` | ~35 | ACTIVE |
| `ros_repositories.yml` | 5 | ACTIVE |
| `chinese_stocks.yml` | 7 | ACTIVE |

### Used in tests only
| File | Records | Status |
|------|---------|--------|
| `hs_codes.yml` | 13 | TESTS ONLY — not loaded at runtime |
| `china_production.yml` | 5 | TESTS ONLY — not loaded at runtime |

### Never used
| File | Records | Status |
|------|---------|--------|
| `search_terms.yml` | 37 | NEVER USED — not loaded, not tested, not referenced |

---

## Scrapers (parallel system)

### `scrapers/apify_suppliers.py` (150 lines)
**Status:** PARTIALLY USED — requires APIFY_TOKEN, not integrated into main CLI
**Does:** AliExpress, Amazon UK, eBay UK scraping via Apify actors

### `scrapers/run_all.py` (137 lines)
**Status:** PARTIALLY USED — orchestrator for scrapers, has own GitHub Actions workflow
**Does:** Batch scraping, stores as component_market_observation

**Note:** These operate as a separate system from the main collectors. They could be integrated as new collectors, or kept as a parallel tool.

---

## What's actually stale

| File | Why stale | Action |
|------|-----------|--------|
| `resolve.py` | Dead code — 247 lines, zero imports | Either wire it up or remove it |
| `parsers/__init__.py` | Empty placeholder | Remove or populate |
| `registry/__init__.py` | Empty placeholder | Remove or populate |
| `layer1/__init__.py` | Empty placeholder | Remove or populate |
| `seeds/search_terms.yml` | Never loaded, never tested | Remove or use in collector configs |
| `core/enums.py` | Tests only, not enforced | Use in collectors or remove |

---

## What's NOT stale but needs work

| File | Issue | Fix |
|------|-------|-----|
| `ebay_uk.py` | location bug (line 52) | Map to correct field |
| `ons_ppi.py` | Stub parser (metadata only) | Parse actual PPI time series |
| `bgs_minerals.py` | Stub parser (metadata only) | Parse actual mineral statistics |
| `mouser.py` | fetch() stub | Implement with MOUSER_API_KEY |
| `farnell.py` | fetch() stub | Implement with FARNELL_API_KEY |
| `lcsc.py` | fetch() stub | Implement with LCSC_API_KEY |
| `ebay_uk.py` | fetch() stub | Implement with OAuth |
| `core/enums.py` | Not enforced | Use in collectors instead of raw strings |

---

## What IS the product?

### What we built
A data collection framework with 15 collectors, a BOM resolution engine, and a graph of 221 robots with 137 components and 234 relations.

### What LeRobot already does
LeRobot is the open-source robotics framework from Hugging Face. It provides:
- Robot arm control (SO-101)
- Teleoperation
- Imitation learning
- Data collection
- Model training

**LeRobot does NOT provide:**
- Cross-brand parts compatibility
- Multi-supplier pricing intelligence
- UK landed costs
- Repair outcome tracking
- BOM-to-manufacturing pipeline

### Our actual wedge
**The graph that connects broken robots to verified parts with live UK pricing.**

Not the design tool (LeRobot/Blender has that).
Not the manufacturing (JLCPCB/Seeed has that).
Not the parts search (FixPart/RobotShop has that).

**The verified, cross-model, multi-supplier, UK-priced compatibility intelligence that none of them have.**

### What we should focus on
1. Get the API-key collectors working (Mouser, Farnell, LCSC) — this gives us real pricing
2. Wire resolve.py to CLI — this makes the graph queryable
3. Do the SO-101 vertical slice — one robot, full BOM, real quotes
4. Stop adding robots to the graph until we sell something
