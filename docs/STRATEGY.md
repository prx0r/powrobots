# STRATEGY.md — How to Build the Best Graph in the Business

The goal: become the definitive procurement intelligence layer for physical robotics.

---

## The thesis

**POW wins by knowing which specific part fits which specific robot revision, sourced from where, at what cost, with what evidence that it actually works — and making that intelligence available to humans and AI agents before competitors can accumulate the same evidence.**

## The flywheel (from goldmoat.md)

```
PROCUREMENT GRAPH (what we build)
  robot → revision → BOM → parts → suppliers → UK cost
        ↓
PRODUCTS (spare parts, kits, consumer agents)
  sold to repairers, builders, hobbyists
        ↓
OUTCOME DATA (the moat)
  what actually failed, what worked, what shipped on time
        ↓
FEEDS BACK INTO GRAPH
  more accurate, more reliable, more useful
```

## What "best graph" means

The best graph isn't the biggest. It's the most **actionable**:

| Metric | What it means | How we measure |
|--------|--------------|----------------|
| **Coverage** | How many robots we know about | robot_model count |
| **Depth** | How many parts per robot | product_relation count per model |
| **Pricing** | How many suppliers per component | component_market_observation count |
| **Compatibility** | Cross-model substitution evidence | COMPATIBLE_WITH relations |
| **Verification** | Evidence level (declared vs tested) | confidence field |
| **Freshness** | How current the pricing data is | observed_at timestamps |
| **UK specificity** | UK-delivered pricing and stock | distributor country_code = GB |

## Current state vs target

| Metric | Current | Target (3 months) | Target (12 months) |
|--------|---------|-------------------|---------------------|
| Robot models | 145 | 200 | 500 |
| Components | 118 | 300 | 1000 |
| Relations | 169 | 500 | 2000 |
| Price observations | 90 | 500 | 5000 |
| Suppliers tracked | 15 | 25 | 50 |
| Verified compatibility | 0 | 20 | 200 |
| Consumer products | 7 | 10 | 20 |

## How to get there

### Phase 1: Data collection automation (weeks 1-2)

1. **Set up Apify** — free tier, scrape AliExpress/Amazon/eBay daily
2. **Set up API keys** — Mouser, Farnell, LCSC for structured pricing
3. **GitHub Actions** — automated daily scraping schedule
4. **First scrapers working** — STS3215, Roborock parts, ESP32 components

### Phase 2: Graph density (weeks 3-6)

5. **More COMPATIBLE_WITH relations** — every part that fits multiple robots
6. **More robots registered** — Husqvarna models, Dreame models, more UR variants
7. **More components** — from teardown guides, BOMs, manufacturer docs
8. **Cross-supplier price comparison** — same part, 3+ suppliers

### Phase 3: Verification (weeks 6-10)

9. **First transactions** — buy parts, record outcomes
10. **Verified substitutions** — "tested" not just "declared"
11. **Supplier reliability scores** — delivery time, defect rate
12. **Customer feedback loop** — what worked, what failed

### Phase 4: Products (weeks 10-16)

13. **SO-101 build kit** — first complete robot kit
14. **Spare parts kits** — Roborock S7 LiDAR, Automower blades
15. **POW Agent Node kits** — plant/desk/pet agents
16. **Etsy listings** — first consumer sales

## The data moat

What we accumulate that competitors can't easily replicate:

| Asset | Why it's defensible |
|-------|-------------------|
| Verified compatibility | Requires actual testing, not scraping |
| Supplier reliability | Requires transaction history |
| UK landed costs | Requires real import data |
| Repair outcomes | Requires technician relationships |
| Cross-model substitutions | Requires engineering knowledge |
| Component cost trends | Requires time-series data |

## What to do this week

1. Get Apify account and token
2. Set up first AliExpress scraper for STS3215
3. Run it, verify data quality
4. Add to GitHub Actions schedule
5. Repeat for Amazon UK and eBay UK
