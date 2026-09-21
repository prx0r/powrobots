# POWRobots — China→UK Strategy

**Date:** 21 September 2026

## Core Thesis

Track the physical cost and availability of building, importing, operating and repairing robots — beginning in China and ending in the UK.

## The Seven Gardens

1. **Robot Catalogue / BOM Graph** — ROS, OEM specs, manuals, compatibility
2. **China Factory** — NBS production, MIR/GGII public releases, corporate filings, China prices, LCSC/RBTX/marketplaces
3. **Global Flow** — UN Comtrade and HS-code graph
4. **UK Landing** — HMRC trade/traders + UK distributor prices/inventory
5. **UK Adoption** — tenders, grants, integrators, deployments, Companies House
6. **UK Aftermarket** — used robots, replacement parts, repairs, technician demand and apprenticeships
7. **Equity Graph** — China + UK + Japan/Germany suppliers mapped to each component/constraint

## The Transmission Mechanism

```text
CHINA
production
component pricing
OEM pricing
suppliers
robot BOMs
domestic substitution
exports
capacity
listed component companies
        ↓
transport / FX / tariffs / distributors
        ↓
UK landed price
UK inventory
UK integrators
UK deployments
UK jobs
UK repairs
UK used market
        ↓
UK listed-company effects
```

## Key Data Sources (Open)

| Source | What | Auth | History |
|--------|------|------|---------|
| HMRC UK Trade Info | Monthly trade + trader files | None | 2016+ |
| China NBS | Monthly robot production | None | Monthly |
| UN Comtrade | Global trade flows | API key (free) | Decades |
| robot-descriptions.py | 190+ robot URDF/MJCF | None | Static |
| RBTX/igus | Robot pricing China+UK+EU | None | Current |
| LCSC | China component pricing CNY | API key | Current |
| Farnell/element14 | UK component pricing GBP | API key | Current |
| Companies House | UK company data | API key (free) | Historical |
| UKRI GtR | Research grants | None | Historical |
| BGS Minerals | Material production | None | Decades |

## Crown-Jewel Dataset: HMRC Traders

HMRC UK Trade Info API is completely open, no auth. For HS 847950 (industrial robots), 497 businesses trading in 2026. Includes ABB Robotics UK, Applied Automation, and individual end-users.

Reconstructs: who imports robots, what months, their postcode, source country, value, mass.

## Chinese Robotics Stocks

| Company | Ticker | POW Node |
|---------|--------|----------|
| Estun Automation | 002747.SZ / 2715.HK | Robots + motion control / servo |
| SIASUN | 300024.SZ | Industrial robots / automation |
| EFORT | 688165.SH | Industrial robots + automation |
| Leader Harmonious Drive | 688017.SH | Harmonic reducers |
| Shuanghuan Driveline | 002472.SZ | Precision/RV reducers |
| DOBOT | 2432.HK | Cobots / embodied robots |
| UBTECH | 9880.HK | Humanoids / embodied robotics |

## Published Indices (Eventually)

- POW Robot Cost Index
- POW Robot Parts Index
- China→UK Robotics Spread
- UK Robotics Adoption Pulse
- Robot Repair Pressure
- Component Constraint Monitor
- Robot/model BOM pages
