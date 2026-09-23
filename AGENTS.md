# AGENTS.md — POWRobots

Everything a fresh agent needs to know about this repository.

---

## What this is

POWRobots is a **platform for personalised physical robotics products**. It has three layers:

1. **Engines** — 6 reusable electronics platforms (SENSE, REMEMBER, ACT, TALK, SEE, COMPANION)
2. **Parts graph** — 177 components, 16 suppliers, 129 prices, 280 compatibility relations
3. **MCP** — API that connects AI agents (Muse, ChatGPT) to the parts graph

The platform lets anyone design, build, and sell custom robot companions (called **Glimlings**).

---

## Current Strategy (September 2026)

### The Business

**Sell one original Glimling starter kit, then build an open "plant homelab" around it.**

- **Hero product:** Sporebert Indoor Starter (£79.99)
- **Add-on economy:** heads, caps, stands, aesthetic packs
- **Open compatible network:** "works with" third-party sensors
- **Later:** own cheaper indoor Plantling node

### Channel Split

| Channel | What to Sell |
|---------|--------------|
| **Etsy** | Original POW products (Glimlings, heads, caps) |
| **Own site** | Compatibility marketplace, referrals, subscriptions |

**Do NOT resell third-party sensors on Etsy.** Etsy prohibits reselling commercially available items.

### Revenue Streams

| Stream | Source |
|--------|--------|
| Glimling hardware | One-time sale |
| Interchangeable heads | Accessory sales |
| App subscriptions | Recurring software |
| Sensor referrals | Affiliate fees (4-8%) |

---

## Core Concepts

### Engine
A reusable electronics platform that provides a specific capability.

| Engine | Capability | Key components |
|--------|-----------|---------------|
| **SENSE** | Reads moisture, light, temp, NFC | ESP32, sensors |
| **REMEMBER** | Keeps time, tracks history | ESP32, RTC, SD |
| **ACT** | Controls lights, servos, relays | ESP32, servo, LED, relay |
| **TALK** | Speaks, listens, buttons | ESP32, speaker, mic |
| **SEE** | Captures images, motion | ESP32-CAM, servos |
| **COMPANION** | Health monitoring, social | ESP32-S3, touchscreen, camera |

### Product
A personalised physical companion built from one or more engines + enclosure + customisation.

### Glimling
A named, personalised creature that inhabits an everyday object and connects to an AI agent.

Brand: **Glimlings** — "Little spirits for the things you love."
Individual: **A Glimling** — each has its own name, personality, and digital identity.

### Parts graph
The knowledge base of which components exist, what they cost, which suppliers sell them, and which parts are compatible with which robots.

### MCP (Model Context Protocol)
The API that lets AI agents query the parts graph. Muse, ChatGPT, or any MCP-compatible agent can use it.

---

## The Sensor Network Architecture

### Hub + Spoke Model

```
Glimling Hub (ESP32-S3)
    ↓
WiFi → Internet → MCP → Muse/ChatGPT
    ↓
Bluetooth → Plant Sensors (one per plant)
```

### Indoor vs Outdoor

| Type | Radio | Gateway | Sensors |
|------|-------|---------|---------|
| Indoor | Bluetooth | None (direct) | HHCC Flower Care, MiFlora |
| Outdoor | 868MHz | Ecowitt GW1200 | Ecowitt WH51/WH52 |

### "Glimling Compatible" Badge

- Validate existing sensors work with Glimlings
- Add "Glimling Compatible" badge
- Link to where to buy them
- Earn referral fees (4-8%)
- **Don't resell with a logo** (compliance risk)

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
| `powrobots/sdk.py` | SDK for programmatic access |
| `powrobots/shared/db.py` | Schema + seeds + source_health computation |
| `powrobots/shared/persist.py` | Storage + entity graph operations |
| `enclosures/generate.py` | Parametric STL enclosure generator |
| `enclosures/templates/*.scad` | OpenSCAD templates for each character |
| `firmware/plant-sprite/main.py` | ESP32 firmware for plant monitoring |
| `firmware/desk-goblin/main.py` | ESP32 firmware for desk companion |
| `firmware/plant-agent/main.py` | ESP32 firmware for plant agent |
| `tests/test_core.py` | 42 tests |

---

## Database

| Table | Rows | What |
|-------|------|------|
| organisation | 856 | UK businesses, traders, buyers |
| robot_manufacturer | 44 | Robot manufacturers |
| robot_model | 221 | Robot models (industrial + consumer) |
| component | 177 | Electronic + mechanical parts |
| product_relation | 280 | REQUIRES + COMPATIBLE_WITH |
| distributor | 16 | Suppliers (UK, China, US) |
| component_market_observation | 129 | Prices from multiple suppliers |
| collector_run | 24 | Health check history |
| source_health | 15 | Current health status |
| kit | 10 | Curated product bundles |
| product | 12 | Glimlings product catalogue |
| product_variant | 23 | Character + colour options |

---

## Doc Audit (September 2026)

### Active Docs (Current Strategy)

| Doc | Purpose |
|-----|---------|
| `canonical-product-stack.md` | Phase 1 catalogue, Etsy vs own-site, compatibility matrix |
| `canonicalgifts.md` | Core product and commercial model |
| `canonicalsensor.md` | Complete sensor family, sourcing, software spec |
| `cleanest-business.md` | Business model: sell one Glimling, build plant homelab |
| `all-indoor-strategy.md` | Indoor-first approach, product line |
| `what-to-offer.md` | What to sell on Etsy vs own site |
| `fast-path-third-party.md` | Buy third-party sensors, hook up to Glimlings |
| `chinese-suppliers-sensors.md` | Cheapest suppliers for sensors |
| `end-to-end-offerings.md` | Product economics with margins |
| `international-markets.md` | US, EU, AU expansion |
| `design-mcp-spec.md` | Design MCP validator specification |
| `modularglimling.md` | Swappable parts system |
| `network-sensor-architecture.md` | Hub + spoke sensor network |
| `swappable-parts-system.md` | Snap-on heads and accessories |

### Reference Docs (Historical/Technical)

| Doc | Purpose |
|-----|---------|
| `assembly-partners.md` | 8 assembly partners documented |
| `assembly-pipeline.md` | Manufacturing pipeline |
| `engines.md` | 6 engine definitions |
| `engine-pricing.md` | Engine cost breakdowns |
| `brand-identity.md` | Glimlings brand identity |
| `vision.md` | MCP-first product vision |
| `platform.md` | Engines + marketplace architecture |
| `pipeline-graph.md` | Full pipeline graph |
| `supplier-constraints.md` | Real MOQs, pricing, delivery |
| `product-templates.md` | Products mapped to parts |
| `consumer-agents.md` | Consumer agent integration |
| `wedge.md` | Competitive analysis |
| `ideas.md` | Product ideas |
| `devplan.md` | 8-phase development roadmap |
| `BUILD_NOTES.md` | Complete build documentation |

### Stale Docs (Superseded)

40 docs superseded by canonical documents. See `docs/` for full list.

---

## Suppliers

### Component Suppliers

| Supplier | Role | What to Source |
|----------|------|----------------|
| AliExpress | Development | ESP32 boards, prototype sensors |
| Alibaba | OEM quotations | Assembled sensors, bulk components |
| LCSC | Production electronics | Sensor ICs, ESP32 modules |
| JLCPCB | Custom PCB assembly | Complete electronics boards |
| JLC3DP | 3D printing | Enclosures, character shells |
| DFRobot | Specialist modules | pH, EC, pumps, probes |
| Ecowitt | Finished sensors | Outdoor sensors, gateways |

### Assembly Partners

| Partner | Location | MOQ | Services |
|---------|----------|-----|----------|
| Makerfabs | China | 1 | PCB, assembly, packing, dropship |
| UK Electronics | UK | 10 | Full box build |
| M-TEK | UK | Small | SMT, PTH, test |
| Prism Electronics | UK | 1 | Prototype specialist |
| Seeed Fusion | China | 1 | Full turnkey |

---

## The Sensor Network

### Indoor (Bluetooth)

| Sensor | Connection | Price | Status |
|--------|------------|-------|--------|
| HHCC Flower Care | Bluetooth direct | £14.99 | ✅ POW Tested |
| MiFlora | Bluetooth direct | £12.99 | ✅ POW Tested |

### Outdoor (868MHz + Gateway)

| Sensor | Connection | Price | Status |
|--------|------------|-------|--------|
| Ecowitt WH51 | 868MHz → Gateway | £14.50 | ✅ Bridge Required |
| Ecowitt WH52 | 868MHz → Gateway | £22.50 | ✅ Bridge Required |
| Ecowitt WH55 | 868MHz → Gateway | £12.99 | ✅ Bridge Required |

### Environment

| Sensor | Connection | Price | Status |
|--------|------------|-------|--------|
| DFRobot SEN0501 | I2C/GPIO | £24.00 | ⚠️ Community |
| DFRobot SEN0575 | Analog | £25.00 | ⚠️ Community |
| Seeed Grove Water Level | Analog | £6.50 | ⚠️ Community |
| Seeed Grove SCD41 | I2C | £42.00 | ⚠️ Community |

### Interaction

| Sensor | Connection | Price | Status |
|--------|------------|-------|--------|
| Seeed Grove PIR | GPIO | £7.00 | ⚠️ Community |
| DFRobot Sound Sensor | Analog | £3.00 | ⚠️ Community |
| Seeed Grove Vision AI | I2C | £35.00 | ⚠️ Community |

---

## International Markets

| Market | Radio | Plug | Compliance | Status |
|--------|-------|------|------------|--------|
| UK | 868MHz | Type G | UKCA | Launch Christmas 2026 |
| US | 915MHz | Type A/B | FCC | Q1 2027 |
| EU | 868MHz | Type C/F | CE | Q2 2027 |
| Australia | 433MHz | Type I | RCM | Q3 2027 |

**Ship from China (Makerfabs). Global delivery.**

---

## The MCP

### Tools

| Tool | What it answers |
|------|----------------|
| `pow_resolve_bom(model_id)` | "What parts does this robot need?" |
| `pow_find_substitutes(component_id)` | "What else fits this slot?" |
| `pow_optimize_bom(model_id, strategy)` | "Cheapest/fastest way?" |
| `pow_quote_build(model_id)` | "Full assembly cost?" |
| `pow_list_components(query)` | "Show me all servos/sensors" |
| `pow_robot_info(model_id)` | "Tell me about this robot" |
| `pow_list_robots(robot_type)` | "Show me all robot vacuums" |
| `pow_list_products(product_line)` | "Show me all Glimlings" |

### Design MCP

| Tool | What it does |
|------|--------------|
| `validate_design` | Check if design fits constraints |
| `calculate_cost` | Estimate print cost |
| `generate_enclosure` | Create STL within constraints |

---

## Design Principles

1. **Indoor first** — No waterproofing, simpler assembly
2. **Open compatible** — Third-party sensors work with Glimlings
3. **Personalised** — Every product has name, colour, character
4. **Manufacturable** — JLCPCB + JLC3DP + Makerfabs
5. **Software moat** — We validate, not manufacture, sensors
6. **"Glimling Compatible"** — Trust mark for tested products

---

## Blockers

1. Mouser/Farnell/LCSC need API keys for structured pricing
2. eBay needs OAuth setup
3. BARA/RBTX/apprenticeships are JS-rendered
4. Makerfabs quotation needed for exact board + packing
5. HHCC Flower Care wholesale supply unverified
6. UK PSTI compliance requirements need assessment
