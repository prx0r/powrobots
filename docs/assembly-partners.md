# Assembly Partners — Who Actually Builds This

Every step from design to shipped product, with real suppliers, real costs, and real lead times.

---

## The full pipeline (who does what)

```
1. COMPONENTS        → LCSC / Mouser / Farnell / AliExpress
2. PCB ASSEMBLY      → JLCPCB or Seeed Fusion (solder components onto board)
3. FIRMWARE FLASH    → JLCPCB or Seeed (flash firmware onto ESP32)
4. ENCLOSURE         → JLC3DP (3D print the housing)
5. BOX BUILD         → UK Electronics / M-TEK / Prism (put board in enclosure, wire, test)
6. TESTING           → Same as above (functional test included)
7. PACKAGING         → Same as above (branded box, instructions, QR)
8. SHIPPING          → Royal Mail / Evri / DHL
```

---

## Supplier 1: LCSC (China) — electronic components

| Detail | Value |
|--------|-------|
| What | ESP32-C3 $1.91, sensors $1-5, LEDs $0.30 |
| MOQ | 1 piece |
| Shipping | 2-5 days to UK |
| API | Yes (free) |
| Website | lcsc.com |
| **Can order 1?** | **Yes** |

---

## Supplier 2: JLCPCB — PCB assembly

| Detail | Value |
|--------|-------|
| What | Solder components onto PCB, flash firmware |
| MOQ | 2 boards (Economic PCBA) |
| Setup cost | $8.18 |
| Per-unit | $0.48 per SMT joint |
| Build time | 24 hours (Economic), 4+ days (Standard) |
| Components | 720,000+ in stock |
| Firmware flash | Yes (HEX/BIN, $8/hr engineering) |
| Shipping | Worldwide, 2-4 days |
| **Can order 1 assembled board?** | **No — min 2** |
| Website | jlcpcb.com |

**JLCPCB does:** PCB fabrication + component sourcing + SMT assembly + inspection + firmware flash
**JLCPCB does NOT do:** Enclosure, wiring, box build, final testing, packaging

---

## Supplier 3: Seeed Fusion — full kit assembly

| Detail | Value |
|--------|-------|
| What | PCB + components + assembly + firmware + packaging |
| MOQ | 1 kit (for SO-101 type products) |
| Pricing | $189-$299 per assembled kit |
| Build time | 7-15 days (OPL parts), 20-25 days (non-OPL) |
| Services | Firmware flashing, header soldering, board assembly, custom packaging |
| Shipping | Worldwide |
| **Can order 1 assembled kit?** | **Yes** |
| Website | seeedstudio.com/fusion |

**Seeed does:** Everything from components to assembled, tested, packaged product
**Seeed does NOT do:** Custom enclosure design (you provide STL), final product compliance

---

## Supplier 4: JLC3DP — 3D printed enclosures

| Detail | Value |
|--------|-------|
| What | SLA resin, MJF nylon, FDM plastic, SLS nylon, SLM metal |
| MOQ | 1 piece |
| SLA | From $0.30, 2 days, ±0.2mm |
| MJF | From $1.00, 3 days, ±0.3mm |
| FDM | From $1.00, 3 days, ±0.3mm |
| Materials | SLA, MJF, SLS, SLM, FDM, WJP |
| Shipping | Worldwide, 2-4 days |
| **Can order 1 enclosure?** | **Yes** |
| Website | jlc3dp.com |

---

## Supplier 5: UK Electronics (Hampshire) — full box build

| Detail | Value |
|--------|-------|
| What | PCB + enclosure + wiring + test + packaging |
| MOQ | 10+ units |
| Services | SMT, through-hole, cable assembly, box build, test, packaging |
| Experience | 40+ years |
| Quality | IPC Class 2/3, ISO 9001 |
| Location | Hampshire, UK |
| **Can order 1 unit?** | **No — min 10** |
| Website | ukelectronics.co.uk |

**UK Electronics does:** Complete product assembly from PCB to packaged, tested product
**UK Electronics does NOT do:** Design (they build what you design)

---

## Supplier 6: M-TEK Assembly (Reading) — full turnkey

| Detail | Value |
|--------|-------|
| What | PCB + cable + test + programming + box build |
| MOQ | Small batches OK |
| Services | SMT, PTH, flex-rigid, BGA, testing, programming |
| Quality | BS EN ISO 9001:2015, IPC-A-610D Class 3+ |
| Location | Reading, UK |
| **Can order 1 unit?** | **Probably — small batch specialist** |
| Website | mtek.co.uk |

---

## Supplier 7: Prism Electronics (UK) — prototype specialist

| Detail | Value |
|--------|-------|
| What | PCB assembly + test + rework + design |
| MOQ | Prototype runs OK |
| Services | SMT, PTH, box build, test, rework, design |
| Experience | 30+ years |
| Location | UK |
| **Can order 1 unit?** | **Yes — prototype specialist** |
| Website | prism-electronics.com |

---

## Supplier 8: esp32s.com — ESP32 specialist

| Detail | Value |
|--------|-------|
| What | ESP32 custom board manufacturing, firmware flash, testing |
| MOQ | 5+ units |
| Services | PCB design, component sourcing, SMT assembly, firmware flash, functional test |
| Speciality | ESP32-S3/C3/H2 boards |
| Lead time | 5-7 business days |
| **Can order 1 unit?** | **No — min 5** |
| Website | esp32s.com |

---

## The realistic assembly path

### For prototyping (1-5 units)

```
1. Design enclosure in OpenSCAD/Blender
2. Export STL → JLC3DP ($0.30-1.00 per enclosure)
3. Design PCB in KiCad (or use ESP32 dev board)
4. Order assembled PCB from JLCPCB (min 2 boards, $8.18 setup)
5. Order components from LCSC (MOQ 1)
6. Flash firmware via JLCPCB ($8/hr) or manually
7. Assemble: board + enclosure + wiring + test (manual or Seeed)
8. Package: branded box + instructions
9. Ship: Royal Mail £3.50
```

### For small batch (10-50 units)

```
1. Same as above but:
2. JLCPCB: 50 boards assembled ($8.18 + $0.48/joint)
3. JLC3DP: 50 enclosures ($1-5 each)
4. UK Electronics or M-TEK: full box build (quote needed)
5. Automated test (bed-of-nails fixture)
6. Packaging: branded boxes, QR codes, manuals
```

### For production (50+ units)

```
1. Seeed Fusion ODM: full turnkey
   - PCB + components + assembly + firmware + packaging
   - $189-$299 per assembled kit
   - 7-15 days with OPL parts
2. Or: UK Electronics for UK-specific requirements
```

---

## Assembly constraints per product

| Product | JLCPCB | JLC3DP | Box Build | Firmware | Total lead |
|---------|--------|--------|-----------|----------|-----------|
| Plant Sprite | 2 boards, $8 | 5 enclosures, $1.50 | Manual or UK Elec | Flash needed | 6-11 days |
| Desk Goblin | 2 boards, $8 | 5 enclosures, $1.50 | Manual or UK Elec | Flash needed | 6-11 days |
| Garden Familiar | 2 boards, $8 | 5 enclosures, $1.50 | Manual or UK Elec | Flash needed | 6-11 days |
| SO-101 Kit | N/A (Seeed) | N/A | Seeed assembles | Pre-flashed | 7-15 days |
| Friendship Spirits | 4 boards, $8 | 10 enclosures, $3 | Manual or UK Elec | Flash needed | 6-11 days |

**Key constraint:** JLCPCB minimum is 2 boards. For 1 unit, use Seeed Fusion or manual assembly.

---

## What we need to do

1. **Get Apify account** → automated supplier scraping
2. **Set Mouser/Farnell/LCSC keys** → structured component pricing
3. **Contact UK Electronics** → get quote for box build
4. **Order first prototype** → 5x Garden Familiar from JLCPCB + JLC3DP
5. **Test with real plants** → validate moisture readings
6. **List on Etsy** → first sales with hand-assembled units
7. **Scale with Seeed ODM** → when demand is proven
