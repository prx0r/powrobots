# POWRobots — Repair-Outcome Intelligence Vision

The core thesis refined: verified compatibility is the foundation, but the more valuable question is what a robot owner should actually do when something fails. That might mean repairing, substituting a component, claiming warranty coverage, buying a spare in advance or replacing the entire assembly.

POW becomes more defensible if it learns which decision worked, not merely which component fitted.

---

## 1. The data moat: from parts catalogue to repair-outcome intelligence

Several distinct assets accumulate with different levels of defensibility.

| Asset | How POW obtains it | What makes it valuable |
|-------|-------------------|----------------------|
| Revision-aware BOMs | Manufacturer documentation, open designs, teardown work | Identifies the parts actually installed in each revision |
| Compatibility evidence | Bench testing and documented installations | Distinguishes advertised alternatives from working alternatives |
| Supplier performance | Actual quotations, orders and deliveries | Establishes real UK landed costs, lead times and failure rates |
| Repair outcomes | Technician diagnostics, installations and follow-ups | Reveals what fixes problems and what causes repeat failures |
| Economic outcomes | Parts, labour, downtime, returns and replacements | Shows whether a repair was worth doing |
| Customer relationships | Repeated orders, support and useful recommendations | Creates opportunities to observe further outcomes that outsiders cannot automatically access |

The first row is largely reproducible. The next four become harder to reconstruct when they include permissioned, otherwise unpublished evidence. The last row can make the others compound.

However, none is automatically proprietary: technicians may share information elsewhere, suppliers may serve competitors and customers can leave. POW needs to earn continued access by making each subsequent job easier.

The strongest unit to capture is a repair decision episode.

### One repair decision episode

1. **Initial state** — Exact robot model, revision, fault symptoms, diagnostic confidence, warranty status and downtime cost.

2. **Available choices** — Original part, substitute, repair, warranty claim or replacement, each with a dated cost and lead-time estimate.

3. **Decision and action** — What the technician selected, why, what they ordered and what was actually delivered.

4. **Immediate result** — Installation compatibility, extra adapters, labour, successful repair or failure.

5. **Later result** — Whether the fault recurred, the part was returned, the customer was satisfied and the actual total cost.

Crucially, record rejected recommendations and repairs that were never attempted too. Otherwise, POW could end up learning only from successful orders, systematically overstating compatibility and understating costs.

---

## 2. The competitive reality

Remove "nobody has this for robotics" from the business thesis until we can substantiate a narrower claim.

Existing companies already own meaningful parts of the workflow. KUKA operates spare-parts, maintenance and repair services, with manufacturer-specific technical knowledge. Radwell provides replacement parts, verified substitutes and robot refurbishment. 1BOM offers revision management, sourcing, quality assurance and managed BOM delivery.

### The differentiation to test

Cross-manufacturer, exact-revision robotics procurement that connects independently verified substitution, real UK delivery economics and installation outcomes — and makes those findings reusable by repair technicians and AI agents.

Even this is a hypothesis about an underserved market, not established exclusivity. Existing manufacturers and repair businesses have years of experience, customer relationships and internal repair records. Their data is simply not necessarily aggregated into the product POW envisions.

The other serious competitive threat is not another startup building the same graph. It's AI making generic specification matching, supplier discovery and BOM extraction cheap. POW needs to capture information that better reasoning alone doesn't provide: tested substitutions, unexpected faults, supplier reliability, actual installation costs and customer-specific operating constraints.

---

## 3. What earlier POW work adds to the vision

### Warranty and entitlement before procurement

Before telling someone to buy a £200 replacement, determine whether the equipment is under warranty, covered by a maintenance contract or subject to an authorized-repair requirement. A system that saves a customer an unnecessary order has demonstrated value even though POW didn't sell a component.

### Inventory decisions, not just lowest-price sourcing

A part costing £40 from China and taking three weeks to arrive may be economically worse than a £95 UK part available tomorrow. For critical installed equipment, POW should eventually answer whether to stock, order, substitute, share or pre-position spares. That requires actual downtime and demand observations, not merely supplier prices.

### Repair versus replacement

The same graph can eventually compare repair labour, likelihood of recurrence, replacement cost, disposal or resale value and equipment downtime. This is where the existing `repair`, `powproducts`, `powrobots` and `powphysical` work can reinforce one another without merging their codebases.

Together, those extensions make POW a decision system rather than just a purchasing directory.

---

## 4. How the first ten transactions should work

Ten paid orders would be an excellent commercial milestone. They would not, by themselves, validate the data moat.

If ten orders involve ten unrelated robots and customers never report what happened during installation, you have learned something about sourcing and willingness to pay, but very little about repeatable compatibility.

### First pilot: one repairable robot family

| Aspect | Scope |
|--------|-------|
| Customer | UK technicians or operators with recurring repairs |
| Scope | One robot family, its revisions and 20-50 relevant replacement parts |
| Suppliers | Two credible sourcing options for each pilot-critical part, where available |
| Offer | Verified part identification and executable UK-delivered quotation |
| Fulfilment | Manual sourcing initially, without holding speculative inventory |
| Evidence | Order receipt, delivery, technician confirmation and later fault follow-up |

Track the first ten transactions against four questions:
1. Did the customer pay?
2. Did the promised part arrive on time and at the quoted cost?
3. Did it work on the documented robot revision?
4. Did the customer come back, refer someone or grant permission for the outcome to improve POW's dataset?

A technician reporting "the substitute didn't work" can be a valuable observation if the circumstances are documented. Hiding failures to protect apparent compatibility rates would destroy the dataset's value.

---

## 5. The link to Data Gardens, Influence and the other factories

POW could generate two distinct feedback loops from the same work.

### The transaction loop

Learns what works in the physical world.

```
Part recommendation → purchase → installation → repair outcome → improved recommendation
```

### The audience loop

Learns which physical-world problems people want solved.

```
Verified finding → Short → viewer response → new questions → research and product priorities
```

For example, a video about replacing an expensive actuator receives comments from owners asking about a recurring encoder fault. That tells POW where to investigate next. A technician then provides a documented repair, which creates another useful finding and a possible product.

But the two loops must not be confused. High video engagement establishes interest in a topic, not that the proposed repair works. Likewise, a single successful installation establishes compatibility under recorded conditions, not universal compatibility.

The repository boundaries follow those facts:
- `powrobots` owns robot and revision identity
- `powproducts` owns component identity
- `powphysical` owns sourcing and landed costs
- `repair` owns intervention and outcome records
- `powops` monitors the complete pipeline

The commercial extensions follow observed demand. If repairs reveal that a particular sensor or actuator repeatedly needs replacement, POW can assemble a tested repair kit. If customers then repeatedly request a complete build, POW can use the same component and fulfilment knowledge to develop kits or consumer devices.

---

## 6. What would actually demonstrate a moat?

| Stage | What has been demonstrated |
|-------|---------------------------|
| Published graph | POW can organize existing robotics knowledge |
| Independently tested alternatives | POW can generate verified new compatibility information |
| Ten paid orders | Some customers will pay for the sourcing service |
| Repeat orders and documented outcomes | The information is useful repeatedly and improves through transactions |
| Outcomes across multiple revisions and customers | Knowledge is becoming transferable beyond individual repairs |
| Customers contributing outcomes and using recommendations habitually | Relationships, access and accumulated learning are beginning to reinforce one another |

The last two are the beginnings of a defensible business. Whether that advantage becomes substantial still depends on retention, economics, access to customers and whether competitors can obtain equivalent evidence.

### Key measurements

- Proportion of recommendations improved by information from previous POW transactions
- Reduction in incorrect orders, downtime or total repair cost vs customer's previous sourcing process
- These are more meaningful than counting database rows

### Preserve failures

Preserve unsuccessful quotes, rejected recommendations and unresolved faults alongside completed jobs. Without them, POW will lack the denominator needed to distinguish reliable guidance from a collection of success stories.

### The near-term commercial test

Find a tightly defined group of repair customers, make ten paid sourcing transactions, obtain usable outcome evidence and see whether those observations improve the next ten decisions. If they do, POW has demonstrated the mechanism behind the proposed moat. If customers pay but won't contribute outcomes, the sourcing business may still work, but the data strategy will need another way to observe what happens after delivery.

The graph becomes defensible not because POW possesses old information, but because customers repeatedly use its recommendations, generate new evidence and give POW opportunities to improve decisions that competitors weren't present to observe.
