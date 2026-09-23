# AGENTS.md — POWRobots

Everything a fresh agent needs to know about this repository.

---

## What this is

POWRobots is a **platform for personalised physical robotics products**. It has three layers:

1. **Engines** — 5 reusable electronics platforms (SENSE, REMEMBER, ACT, TALK, SEE)
2. **Parts graph** — 143 components, 16 suppliers, 129 prices, 234 compatibility relations
3. **MCP** — API that connects AI agents (Muse, ChatGPT) to the parts graph

The platform lets anyone design, build, and sell custom robot companions (called **Glimlings**).

---

## Core concepts

### Engine
A reusable electronics platform that provides a specific capability.

| Engine | Capability | Key components |
|--------|-----------|---------------|
| **SENSE** | Reads moisture, light, temp, NFC | ESP32, sensors |
| **REMEMBER** | Keeps time, tracks history | ESP32, RTC, SD |
| **ACT** | Controls lights, servos, relays | ESP32, servo, LED, relay |
| **TALK** | Speaks, listens, buttons | ESP32, speaker, mic |
| **SEE** | Captures images, motion | ESP32-CAM, servos |

### Product
A personalised physical companion built from one or more engines + enclosure + customisation.

Examples: Plant Sprite (SENSE+ACT), Desk Goblin (ACT+display), Glimlings (any engine combination).

### Glimling
A named, personalised creature that inhabits an everyday object and connects to an AI agent.

Brand: **Glimlings** — "Little spirits for the things you love."
Individual: **A Glimling** — each has its own name, personality, and digital identity.

### Parts graph
The knowledge base of which components exist, what they cost, which suppliers sell them, and which parts are compatible with which robots.

### MCP (Model Context Protocol)
The API that lets AI agents query the parts graph. Muse, ChatGPT, or any MCP-compatible agent can use it.

---

## How to run

```bash
pip install -e ".[dev]"
python3 -m powrobots.shared.db      # init database
python3 -m powrobots.cli seed       # seed rights + registry
python3 -m powrobots.cli collect all # run all collectors
python3 -m powrobots.cli health     # check status
python3 -m powrobots.cli robots     # entity graph summary
python3 -m powrobots.cli models     # list robot models
python3 -m powrobots.cli components # list components
POWROBOTS_DB=/tmp/test.db python3 -m pytest tests/ -v
```

---

## CLI commands

| Command | What it does |
|---------|-------------|
| `status` | Database row counts |
| `sources` | List registered sources |
| `seed` | Seed source_rights + source_registry |
| `validate` | Check everything is wired |
| `health` | Last collector run per source |
| `robots` | Entity graph summary |
| `models` | List all robot models |
| `components` | List all components |
| `organisations` | List organisations (first 50) |
| `collect <source>` | Run a collector |
| `collect all` | Run all collectors |

---

## Architecture

```
Collectors → Raw storage → Source records → Entity graph
     ↓                                        ↓
collector_run                        powops monitors via collector_db
     ↓                                            ↓
powops health                      MCP / Dashboard / CLI
```

### Key files

| File | What it does |
|------|-------------|
| `powrobots/cli.py` | CLI entry point (15 collectors, 10 commands) |
| `powrobots/collectors/base.py` | Base collector with retry + raw storage |
| `powrobots/collectors/*.py` | 15 source collectors |
| `powrobots/resolve.py` | BOM resolution + substitution engine |
| `powrobots/mcp.py` | MCP server for Muse/ChatGPT integration |
| `powrobots/shared/db.py` | Schema + seeds + source_health computation |
| `powrobots/shared/persist.py` | Storage + entity graph operations |
| `powrobots/core/enums.py` | Domain enums (RobotType, ComponentCategory) |
| `enclosures/generate.py` | Parametric STL enclosure generator |
| `firmware/plant-sprite/main.py` | ESP32 firmware for plant monitoring |
| `firmware/desk-goblin/main.py` | ESP32 firmware for desk companion |
| `scripts/seed_loader.py` | Entity graph seeder |
| `tests/test_core.py` | 42 tests |

---

## How to add a new engine

1. Define engine name and capability
2. List required components in `powrobots/seeds/component_basket.yml`
3. Add components to database via `seed_loader.py`
4. Create enclosure template in `enclosures/generate.py`
5. Create firmware in `firmware/<engine-name>/main.py`
6. Register as product in `product` table
7. Add to MCP tools in `powrobots/mcp.py`

### Engine criteria

An engine must:
- Be buildable from 3-5 off-the-shelf components
- Cost under £20 in parts
- Have a clear capability (sense, remember, act, talk, see)
- Be compatible with ESP32-class controllers
- Be producible at scale (JLCPCB + JLC3DP)

---

## How to add a new product

1. Choose engine combination (e.g. SENSE + ACT)
2. Create enclosure design (Blender/OpenSCAD)
3. Run `resolve_bom()` to verify parts exist
4. Add to `product` table with pricing
5. Add character variants to `product_variant` table
6. Create Etsy listing template
7. Test manufacturing pipeline (JLCPCB → JLC3DP → assembly)

### Product criteria

A product must:
- Use 1-3 engines
- Have a unique enclosure design
- Be personalisable (name, colour, character)
- Have >40% margin at retail
- Be manufacturable (JLCPCB + JLC3DP + assembly)

---

## How to add a new supplier

1. Add to `source_rights` table (status: open/approved)
2. Add to `source_registry` table (authority, cadence, tier)
3. Add collector in `powrobots/collectors/<name>.py`
4. Add to `COLLECTORS` dict in `cli.py`
5. Run `powrobots seed` (idempotent)
6. Run `powrobots collect <source>`
7. powops sees it via collector_db

---

## How to add a new component

1. Add to `powrobots/seeds/component_basket.yml`
2. Run `scripts/seed_loader.py` to populate
3. Add pricing observations to `component_market_observation`
4. Add `REQUIRES` relations from robots that use it
5. Add `COMPATIBLE_WITH` relations for alternatives

---

## The MCP (what AI agents see)

### Tools

| Tool | What it answers |
|------|----------------|
| `pow_resolve_bom(model_id)` | "What parts does this robot need and what do they cost?" |
| `pow_find_substitutes(component_id)` | "What else fits this slot?" |
| `pow_optimize_bom(model_id, strategy)` | "What's the cheapest/fastest way to get these parts?" |
| `pow_quote_build(model_id)` | "What's the full assembly cost?" |
| `pow_list_components(query)` | "Show me all servos / sensors / ESP32 boards" |
| `pow_robot_info(model_id)` | "Tell me about this robot model" |
| `pow_list_robots(robot_type)` | "Show me all robot vacuums" |
| `pow_list_products(product_line)` | "Show me all Glimlings" |

### Integration with Muse

```
Muse → Blender MCP → creates 3D design
Muse → POW MCP → resolves BOM
Muse → customer → approves quote
Muse → manufacturing → places order
```

---

## Data flow

```
1. Collectors fetch data from public sources
2. Raw blobs stored in warehouse/raw/
3. Source records created in source_record table
4. Entity graph populated (organisations, models, components)
5. Powops monitors via collector_db
6. MCP exposes graph to AI agents
7. resolve_bom() returns parts + prices
8. Manufacturing pipeline assembles product
9. Product ships to customer
```

---

## What's in the database

| Table | Rows | What |
|-------|------|------|
| organisation | 856 | UK businesses, traders, buyers |
| robot_manufacturer | 44 | Robot manufacturers |
| robot_model | 221 | Robot models (industrial + consumer) |
| component | 143 | Electronic + mechanical parts |
| product_relation | 234 | REQUIRES + COMPATIBLE_WITH |
| distributor | 16 | Suppliers (UK, China, US) |
| component_market_observation | 129 | Prices from multiple suppliers |
| collector_run | 24 | Health check history |
| source_health | 15 | Current health status |
| kit | 10 | Curated product bundles |
| product | 11 | Glimlings product catalogue |
| product_variant | 19 | Character + colour options |

---

## Blockers (see docs/blockers.md)

1. Mouser/Farnell/LCSC need API keys for structured pricing
2. eBay needs OAuth setup
3. BARA/RBTX/apprenticeships are JS-rendered
4. powops can't query entity graph directly (by design)
5. 5 API-key collectors have fetch() stubs

---

## Design principles

1. **Modular** — engines are independent, products compose them
2. **Extensible** — new engines, products, and suppliers are easy to add
3. **Open** — MCP exposes everything to any AI agent
4. **Personalised** — every product has name, colour, character
5. **Manufacturable** — every design must be buildable (JLCPCB + JLC3DP)
6. **Tested** — every component has verified compatibility
