# Wedge Analysis

Where POW can win and why. Based on competitor research, market gaps, and existing assets.

---

## The competitive landscape

### Tier 1: Manufacturer OEM parts stores

| Competitor | What they sell | Strength | Weakness |
|------------|---------------|----------|----------|
| **KUKA Marketplace** | 25,000+ spare parts, 24h delivery Europe | OEM quality, compatibility guaranteed, 10-year availability | Single brand, enterprise pricing, no cross-brand |
| **ABB Robotics** | Factory-certified parts, exchange units, repair | OEM quality, global service network | Single brand, no pricing transparency |
| **FANUC World** | 150,000+ new & refurbished parts, 50-75% off OEM | Huge inventory, fast quotes, repair services | US-focused, industrial only |
| **iRobot UK** | Consumables (filters, brushes, bags) | Brand trust, direct relationship | Only consumables, no component-level parts, no internal components |
| **Dreame** | Official accessories | Brand direct | Limited to consumables, no internal parts |
| **Stäubli** | Genuine parts, 15-year availability | Quality guarantee | Single brand, industrial |

**Verdict:** OEMs own their ecosystem. They won't cross-sell. They don't tell you which internal component failed — they sell complete assemblies.

### Tier 2: Third-party spare parts platforms

| Competitor | What they sell | Strength | Weakness |
|------------|---------------|----------|----------|
| **FixPart** | 15M+ appliance spare parts, 1-3 day delivery | Huge catalogue, UK stock, fit guarantee | Generic appliances, not robotics-specific |
| **Spares2Repair** | 200K parts in stock, 300K available in 7 days | UK warehouse, next-day delivery, family business | Generic appliances, no robotics |
| **Spares2you** | Karcher, Sebo, Dyson, Numatic parts | Brand-specific, good stock | Generic cleaning equipment, no robotics |
| **Global Robots** | Refurbished industrial robots + parts | UK-based, tested parts, technical support | Industrial only, no consumer robots |
| **Robot Store** | ABB, KUKA, FANUC, Motoman parts | UK delivery, tested parts, emergency dispatch | Industrial only, no consumer robots |
| **Robothub** | New and used robotics/automation parts | Online marketplace, multiple brands | Industrial only |

**Verdict:** Generic appliance parts platforms don't understand robotics. Industrial parts sellers don't serve consumers. Nobody bridges both.

### Tier 3: BOM management platforms

| Competitor | What they do | Strength | Weakness |
|------------|-------------|----------|----------|
| **OpenBOM** | Cloud PDM/PLM, CAD integration, BOM management | Enterprise-grade, SolidWorks/Fusion360 integration | Manufacturing-focused, no procurement, no robotics-specific |
| **Luminovo** | Electronics BOM management, AI-powered MPN matching | Real-time sourcing from 1,000+ distributors | Electronics only, no mechanical parts, no robotics |
| **Siemens Teamcenter** | Enterprise BOM lifecycle management | Massive scale, multi-domain | Enterprise only, £100K+ implementations |

**Verdict:** BOM platforms manage engineering data. They don't identify which part failed in a specific robot, what alternatives exist, or what UK delivery looks like.

### Tier 4: Repair intelligence

| Competitor | What they do | Strength | Weakness |
|------------|-------------|----------|----------|
| **iFixit** | Repair guides, parts, tools, community | 80,000+ guides, trusted brand, parts sales | Generic electronics, not robotics-specific |
| **WAKU Care** | Machine maintenance software, predictive maintenance | Real-time monitoring, lifecycle tracking | Industrial focus, no parts procurement |
| **NASA Prognostics** | Failure datasets | Public data | Research only, not actionable |

**Verdict:** iFixit knows how to fix things but doesn't source parts or track outcomes. WAKU monitors machines but doesn't sell parts. Nobody connects diagnosis → part → purchase → outcome.

### Tier 5: Chinese suppliers

| Competitor | What they do | Strength | Weakness |
|------------|-------------|----------|----------|
| **LCSC** | 400K+ electronic components, API | Cheap, fast, huge selection | Electronics only, no mechanical parts, no UK stock |
| **Alibaba/1688** | Everything | Cheapest prices | Quality unknown, long shipping, no compatibility verification |
| **RBTX/igus** | Low-cost robot kits + components | Affordable robots, direct from manufacturer | Limited selection, not repair-focused |

**Verdict:** China has the cheapest parts but no UK availability, no compatibility verification, no repair knowledge.

---

## Where POW's wedge is

### Wedge 1: Cross-brand, cross-category intelligence

**Nobody else does this.** KUKA knows KUKA parts. iRobot knows iRobot parts. FixPart knows generic appliances. But nobody connects:

```
Dreame L10s Ultra dock pump
  → compatible with these 3 alternative part numbers
  → available from these 5 suppliers (UK + China)
  → verified by these 2 repair technicians
  → costs this much delivered to UK
  → takes this long to arrive
```

**Why it's defensible:** This requires accumulating verified compatibility evidence from actual repairs. A competitor can scrape prices but can't replicate "this substitute actually worked on this revision."

### Wedge 2: Component-level replacement (not assembly replacement)

**The overlooked opportunity.** iRobot sells a complete cleaning head module for £299.99. But the actual failure might be just the motor inside it (£15 from China). Nobody identifies the component-level repair:

```
Cleaning head module £299.99 (iRobot)
  ↓ diagnosis
Motor inside: Johnson Electric 380S-024G (£15 LCSC)
  ↓ verified
Belt: 6mm × 255mm synchronous (£3 AliExpress)
  ↓ tested
Total repair: £18 vs £300 replacement
```

**Why it's defensible:** Requires teardown knowledge, component identification, and functional testing. Can't be scraped from catalogues.

### Wedge 3: UK-held stock for urgent repairs

**The timing gap.** FixPart lists Dreame parts but ships from Netherlands (1-3 days). Chinese suppliers take 2-3 weeks. For a technician with a customer waiting:

```
Current options:
  FixPart NL:  1-3 days,  £30 + shipping
  China:       2-3 weeks, £8
  iRobot OEM:  out of stock, 10-11 weeks

POW opportunity:
  UK stock:    next day,  £20
  verified:    tested on correct revision
  tracked:     outcome recorded
```

**Why it's defensible:** Requires holding inventory, which creates switching costs and recurring relationships.

### Wedge 4: Outcome data that improves recommendations

**The flywheel.** Every other competitor has a static catalogue. POW learns from every transaction:

```
Transaction 1: "Dreame pump替代品 X worked on L10s Ultra rev2"
Transaction 2: "Same pump didn't fit L10s Ultra rev3 — different connector"
Transaction 3: "Roborock LiDAR motor Y has 6-month failure rate of 15%"
→ POW recommends better alternatives over time
→ Competitors can't replicate this without the transaction history
```

**Why it's defensible:** Requires permissioned, longitudinal data from real customers. Cannot be scraped or reverse-engineered.

### Wedge 5: AI-agent procurement interface

**The new channel.** No competitor exposes procurement through MCP/API for AI assistants. When Muse, Claude, or GPT need to source parts:

```
AI: "I need a replacement dock pump for Dreame L10s Ultra"
POW MCP: {
  "part": "20020100005232",
  "compatible": ["alternative_A", "alternative_B"],
  "uk_stock": true,
  "price": 18.50,
  "delivery": "next day",
  "verified": true,
  "outcome_history": "12 successful installations"
}
AI: orders → POW tracks outcome → improves recommendations
```

**Why it's defensible:** First-mover in AI-agent procurement for robotics. Network effects once agents standardize on POW's interface.

---

## What POW should NOT try to be

| Don't compete with | Why |
|-------------------|-----|
| KUKA/ABB on OEM parts | They have the brand, the warranty, the service network |
| Alibaba on price | Can't beat China on cheap commodities |
| iFixit on repair guides | They have the community, the content, the trust |
| Amazon on logistics | They have the warehouses, the delivery network |
| Siemens on enterprise BOM | Wrong market entirely |

---

## The narrow path to winning

1. **Start with one robot family** — Dreame L10s Ultra or Roborock S7
2. **Identify the 20 most common failures** — dock pumps, LiDAR motors, charging contacts, belts
3. **Find 2+ verified alternatives for each** — OEM + tested substitute
4. **Get UK stock for 5 parts** — next-day delivery, small batch
5. **Do 10 transactions** — track outcomes
6. **Let the data compound** — every transaction improves the next recommendation

The wedge isn't "we have a database." The wedge is "we know from experience which parts actually work, which suppliers deliver on time, and which repairs are worth doing."

---

## Mapping to POW repos

| Wedge | Repo | What it owns |
|-------|------|-------------|
| Cross-brand intelligence | powrobots + powproducts | Robot identity + part identity |
| Component-level replacement | powrobots (BOM) + repair (faults) | What's inside each assembly |
| UK-held stock | powphysical | Supplier offers, landed costs |
| Outcome data | repair | What actually worked |
| AI-agent interface | powops MCP | Expose procurement through MCP |

---

## The one sentence

**POW wins by knowing which specific part fits which specific robot revision, sourced from where, at what cost, with what evidence that it actually works — and making that intelligence available to humans and AI agents before competitors can accumulate the same evidence.**
