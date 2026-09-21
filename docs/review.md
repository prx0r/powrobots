# Review — POWRobots Northstar

**Date:** 21 September 2026

## Strengths

1. **Causal chain is well-defined.** Robot adoption → component demand → inventory/price → installation → maintenance → labour → supplier consequences. This is measurable, not speculative.

2. **UK-first is correct.** HMRC trade data, Contracts Finder, Companies House, UKRI, BARA — these are free, machine-readable, and temporally deep. Starting elsewhere would be harder.

3. **Repair basket is the sleeper insight.** Robots accumulating faster than local maintenance capability is a second-order bottleneck that most investors miss. The UK's own robotics skills programme validates this thesis.

4. **Source hierarchy is honest.** Tier A-E quality assignments, `collection_allowed` flags, no proxy bypasses. This prevents the "scrape first, ask permission never" pattern.

5. **BOM confidence tiers (A/B/C)** prevent presenting inferred architecture as exact specification. Critical for credibility.

6. **"Never call disappearance a sale"** carried forward from powproducts. Correct.

7. **Backfill is first-class.** Historical HMRC trade, ONS PPI, Companies House, UKRI — these exist and should be ingested immediately.

## Risks

1. **Scope is enormous.** 52 sections covering trade, procurement, grants, companies, integrators, skills, repair, materials, safety, producer prices, geography, equity exposure. This is 3-5 years of work described as one northstar. Needs strict phase gating.

2. **DuckDB + Parquet + R2 is premature infrastructure.** The powproducts kernel (SQLite + raw files) works. Don't add analytical infrastructure until the ingestion pipeline is proven. SQLite is fine for Checkpoint 1.

3. **Async collector interface is over-designed for Checkpoint 1.** The sync BaseCollector from powproducts works. Migrate to async later when volume demands it.

4. **Postgres is explicitly deferred but DuckDB is required.** Pick one: SQLite for now, DuckDB when query complexity demands it.

5. **50+ sources is too many for one push.** P0 has 16 sources. Even that is aggressive. Focus on the 5-6 that prove the causal chain: HMRC trade, Companies House, Contracts Finder, Mouser, eBay, ROS/URDF.

6. **Material graph (Section 24) should be deferred.** The northstar itself says "only after BOM graph is mature." Don't build material collectors in this phase.

7. **Equity exposure mapping (Section 34) is Layer 2.** Defer entirely.

## Recommended Phase Gating

### Phase 1 — Kernel + Seeds (this push)
- Repo structure, shared kernel, schema, seeds
- Source registry
- 3-5 proof-of-concept collectors (Companies House, UKRI, Mouser, eBay, ROS)
- Tests
- Push to GitHub

### Phase 2 — Core Collectors
- HMRC trade, Contracts Finder, Find a Tender
- BARA directory, apprenticeships
- ONS PPI, BGS minerals
- OPSS safety

### Phase 3 — Analysis
- DuckDB layer
- Component baskets
- Quality reports
- CLI

### Phase 4 — Derived Signals
- Robot import pulse
- Component pressure
- Used robot liquidity
- Skills pressure

## Verdict

The northstar is a comprehensive research document, not a sprint plan. The causal chain is sound. The UK-first data access is real. The repair basket insight is genuinely differentiated.

For this push: build the kernel, prove 3-5 collectors work end-to-end, seed the entity graph, ship tests. That's Checkpoint 1.
