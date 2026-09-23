# Pipeline Graph — Lead Times, Costs, Assembly Flow

Every product flows through this pipeline. Each step has a cost and a lead time.

---

## The pipeline graph

```
┌─────────────────────────────────────────────────────────────────┐
│                     DESIGN PHASE                                │
│  Customer → Muse → Blender MCP → 3D model + BOM               │
│  Lead time: minutes                                             │
│  Cost: $0 (AI does the work)                                    │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PARTS RESOLUTION                              │
│  POW MCP → resolve_bom() → parts + suppliers + prices          │
│  Lead time: seconds                                             │
│  Cost: $0 (graph query)                                         │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    COMPONENTS ORDER                              │
│  LCSC (China) → 2-5 days    $1-5 per component                 │
│  Mouser/Farnell (UK) → 1-3 days  £3-10 per component           │
│  AliExpress (China) → 2-3 weeks  $0.30-5 per component         │
│  DigiKey (UK) → 1-3 days  £3-10 per component                  │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PCB ASSEMBLY                                  │
│  JLCPCB → 24 hours  $8.18 setup + $0.48/joint                  │
│  Seeed Fusion → 7 days  $9.90 for 10 pieces                    │
│  UK Electronics → quote  Full box build                         │
│  Min order: 2 boards (JLCPCB) or 1 (Seeed)                     │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ENCLOSURE                                     │
│  JLC3DP SLA → 2 days  From $0.30                               │
│  JLC3DP MJF → 3 days  From $1.00                               │
│  JLC3DP FDM → 3 days  From $1.00                               │
│  Material: ASA (outdoor), SLA resin (indoor), MJF nylon         │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FINAL ASSEMBLY                                │
│  Seeed Fusion → full kit, firmware, packaging                   │
│  UK Electronics → PCB + enclosure + wiring + test               │
│  Esprit Electronics → SMT + cable + product                     │
│  Lead time: 3-7 days (depending on provider)                    │
│  Cost: £5-50 per unit (depending on complexity)                 │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PACKAGING                                     │
│  Same assembler → branded box + instructions + QR code           │
│  Lead time: included in assembly                                 │
│  Cost: £2-5 per unit                                            │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FULFILMENT                                    │
│  Royal Mail → £3.50  2-3 days                                   │
│  Evri → £2.99  3-5 days                                        │
│  DHL → £8.00  1-2 days                                          │
│  Etsy shipping → built-in                                        │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CUSTOMER                                      │
│  Receives product → connects to Muse/ChatGPT → outcome recorded │
└─────────────────────────────────────────────────────────────────┘
```

## Lead time summary

| Step | Best case | Typical | Worst case |
|------|-----------|---------|-----------|
| Design | 5 min | 30 min | 2 hours |
| BOM resolution | 1 sec | 5 sec | 30 sec |
| Components (UK) | 1 day | 2 days | 5 days |
| Components (China) | 5 days | 14 days | 21 days |
| PCB assembly | 1 day | 2 days | 5 days |
| Enclosure | 2 days | 3 days | 5 days |
| Final assembly | 1 day | 3 days | 7 days |
| Packaging | 0.5 day | 1 day | 2 days |
| Shipping (UK) | 1 day | 2 days | 5 days |
| **Total (UK parts)** | **6 days** | **11 days** | **21 days** |
| **Total (China parts)** | **11 days** | **22 days** | **37 days** |

## Cost breakdown per product

| Product | Parts | Assembly | Packaging | Shipping | **Total COGS** | **Etsy price** | **Margin** |
|---------|-------|----------|-----------|----------|---------------|---------------|-----------|
| Plant Sprite | £13 | £5 | £3 | £3 | **£24** | **£79** | **70%** |
| Desk Goblin | £16 | £5 | £3 | £3 | **£27** | **£49** | **45%** |
| Desk Companion | £11 | £3 | £3 | £3 | **£20** | **£35** | **43%** |
| Garden Familiar | £13 | £5 | £3 | £3 | **£24** | **£39** | **38%** |
| SO-101 Kit | £122 | £0 | £5 | £8 | **£135** | **£189** | **29%** |

## How to improve lead times

| Improvement | Impact | Cost |
|------------|--------|------|
| Hold UK stock of top 10 parts | -5 days for repeat orders | ~£200 initial stock |
| Use Seeed OPL parts only | -7 days on PCB assembly | Free (OPL is free) |
| Pre-flash firmware | -1 day on assembly | Firmware engineering |
| Use MJF nylon enclosures | Same-day after design | JLC3DP from $1 |
| Partner with UK Electronics | Automated box build | Quote needed |

## How to improve costs

| Improvement | Impact | Effort |
|------------|--------|--------|
| Volume pricing (100+ units) | -30% on components | Bulk orders |
| Use OPL parts only | -50% on PCB assembly | Design constraint |
| 3D print enclosures in-house | -80% on enclosures | Printer investment |
| Standardise on 3 engines | -20% on engineering | Design constraint |
| Direct from Feetech | -20% on servos | Account setup |

## Additional suppliers to consider

| Supplier | What they offer | Why add them |
|----------|----------------|-------------|
| **TME** | European components, fast UK delivery | Better than AliExpress for UK |
| **DigiKey** | Global components, same-day UK | Fastest UK delivery |
| **RS Components** | Industrial components, UK stock | UK specialist |
| **JLCPCB Components** | Their own component library | Integrated with PCB assembly |
| **Seeed OPL** | 150,000+ locally stocked parts | Free, fast assembly |
| **PartaBot** | SO-101 kits, robot parts | Specialised robotics |
| **WowRobo** | SO-101 kits | Alternative to Seeed |
| **Feetech** | Direct servo manufacturer | Best servo pricing |
| **DFRobot** | Sensors, probes, modules | Specialist sensors |
| **M5Stack** | ESP32 modules, displays | Pre-built modules |
