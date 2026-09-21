# POWRobots

UK-first physical-economy data garden for robotics.

> POWRobots is a longitudinal data garden for the physical economics of robotics. It continuously records UK robot adoption, supply chains, component availability, prices, trade flows, integration capacity, repair capacity and skills demand. Its objective is to detect physical constraints before their economic consequences are fully reflected elsewhere.

## What This Is

A data garden that continuously acquires, normalizes, identity-resolves and preserves the physical signals needed to reconstruct the UK robotics economy through time.

```text
raw data is not the moat

transformation
× continuous collection
× time

is the moat
```

## Quick Start

```bash
pip install -e ".[dev]"
POWROBOTS_DB=/tmp/test.db python3 -m pytest tests/ -v
python3 -m powrobots.shared.db
```

## pw.systems

- `powrobots.pw.systems` — this repo (UK robotics economy)
- `powproducts.pw.systems` — generic physical product primitives
- `powrepair.pw.systems` — generic repair/service primitives
- `powpowpow.pw.systems` — physical compute economics
- `powstocks.pw.systems` — equity prices, market response
