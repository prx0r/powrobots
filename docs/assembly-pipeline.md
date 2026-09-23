# Assembly Pipeline — From Components to Shipped Product

Zero manual assembly. Every step handled by suppliers.

---

## The full pipeline

```
1. DESIGN
   Blender/OpenSCAD → enclosure STL + PCB Gerber + BOM

2. COMPONENTS
   LCSC/Mouser/Farnell → ordered, shipped to assembler

3. PCB ASSEMBLY
   JLCPCB or Seeed Fusion → PCB + SMT components soldered

4. ENCLOSURE
   JLC3DP → 3D printed, coloured, finished

5. FINAL ASSEMBLY
   UK Electronics or Seeed → PCB into enclosure, wiring, firmware, test

6. PACKAGING
   Same assembler → branded box, instructions, QR code

7. FULFILMENT
   Ship to customer or Etsy warehouse
```

---

## Supplier options per step

### Step 1: Design (we do this)

| Tool | Cost | What |
|------|------|------|
| OpenSCAD | Free | Parametric enclosure design |
| Blender | Free | Complex organic shapes |
| KiCad | Free | PCB design |
| Our graph | Free | Component selection + pricing |

### Step 2: Components

| Supplier | MOQ | Price range | Delivery |
|----------|-----|-------------|----------|
| **LCSC** | 1 | $0.30-5 | 2-5 days |
| **Mouser** | 1 | $1-10 | UK 1-3 days |
| **Farnell** | 1 | £1-8 | UK same-day |
| **DigiKey** | 1 | $1-10 | UK 1-3 days |
| **AliExpress** | 1 | $0.30-5 | 2-3 weeks |

**Can order 1 of anything.** Cheapest for prototyping: AliExpress. Cheapest for production: LCSC.

### Step 3: PCB Assembly

| Provider | MOQ | Setup cost | Build time | Ships to |
|----------|-----|-----------|-----------|----------|
| **JLCPCB** | 2 boards | $8.18 | 24 hours | Worldwide |
| **Seeed Fusion** | 1 board | Free (5pc promo) | 7 days | Worldwide |
| **UK Electronics** | 10+ | Quote | Quote | UK |
| **Esprit Electronics** | 10+ | Quote | Quote | UK |

**For prototyping:** JLCPCB (2 boards, $8.18)
**For production:** UK Electronics or Esprit (full box build)

### Step 4: Enclosure

| Provider | MOQ | Price | Material | Delivery |
|----------|-----|-------|----------|----------|
| **JLC3DP SLA** | 1 | $0.30 | Resin, smooth | 2 days |
| **JLC3DP MJF** | 1 | $1.00 | Nylon, strong | 3 days |
| **JLC3DP FDM** | 1 | $1.00 | PLA/ASA | 3 days |
| **JLC3DP SLM** | 1 | $8.00 | Metal | 3 days |

**For prototyping:** SLA ($0.30, smooth finish)
**For outdoor:** ASA via FDM (UV resistant)
**For production:** MJF nylon (strong, fast)

### Step 5: Final Assembly

| Provider | What they do | MOQ | Location |
|----------|-------------|-----|----------|
| **Seeed Fusion** | Full kit assembly, firmware, packaging | 1 | Shenzhen |
| **UK Electronics** | PCB + enclosure + wiring + test + package | 10+ | UK |
| **Esprit Electronics** | SMT + cable + product assembly | 10+ | Hampshire |
| **EPS Woking** | PCB + cable + wiring + test | 10+ | Surrey |
| **Arista Electronic** | Design + PCB + box build | 10+ | High Wycombe |
| **EC Electronics** | Box build, test, logistics | 10+ | UK/NL/Romania |

**For prototyping (1-10 units):** Seeed Fusion or DIY
**For production (10-100 units):** UK Electronics or Esprit
**For scale (100+ units):** EC Electronics or Seeed ODM

### Step 6: Packaging

| Provider | What they do | Cost |
|----------|-------------|------|
| **Seeed Fusion** | Custom packaging, branding, firmware flash | Included in ODM |
| **UK Electronics** | Box build + packaging | Included in quote |
| **Manual** | Bubble wrap + branded box | ~£2/unit |

### Step 7: Fulfilment

| Method | Cost | Speed |
|--------|------|-------|
| **Royal Mail** | £3.50 | 2-3 days |
| **Evri** | £2.99 | 3-5 days |
| **DHL** | £8.00 | 1-2 days |
| **Etsy shipping** | Built-in | Variable |

---

## The realistic first order

### Batch 1: 5x Garden Familiar (prototypes)

| Step | Provider | What | Cost |
|------|----------|------|------|
| Components | LCSC | 5x ESP32-C3 | $9.55 |
| Components | AliExpress | 5x soil sensor + LED + button | $37.50 |
| PCB | JLCPCB | 10x assembled PCBs | $12.98 |
| Enclosure | JLC3DP | 5x SLA resin | $1.50 |
| **Total** | | | **~$62** |
| **Per unit** | | | **~$12** |

### Batch 2: 50x Garden Familiar (production run)

| Step | Provider | What | Cost |
|------|----------|------|------|
| Components | LCSC | 50x ESP32-C3 | $95.50 |
| Components | DigiKey | 50x soil sensor + LED | $375.00 |
| PCB | JLCPCB | 50x assembled PCBs | $45.00 |
| Enclosure | JLC3DP | 50x MJF nylon | $50.00 |
| Assembly | UK Electronics | 50x box build + test | Quote (~£500) |
| Packaging | UK Electronics | 50x branded boxes | Quote (~£100) |
| **Total** | | | **~£750** |
| **Per unit** | | | **~£15** |

### Batch 3: 200x Garden Familiar (scale)

| Step | Provider | What | Cost |
|------|----------|------|------|
| Components | LCSC | 200x ESP32-C3 | $382.00 |
| PCB | JLCPCB | 200x assembled | $150.00 |
| Enclosure | JLC3DP | 200x MJF | $200.00 |
| Assembly | UK Electronics | 200x full build | Quote (~£1,500) |
| **Total** | | | **~£2,000** |
| **Per unit** | | | **~£10** |

---

## Who does what at each scale

| Scale | PCB | Enclosure | Assembly | Testing | Packaging |
|-------|-----|-----------|----------|---------|-----------|
| **1-5 units** | JLCPCB | JLC3DP | Seeed or DIY | Manual | Manual |
| **5-50 units** | JLCPCB | JLC3DP | UK Electronics | Automated | UK Electronics |
| **50-200 units** | JLCPCB | JLC3DP | UK Electronics | Automated | UK Electronics |
| **200+ units** | Seeed Fusion | JLC3DP | Seeed ODM | Automated | Seeed ODM |

**The path: JLCPCB → UK Electronics → Seeed ODM**

---

## What the graph provides at each step

| Step | Graph contribution |
|------|-------------------|
| Design | Component selection, pricing, compatibility |
| Components | Supplier routing (cheapest/fastest), stock check |
| PCB | Assembly quotes, component matching |
| Enclosure | Material selection, printing parameters |
| Assembly | Assembly instructions, test procedures |
| Packaging | Personalisation data, QR codes |
| Fulfilment | Shipping cost calculation |
