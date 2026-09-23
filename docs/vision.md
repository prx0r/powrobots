# Vision — POWRobots

The MCP-first product vision.

---

## The product

An MCP that gives AI agents access to parts intelligence.

We don't build the brain. ChatGPT and Muse do that.
We don't build the robot. LeRobot and Seeed do that.
We don't build the storefront. Shopify and eBay do that.

**We build the API that connects them all.**

---

## How it works

```
Customer: "My Roborock S7 stopped navigating"
    ↓
ChatGPT/Muse: identifies Roborock S7, likely LiDAR failure
    ↓
POW MCP: resolve_bom("roborock-s7")
    → LDS01RR LiDAR module
    → £22 from Amazon UK (next day)
    → £25 from eBay UK (2-3 days)
    → £18 from AliExpress (2-3 weeks)
    → compatible with S5/S6/S7/S8/Q5/Q7/G10
    ↓
ChatGPT/Muse: "Your LiDAR needs replacing. Part is £22, available next day from Amazon UK. Shall I find a local technician?"
    ↓
POW records: failure tracked, supplier performance logged, demand pattern noted
```

---

## The flywheel

```
MCP EXPOSES GRAPH
  AI agents query: what part, where, how much
        ↓
TRANSACTIONS HAPPEN
  Parts ordered, repairs completed
        ↓
DATA COMPOUND
  Which parts fail, when, on which robots
  Which suppliers deliver on time
  Which substitutes actually work
  Demand patterns emerge
        ↓
BETTER RECOMMENDATIONS
  More accurate diagnoses
  Cheaper sourcing
  Verified substitutions
        ↓
MORE TRANSACTIONS
  Technicians trust the recommendations
  Customers come back
        ↓
STOCK DECISIONS
  High-demand parts held in UK
  Chinese alternatives sourced
  Margins improve
```

---

## What we track

### Failure intelligence
- Which parts fail on which robots
- Failure rate by model, component, age
- Common fault symptoms and root causes
- Repeat failure patterns

### Supplier intelligence
- Which suppliers deliver on time
- UK landed cost vs China price
- Lead time by supplier and part
- Stock availability by supplier

### Demand intelligence
- Which parts are requested most often
- Which robots are most commonly repaired
- Seasonal patterns
- Geographic demand (UK regions)

### Substitution intelligence
- Which alternatives fit which robots
- Verified vs declared compatibility
- Cost comparison across alternatives
- Which substitutions actually worked in the field

---

## Revenue path

```
Phase 1: MCP service
  AI agents use it, we learn from usage

Phase 2: Spare parts
  High-demand parts held in UK
  Margin on each sale

Phase 3: Technician network
  Connect repair businesses to customers
  Commission on referrals

Phase 4: Chinese alternatives
  Source cheaper replacements for expensive OEM parts
  Verified compatibility from repair outcomes
```

---

## What we build

| Layer | What | Status |
|-------|------|--------|
| **Graph** | 221 robots, 137 components, 234 relations | Done |
| **BOM engine** | resolve_bom, find_substitutes | Done (CLI, needs MCP) |
| **Failure tracking** | common_failure table | Done (schema) |
| **Demand tracking** | lead table | Done (schema) |
| **MCP exposure** | powops.mcp tools | Needs wiring to resolve.py |
| **Supplier routing** | cheapest/fastest optimization | Done (optimize_bom) |
| **Technician network** | UK repair businesses | Not started |
| **Stock decisions** | High-demand parts in UK | Not started |
| **Chinese sourcing** | Alternative supplier discovery | Not started |

---

## What ChatGPT/Muse can't do (our wedge)

| AI can do | We provide |
|-----------|-----------|
| Identify robot from photo | Graph lookup, model specs |
| Diagnose common faults | Failure intelligence data |
| Suggest repair options | Parts + pricing + alternatives |
| **Find local technician** | **UK technician network** |
| **Route to cheapest supplier** | **Multi-supplier pricing** |
| **Track which parts actually work** | **Outcome data from repairs** |
| **Decide what to stock** | **Demand pattern analysis** |

The last four are what we build. The AI does the first three. We do the last four.

---

## The one sentence

**POW is the parts intelligence MCP that tells AI agents which part fits which robot, where to get it, what it costs, and which technician can install it — learning from every repair to make the next one better.**

---

## Competitive landscape (what exists)

| Competitor | Focus | Has MCP | Has UK focus | Has repair intelligence |
|-----------|-------|---------|-------------|----------------------|
| RoboParts AI | Humanoid components | Yes | No | No |
| RoboPartPicker | Open-source projects | Yes | No | No |
| RoboParts.cc | Humanoid compatibility | Yes | No | No |
| Partsgraph.ai | Electronics datasheets | Yes | No | No |
| Source Parts | Component graph | Yes | No | No |
| pcbparts-mcp | PCB components | Yes | No | No |
| NeoGiga | 2M+ MPNs | Yes | No | No |
| **POW** | **Consumer robot repair** | **Building** | **Yes** | **Yes** |

**Nobody focuses on consumer robot repair parts with UK routing and technician dispatch.**

## How POW plugs into the AI agent ecosystem

```
ChatGPT/Muse:  takes photo of broken Roomba
    ↓
POW MCP:       identifies model → finds failed part → prices from 3 suppliers
    ↓
ChatGPT/Muse:  "Here's your repair quote"
    ↓
POW MCP:       routes to nearest technician → tracks outcome
    ↓
POW graph:     failure recorded → next customer gets better recommendation
```

### Three entry points for AI agents

1. **"I want to build a robot"** → resolve_bom() → BOM with pricing and alternatives
2. **"This part is broken"** → find_substitutes() → verified alternatives with UK prices
3. **"What fails most on this robot?"** → failures command → demand patterns and common faults

### The normalisation layer

POW normalises the fragmented robotics parts ecosystem:

```
Before POW:
  Seeed:     their parts, their prices, their ecosystem
  LeRobot:   open-source BOMs, no pricing, no suppliers
  FixPart:   15M parts, no robotics-specific intelligence
  eBay:      random listings, no compatibility data
  Alibaba:   cheapest but no UK delivery, no verification

After POW:
  MCP:       unified query across all suppliers
  Graph:     cross-brand compatibility verified
  Routing:   cheapest/fastest/UK-held options
  Outcomes:  which parts actually work in the field
```
