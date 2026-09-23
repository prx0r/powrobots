# Supplier Constraints — What We Can Actually Order

Real constraints, not aspirational specs. Based on current supplier listings and public pricing.

---

## Component suppliers

### LCSC (China) — electronic components
| Constraint | Value |
|-----------|-------|
| MOQ | **1 piece** (most parts) |
| Stock | 760,000+ parts |
| Shipping | Worldwide, $399+ free shipping |
| ESP32-C3 price | $1.91 (1pc), $1.24 (1000pc) |
| ESP32-S3 price | $3.76 (1pc), $2.54 (1000pc) |
| Lead time | 2-5 days (China to UK) |
| API | Yes (free) |
| **Can we order 1?** | **Yes** |

### Mouser (UK/Global) — electronic components
| Constraint | Value |
|-----------|-------|
| MOQ | **1 piece** |
| Stock | Millions of parts |
| Shipping | UK next-day available |
| ESP32-S3 price | €1.59 (1pc) |
| Lead time | 1-3 days UK |
| API | Yes (free, 1000 req/day) |
| **Can we order 1?** | **Yes** |

### Farnell (UK) — electronic components
| Constraint | Value |
|-----------|-------|
| MOQ | **1 piece** |
| Stock | 600,000+ parts |
| Shipping | UK same-day dispatch |
| ESP32-S3 price | £8.90 (dev board) |
| Lead time | Same-day UK |
| API | Yes (free) |
| **Can we order 1?** | **Yes** |

### DigiKey (UK/Global) — electronic components
| Constraint | Value |
|-----------|-------|
| MOQ | **1 piece** |
| Stock | Millions of parts |
| Shipping | UK available |
| Lead time | 1-3 days |
| API | Yes |
| **Can we order 1?** | **Yes** |

### Alibaba (China) — wholesale
| Constraint | Value |
|-----------|-------|
| MOQ | **Varies (1-1000)** |
| Pricing | Lowest ($0.30-5 per unit at volume) |
| Shipping | 2-3 weeks to UK |
| ESP32-S3 price | $0.88-2.87 |
| **Can we order 1?** | **Some sellers yes, most MOQ 5-10** |

### AliExpress (China) — consumer
| Constraint | Value |
|-----------|-------|
| MOQ | **1 piece** |
| Pricing | Low (retail Chinese prices) |
| Shipping | 2-3 weeks |
| ESP32-S3 price | $2-5 |
| **Can we order 1?** | **Yes** |

---

## Manufacturing services

### JLCPCB — PCB assembly
| Constraint | Value |
|-----------|-------|
| MOQ | **2 boards** (Economic PCBA) |
| Setup cost | $8.18 (Economic) |
| Build time | 24 hours |
| Components | 720,000+ in stock |
| Shipping | Worldwide, 2-4 days |
| **Can we order 1 assembled board?** | **No — minimum 2** |

### JLC3DP — 3D printing
| Constraint | Value |
|-----------|-------|
| MOQ | **1 piece** |
| SLA (resin) | From $0.30, 2 days |
| MJF (nylon) | From $1.00, 3 days |
| FDM (plastic) | From $1.00, 3 days |
| Tolerance | ±0.2mm (SLA), ±0.3mm (MJF/FDM) |
| Materials | SLA, MJF, SLS, SLM, FDM, WJP |
| **Can we order 1 enclosure?** | **Yes** |

### Seeed Studio — kit assembly
| Constraint | Value |
|-----------|-------|
| MOQ | **1 kit** (for SO-101) |
| Pricing | $189-$299 (assembled kits) |
| Shipping | Worldwide |
| **Can we order 1 assembled kit?** | **Yes** |

---

## What this means for each product

### Garden Familiar (first product)

| Component | Supplier | MOQ | Price | Can order 1? |
|-----------|----------|-----|-------|-------------|
| ESP32-C3 module | LCSC | 1 | $1.91 | Yes |
| Soil moisture sensor | DFRobot | 1 | $5.90 | Yes |
| LED | AliExpress | 1 | $0.30 | Yes |
| Button | AliExpress | 1 | $0.50 | Yes |
| Battery holder | AliExpress | 1 | $0.80 | Yes |
| PCB assembly | JLCPCB | 2 | $8.18 | No — min 2 |
| Enclosure | JLC3DP | 1 | $0.30-1.00 | Yes |
| **First unit cost** | | | **~$20** | |
| **First 10 units** | | | **~$18/unit** | |

**Realistic first order:**
- 5x ESP32-C3 from LCSC: $9.55
- 5x Soil sensor from DFRobot: $29.50
- 5x LED + button + battery holder from AliExpress: $8.00
- 10x PCB assembly from JLCPCB: $8.18 setup + $4.80 SMT = $12.98
- 5x Enclosure from JLC3DP: $5.00
- **Total first batch: ~$64 for 5 units = $12.80/unit**

### SO-101 Build Kit

| Component | Supplier | MOQ | Price | Can order 1? |
|-----------|----------|-----|-------|-------------|
| STS3215 C001 (6x) | Alibaba | 2 | $13.89 each | Yes (MOQ 2) |
| STS3215 C044 (2x) | Alibaba | 2 | $13.89 each | Yes (MOQ 2) |
| STS3215 C046 (3x) | Alibaba | 2 | $13.89 each | Yes (MOQ 2) |
| Control board (2x) | Amazon | 1 | $10.60 each | Yes |
| USB cable (2x) | Amazon | 1 | $3.50 each | Yes |
| Power supply (2x) | Amazon | 1 | $5.00 each | Yes |
| **Total** | | | **$122** | |

**Constraint: 12 servos minimum from Alibaba (MOQ 2 per type, need 3 types)**

---

## The realistic first order

### Batch 1: 5x Garden Familiar prototypes
```
LCSC:        5x ESP32-C3          $9.55
AliExpress:  5x Soil sensor       $29.50
AliExpress:  5x LED + button      $8.00
JLCPCB:      10x PCB assembly     $12.98
JLC3DP:      5x Enclosure         $5.00
                         Total:   ~$65
                         Per unit: $13
```

### Batch 2: 2x SO-101 kits
```
Alibaba:     12x STS3215 servos   $166.68 (3 types x $13.89)
Amazon:      2x Control boards    $21.20
Amazon:      2x USB cables        $7.00
Amazon:      2x Power supplies    $10.00
                         Total:   ~$205
                         Per kit: $102
```

### Batch 3: 10x Desk Goblin
```
LCSC:        10x ESP32-C3         $19.10
AliExpress:  10x OLED + encoder   $45.00
AliExpress:  10x LED + buzzer     $5.00
JLCPCB:      10x PCB assembly     $12.98
JLC3DP:      10x Enclosure        $10.00
                         Total:   ~$97
                         Per unit: $9.70
```

---

## Summary: what's realistic

| Question | Answer |
|----------|--------|
| Can we order 1 of anything? | Yes — LCSC, AliExpress, JLC3DP all allow 1pc |
| Can we get PCB assembly for 1? | No — JLCPCB min is 2 boards |
| Can we get 3D printed enclosures for 1? | Yes — JLC3DP from $0.30 |
| Cheapest ESP32 for prototyping? | ESP32-C3 SuperMini $0.38 from AliExpress |
| Cheapest production ESP32? | ESP32-C3-WROOM-02 $1.91 from LCSC |
| First batch cost? | ~$65 for 5 Garden Familiar prototypes |
| Per-unit at scale (100)? | ~$8-12 depending on product |
| **First product realistic?** | **Yes — orderable today, deliverable in 2-3 weeks** |
