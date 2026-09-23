# POWRobots Handover Document

## What We Built

POWRobots is a **platform for personalised physical robotics products**. It has three layers:

1. **Engines** — 5 reusable electronics platforms (SENSE, REMEMBER, ACT, TALK, SEE) + 1 new engine (COMPANION)
2. **Parts graph** — 177 components, 16 suppliers, 129 prices, 280 compatibility relations
3. **MCP** — API that connects AI agents (Muse, ChatGPT) to the parts graph

The platform lets anyone design, build, and sell custom robot companions (called **Glimlings**).

---

## Current State (September 2026)

### Database

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

### Engines

| Engine | Capability | Key Components | Cost |
|--------|-----------|---------------|------|
| **SENSE** | Reads moisture, light, temp, NFC | ESP32, sensors | £13 |
| **REMEMBER** | Keeps time, tracks history | ESP32, RTC, SD | £9 |
| **ACT** | Controls lights, servos, relays | ESP32, servo, LED, relay | £8 |
| **TALK** | Speaks, listens, buttons | ESP32, speaker, mic | £10 |
| **SEE** | Captures images, motion | ESP32-CAM, servos | £1 |
| **COMPANION** | Health monitoring, social connection | ESP32-S3, touchscreen, camera | £62 |

### Products

| Product | Name | Engines | Price | COGS | Margin |
|---------|------|---------|-------|------|--------|
| glimling-garden-frog | Mosswick | SENSE+ACT | £39 | £21 | 46% |
| glimling-garden-mushroom | Sporebert | SENSE+ACT | £39 | £21 | 46% |
| glimling-garden-ghost | Boo Bloom | SENSE+ACT | £35 | £21 | 40% |
| glimling-desk-goblin | Puck | ACT+display | £49 | £24 | 51% |
| glimling-desk-familiar | Mab | ACT+display | £49 | £20 | 59% |
| glimling-sleep-alarm | Mab | ACT+TALK | £79 | £25 | 68% |
| glimling-home-weather | Nimbus | SENSE+display | £39 | £18 | 54% |
| glimling-home-mood | Chroma | SENSE+LED | £39 | £18 | 54% |
| glimling-home-parcel | Postie | SENSE+TALK | £39 | £21 | 46% |
| glimling-outdoor-pet | Pickles | SENSE+ACT+TALK | £59 | £30 | 49% |
| glimling-gift-bookworm | Wormington | REMEMBER | £15 | £17 | -13% |
| **elderly-companion** | Companion | COMPANION | £149.99 | £62 | 59% |

### Collectors

| Collector | Source | Status | Records |
|-----------|--------|--------|---------|
| hmrc_traders | HMRC | ✅ OK | 561 |
| companies_house | Companies House | ✅ OK | 250 |
| opss_safety | OPSS | ✅ OK | 50 |
| contracts_finder | Contracts Finder | ✅ OK | 20 |
| mouser | Mouser | ⚠️ Needs API key | - |
| farnell | Farnell | ⚠️ Needs API key | - |
| lcsc | LCSC | ⚠️ Needs API key | - |
| ebay | eBay | ⚠️ Needs OAuth | - |
| bara | BARA | ⚠️ JS rendered | - |
| rbtx | RBTX | ⚠️ JS rendered | - |

---

## What We Did Today

### 1. Added Cross-Model Part Compatibility

Added 46 COMPATIBLE_WITH relations for:
- **Roller brushes** — iRobot, Dreame, Ecovacs, Roborock
- **Filters** — Standard HEPA, Premium HEPA, Anti-allergen
- **Batteries** — 14.4V, 14.8V, 25V Li-ion packs
- **Side brushes** — 3-arm and 5-arm variants
- **Mop pads** — Standard and premium
- **Water tanks** — 200ml and 300ml
- **Charging docks** — Basic and auto-empty

### 2. Wired Mouser/Farnell/LCSC Fetch()

Implemented actual API calls for:
- **Mouser** — Search by MPN via REST API
- **Farnell** — Search by MPN via element14 API
- **LCSC** — Search by keyword via REST API

All three now query the component table for tracked MPNs and fetch real pricing data.

### 3. Designed Elderly Companion Engine

Created **COMPANION** engine with:
- **Health monitoring** — Connects to wearables via Open Wearables MCP
- **Medication reminders** — NFC-based tracking
- **Social connection** — One-button video calls via Home Assistant MCP
- **Emergency assistance** — Fall detection, emergency contacts

Product: **Elderly Companion** at £149.99 (59% margin)

### 4. Researched MCP Integrations

Found existing MCP servers for:
- **Home Assistant** — 87+ tools, in-process server, webhook support
- **Open Wearables** — 10+ tools for health data (sleep, activity, vitals)
- **Patientary** — 6 tools for clinical data (ICD-10 codes, provider lookup)
- **Butlr** — 6 tools for occupancy sensing (movement patterns)
- **ESPHome** — Direct device control for ESP32

---

## What to Do Next

### Immediate (Next Session)

1. **Deploy Open Wearables** — Self-hosted health data platform
2. **Configure Home Assistant** — Connect smart home devices
3. **Build Custom MCP** — Medication reminders, emergency alerts
4. **Test Integration** — End-to-end flow with real users

### Short-term (Next Week)

5. **Prototype MVP** — ESP32-S3 + touchscreen + speaker
6. **Test with 5 elderly users** — 2-week trial
7. **Iterate based on feedback** — Refine UX, add features
8. **Launch beta** — 100 units

### Medium-term (Next Month)

9. **Scale deployment** — 1000 units per month
10. **Care home partnerships** — 5 care homes
11. **NHS integration** — Clinical data sharing
12. **Insurance partnerships** — Reduced premiums for monitored users

---

## Key Files

### Code

| File | What it does |
|------|-------------|
| `powrobots/cli.py` | CLI entry point (15 collectors, 10 commands) |
| `powrobots/collectors/base.py` | Base collector with retry + raw storage |
| `powrobots/collectors/mouser.py` | Mouser API integration |
| `powrobots/collectors/farnell.py` | Farnell/element14 API integration |
| `powrobots/collectors/lcsc.py` | LCSC API integration |
| `powrobots/resolve.py` | BOM resolution + substitution engine |
| `powrobots/mcp.py` | MCP server for Muse/ChatGPT integration |
| `powrobots/sdk.py` | SDK for programmatic access |
| `powrobots/shared/db.py` | Schema + seeds + source_health computation |
| `powrobots/shared/persist.py` | Storage + entity graph operations |
| `enclosures/generate.py` | Parametric STL enclosure generator |
| `firmware/plant-sprite/main.py` | ESP32 firmware for plant monitoring |
| `firmware/desk-goblin/main.py` | ESP32 firmware for desk companion |

### Documentation

| File | What it covers |
|------|---------------|
| `docs/vision.md` | MCP-first product vision + competitive landscape |
| `docs/engines.md` | 5 engines mapped to 16+ products |
| `docs/elderly-companion-engine.md` | New COMPANION engine spec |
| `docs/mcp-integrations.md` | Home Assistant, Open Wearables, Patientary MCP |
| `docs/brand-identity.md` | Glimlings brand identity |
| `docs/platform.md` | Engines + community + marketplace architecture |
| `docs/design-pipeline.md` | Blender MCP → POW MCP → manufacturing |
| `docs/assembly-partners.md` | 8 real assembly partners with costs |
| `docs/pipeline-graph.md` | Full pipeline graph with lead times |
| `docs/NEXT_STEPS.md` | Priority-ordered actions |

### Database

| Path | What |
|------|------|
| `warehouse/powrobots.db` | SQLite database (all tables) |
| `warehouse/raw/` | Raw collector data |
| `seeds/component_basket.yml` | Component definitions |

---

## How to Extend

### Add a New Engine

1. Define engine name and capability
2. List required components in `powrobots/seeds/component_basket.yml`
3. Add components to database via `scripts/seed_loader.py`
4. Create enclosure template in `enclosures/generate.py`
5. Create firmware in `firmware/<engine-name>/main.py`
6. Register as product in `product` table
7. Add to MCP tools in `powrobots/mcp.py`

### Add a New Product

1. Choose engine combination (e.g. SENSE + ACT)
2. Create enclosure design (Blender/OpenSCAD)
3. Run `resolve_bom()` to verify parts exist
4. Add to `product` table with pricing
5. Add character variants to `product_variant` table
6. Create Etsy listing template
7. Test manufacturing pipeline (JLCPCB → JLC3DP → assembly)

### Add a New Supplier

1. Add to `source_rights` table (status: open/approved)
2. Add to `source_registry` table (authority, cadence, tier)
3. Add collector in `powrobots/collectors/<name>.py`
4. Add to `COLLECTORS` dict in `cli.py`
5. Run `powrobots seed` (idempotent)
6. Run `powrobots collect <source>`
7. powops sees it via collector_db

---

## Testing

### Run Tests

```bash
POWROBOTS_DB=/tmp/test.db python3 -m pytest tests/ -v
```

### Current Test Results

- **powrobots**: 42/42 passing
- **powops**: 69/69 passing

---

## Deployment

### VPS Location

- **Path**: `/home/ubuntu/powrobots/`
- **Database**: `/home/ubuntu/powrobots/warehouse/powrobots.db`
- **Python**: 3.11+
- **Dependencies**: Installed via `pip install -e ".[dev]"`

### GitHub

- **Repo**: `prx0r/powrobots`
- **Latest commit**: `e9a9127`
- **Token**: Available via environment variable

---

## Brand

### Glimlings

**Tagline**: "Little spirits for the things you love."

- **Individual**: A Glimling
- **Plural**: The collectible family
- **Characters**: 10 (Mab, Nimbus, Puck, Boo Bloom, Pickles, etc.)
- **Colours**: 9 (natural, earthy palette)

### Avoid

- **Piskies** — Cornish folklore, trademark risk
- **Whimlings** — Already used by Whimside game

---

## The Vision

```
Old person: "I'm lonely"
    ↓
POW: "I'll make you a Glimling companion"
    ↓
Design in Blender via Muse
    ↓
POW resolves parts + pricing
    ↓
Manufactured and shipped
    ↓
Connected to Home Assistant
    ↓
Muse checks in daily
    ↓
Social isolation reduced
```

**The elderly companion is the highest-impact product.** It solves a real problem (loneliness), has a clear customer (care homes, families), and connects to existing MCP infrastructure (Home Assistant, wearables).

---

## Questions to Answer

1. **How do we deploy Open Wearables on the VPS?**
2. **How do we configure Home Assistant for elderly care?**
3. **How do we build a custom MCP for medication reminders?**
4. **How do we test with real elderly users?**
5. **How do we scale to 1000 units per month?**

---

**Handover complete.** The next agent should start with deploying Open Wearables and configuring Home Assistant.
