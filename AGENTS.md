# AGENTS.md — POWRobots

## Core Thesis

Track the physical cost and availability of building, importing, operating and repairing robots — beginning in China and ending in the UK.

## The Seven Gardens

1. **Robot Catalogue / BOM Graph** — ROS, OEM specs, manuals, compatibility
2. **China Factory** — NBS production, MIR/GGII, corporate filings, China prices, LCSC/RBTX
3. **Global Flow** — UN Comtrade and HS-code graph
4. **UK Landing** — HMRC trade/traders + UK distributor prices/inventory
5. **UK Adoption** — tenders, grants, integrators, deployments, Companies House
6. **UK Aftermarket** — used robots, parts, repairs, technician demand, apprenticeships
7. **Equity Graph** — China + UK + Japan/Germany suppliers mapped to each layer

## How to Run

```bash
# Tests
POWROBOTS_DB=/tmp/test.db python3 -m pytest tests/ -v

# Initialize DB
python3 -m powrobots.shared.db

# Status
powrobots status
powrobots sources
powrobots collect hmrc_traders
powrobots validate
```

## Source Priority

### P0 — Open / No Auth
- HMRC UK Trade Info (trader API, completely open)
- UKRI Gateway to Research
- robot-descriptions.py
- ROS/URDF repositories
- RBTX/igus (robot pricing China+UK+EU)
- OPSS safety
- BARA directory
- BGS minerals

### P0 — Needs API Key (free)
- Companies House
- Mouser
- Farnell/element14
- LCSC (China component pricing)
- eBay UK Browse

### P1 — Later
- UN Comtrade
- HMRC bulk trade files
- ONS PPI
- Adzuna jobs
- Apprenticeships
