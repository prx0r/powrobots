# Cross-Repo Compatibility Review

**Date:** 21 September 2026

## Three-Repo Architecture

```text
repair          → what breaks, why, intervention, outcome
powproducts     → generic physical product primitives (horizontal)
powrobots       → UK robotics economy (vertical)
```

## Shared Infrastructure (all three repos)

| Table | repair | powproducts | powrobots | Notes |
|-------|--------|-------------|-----------|-------|
| raw_blob | ✅ | ✅ | ✅ | Identical schema |
| raw_acquisition | ✅ | ✅ | ✅ | Identical schema |
| source_record | ✅ | ✅ | ✅ | Identical schema |
| source_cursor | ✅ | ✅ | ✅ | Identical schema |
| source_health | ✅ | ✅ | ✅ | Identical schema |
| collector_run | ✅ | ✅ | ✅ | Identical schema |
| source_rights | ✅ | ✅ | ✅ | powrobots adds more fields |

**Verdict:** Shared kernel is identical. No conflicts.

## Overlapping Tables (powproducts ↔ powrobots)

| Table | powproducts | powrobots | Resolution |
|-------|-------------|-----------|------------|
| market_listing | ✅ | ✅ | powrobots extends with robot-specific fields |
| market_observation | ✅ | ✅ | Identical schema |
| product_relation | ✅ | ✅ | Identical schema |
| robot_description | ✅ | ✅ | Identical schema |

**Verdict:** Intentional overlap. powrobots inherits from powproducts. Acceptable for Layer 1 — can later use powproducts as a shared library.

## Unique to Each Repo

### repair only
- `fault_record`, `repair_economics`, `resale_listing` — repair domain
- Open Repair collector (305K records)
- Repair-specific schemas

### powproducts only
- `manufacturer`, `product_family`, `product_model`, `product_variant` — generic product hierarchy
- `product_identifier`, `product_spec_observation` — generic product specs
- `benchmark_observation` — Blender, MLPerf
- `jev_decision` — semantic annotations
- `listing_seen` — disappearance detection
- `market_event` — state transitions
- PCI IDs, OSHWA, DYNAMIXEL, MuJoCo, robot_descriptions collectors

### powrobots only
- `organisation`, `robot_manufacturer`, `robot_family`, `robot_model` — robotics entity graph
- `component`, `component_category`, `component_manufacturer` — BOM graph
- `uk_trade_record` — HMRC trade flows
- `procurement_notice` — government contracts
- `grant_project` — UKRI grants
- `apprenticeship_listing`, `job_listing` — skills/labour
- `safety_notice` — OPSS
- `deployment_evidence` — installation evidence
- `company_filing` — Companies House
- `change_event` — state transitions
- HMRC, UKRI, OPSS, BARA, BGS, ONS, RBTX, Contracts Finder, Apprenticeships collectors

## Cross-Repo Links

powrobots → powproducts:
- `robot_model` in powrobots could reference `product_model` in powproducts
- `component` in powrobots could reference `product_variant` in powproducts
- Future: powproducts becomes the horizontal substrate, powrobots adds domain-specific structure

powrobots → repair:
- `deployment_evidence` in powrobots could link to `failure_event` in repair
- Future: powrobots detects adoption, repair detects failures, both reference same product

## Recommendations

1. **No conflicts found.** The three repos are distinct and compatible.
2. **powproducts is the horizontal layer.** powrobots should eventually import product primitives from powproducts rather than duplicating them.
3. **repair is independent.** It owns failure/intervention/outcome. No overlap with powproducts or powrobots.
4. **Shared kernel is stable.** The 6 identical tables (raw_blob through collector_run) are the foundation. Don't change them independently.
