# Glimlings: From Custom Design to a Finished, Shipped Product

## The Manufacturing Model

One standard electronic core, custom-made character shells, and one assembly partner in Shenzhen that combines everything into a finished gift.

Customers design a unique mushroom, ghost, robot or desk creature without POW having to manufacture different electronics for each design. Customisation happens in POW Studio; production partners handle the physical object.

### The Supply Chain

```
POW Studio
  ↓
Customer chooses character, shape, colour, material, personality
  ↓
M5Stack
  Standard voice electronics
  ↓
JLC3DP
  Personalised printed shells
  ↓
Assembly partner
  Receives parts, flashes firmware, assembles, tests, packages, ships
```

### Verified Candidates

| Supplier | Service | Status |
|----------|---------|--------|
| Makerfabs | Electronics assembly, 3D-printing coordination, packaging, fulfilment | Advertised, not yet quoted |
| Elecrow | Parts sourcing, 3D printing, kitting, worldwide dropshipping | Advertised, not yet quoted |

**Neither has yet provided a Glimlings-specific assembly quotation.**

---

## 1. The Supplier Arrangement

| Supplier | Responsibility | Decision |
|----------|----------------|----------|
| M5Stack | Supply Atom Voice cores; bulk pricing, factory firmware | Keep stock electronics initially |
| JLC3DP | Custom shells, translucent caps, full-colour characters | Specialist print supplier |
| Makerfabs | Receive components, final assembly, testing, packaging, ship | First approach for complete product |
| Elecrow | Alternative all-in manufacturing and fulfilment | Obtain competing quote |
| PCBWay | Independent printing and finishing | Backup when JLC3DP can't provide required appearance |

**Potential improvement:** Ask Makerfabs and Elecrow to quote complete manufacturing route before committing to JLC3DP for every order.

---

## 2. Material Tiers

| Customer Finish | Production Method | Position |
|-----------------|-------------------|----------|
| Standard matte | SLS or MJF nylon | Everyday character |
| Smooth premium | SLA resin | Detailed collector |
| Full-colour artist | WJP full-colour resin | Complex patterns |
| Glowing translucent | Transparent/translucent resin | Illuminated characters |
| Metallic | Painted/coated shell | Later, after samples |

### JLC3DP Materials

- MJF nylon
- Transparent/translucent SLA resin
- WJP full-colour resin (from $5/part)
- Metallic effects: **unavailable** in that material

---

## 3. The Construction Trick

Make the character from three components:

### Fixed Inner Chassis
- Tough, inexpensive nylon or moulded plastic
- Holds electronics
- Provides consistent mounting interface

### Custom Outer Body
- Smooth resin, matte nylon, or full-colour material
- What customers personalise

### Optional Light Diffuser
- Translucent cap, eyes, belly or decorative feature
- Positioned relative to electronics' LED

**This is more practical than manufacturing entire complex enclosure in every premium material.**

For metallic: start with metallic-looking paint or finish on plastic shell. Actual conductive metal enclosure can obstruct Wi-Fi and Bluetooth.

---

## 4. What Happens After a Customer Orders

1. **POW Studio finalises design** — Customer selects character, material, colours, expression, name. System produces preview and manufacturing file.

2. **Design is validated** — Check wall thickness, dimensions, mounting geometry, button travel, USB access, microphone/speaker openings, LED visibility, material restrictions.

3. **Supplier prints shell** — Standard finish from assembly partner; special full-colour/translucent from JLC3DP. Every order gets unique design and manufacturing revision.

4. **Assembler installs electronics** — Cores in stock at facility. Workers mount using repeatable fixture, flash/verify firmware, test button/mic/speaker/LED, record serial number.

5. **Character gets packaged and dispatched** — QR pairing card, charging cable, personalised adoption card, instructions, accessories. Fulfilment partner sends serial number, tracking number, final inspection result.

**Personalised shell produced to order. Electronic core, chassis, packaging and accessories stocked at assembler.**

---

## 5. Margin Correction

### Illustrative £59.99 Premium Glimling

| Cost | Allowance |
|------|-----------|
| Electronic core delivered to assembler | £12 |
| Premium shell and diffuser | £8 |
| Internal parts and supplier consolidation | £1 |
| Assembly and functional testing | £4 |
| Gift packaging | £2 |
| International customer delivery | £6 |
| Returns and warranty allowance | £2 |
| Etsy transaction, UK processing, regulatory fees | ~£7 |
| **Total** | **£42** |

**Etsy fees:** 6.5% transaction + 4% + £0.20 UK processing + 0.48% regulatory.

If VAT-registered and £59.99 includes 20% VAT:
- Revenue excluding VAT: ~£50
- Contribution: ~£8
- **Not the 70% margins originally proposed**

---

## 6. Delivery Promise Revision

JLC3DP production: ~72 hours for several materials. After printing, shell must reach assembler, be inspected, installed, then shipped internationally.

**Display calculated production and delivery range for each material and destination.** Standard characters stocked at assembly facility can have faster delivery.

**For Christmas:** Ship real, personalised sample to UK address before publishing final ordering deadline.

---

## 7. What POW Studio Passes to Manufacturing

Every paid order generates one immutable manufacturing record:

- Core SKU and hardware revision
- Design-file hash
- Customer-selected material and finish
- Colour specification
- Shell and diffuser revisions
- Assembly instructions
- Validated geometry result
- Factory test requirements
- Packaging personalisation
- Approved manufacturing price

**Order states:** design approved → quote accepted → printing → print inspection → ready for assembly → device tested → packed → shipped

---

## 8. Two Constraints to Resolve

### Etsy Compliance
- Custom Glimlings with original designs + disclosed manufacturing partners fit Etsy's rules
- Generic dropshipped sensors do not
- **Cambodia not on Etsy Payments eligibility list** — verify seller setup

### Product Compliance
- Compliant M5Stack module ≠ compliant finished device
- UK: radio-equipment requirements, PSTI connected-product security
- Must resolve before selling

---

## The Immediate Manufacturing Decision

**Quote two complete routes using same approved Glimling design:**

1. **M5Stack + JLC3DP + Makerfabs**
2. **Elecrow-managed complete product**

**Request prices for:**
- Individual personalised orders
- Batches of 10, 50, 100
- Including printing, firmware, assembly, packaging, delivered shipping to UK, US, EU

**Whichever reliably delivers finished character at sustainable all-in price becomes the fulfilment partner. Preserve others as alternatives in POW's procurement graph.**
