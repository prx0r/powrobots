# AGENTS.md — POWRobots

## What This Is

UK-first physical-economy data garden for robotics. Continuously records UK robot adoption, supply chains, component availability, prices, trade flows, integration capacity, repair capacity and skills demand.

## How to Run

```bash
# Tests
POWROBOTS_DB=/tmp/test.db python3 -m pytest tests/ -v

# Initialize DB
python3 -m powrobots.shared.db

# Check status
python3 -m powrobots.shared.db status
```

## What Belongs Here

**powrobots** owns: robots, robot models, BOMs, integrators, installations, failures, repair skills, service coverage, deployment economics, UK trade, UK procurement, UKRI grants, skills/labour, used market, component baskets.

**powproducts** owns: generic physical-product primitives (product, manufacturer, MPN, price, availability).

**powrepair** owns: generic repair/service primitives.

**powstocks** owns: equity prices, L2, RNS, market response.

## File Layout

```
powrobots/
├── shared/           db.py, persist.py
├── core/             enums.py
├── collectors/       base.py + per-source collectors
├── seeds/            manufacturers, robot_models, hs_codes, etc.
├── layer1/           manifests/
├── registry/         sources.yaml
├── parser/           (planned)
tests/
warehouse/
docs/                 northstar.md, review.md
```

## Source Priority

### P0 — Build Now
- Companies House
- UKRI Gateway to Research
- Mouser (needs API key)
- eBay Browse (needs app ID)
- ROS/URDF repositories

### P1 — Next Phase
- HMRC trade statistics
- Contracts Finder / Find a Tender
- BARA directory
- Apprenticeships
- ONS PPI
- BGS minerals
- OPSS safety
