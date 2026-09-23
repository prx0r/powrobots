# The Solution: How to Get 1 Unit Assembled

## The Problem

You want to design a product and get 1 fully assembled, tested, working unit delivered. No manual assembly.

## The Answer

**PCBWay Box Build Assembly** or **Makerfabs** or **PCBark**.

---

## Option 1: PCBWay (Recommended)

### What They Do
- Take your PCB design + enclosure CAD + firmware
- Source components
- Assemble PCB
- Print enclosure
- Wire everything together
- Flash firmware
- Test
- Ship a working product

### How to Order

1. Go to https://www.pcbway.com/
2. PCB Quote → Enable Assembly
3. Select "Box Build Assembly: Yes"
4. Upload:
   - Gerber files (PCB design)
   - BOM (bill of materials)
   - Pick-and-place file
   - Enclosure CAD (STEP/STL)
   - Assembly instructions
5. Submit for engineering review
6. Get quote for finished product

### Estimated Cost (1 Unit)

| Item | Cost |
|------|------|
| PCB (2-layer, 5pcs) | $2-5 |
| Components | $5-15 |
| SMT Assembly | $29 promo |
| Enclosure (3D print) | $5-15 |
| Box Build (wiring, test) | $20-50 |
| Firmware flash | $8-15 |
| **Total** | **$70-130** |
| **Shipping** | **$10-20** |
| **All-in** | **$80-150** |

### Pros
- One order, everything included
- Professional quality
- Repeatable

### Cons
- Need engineering review (1-3 days)
- $80-150 for 1 unit (still expensive)
- Minimum order may apply

---

## Option 2: Makerfabs

### What They Do
- PCB assembly + programming + testing
- Can assemble your external parts into finished product
- Specialise in ESP32 products

### How to Order

1. Go to https://www.makerfabs.com/pcb-assembly.html
2. Submit PCB design + BOM
3. They assemble and test the PCB
4. You provide enclosure + they assemble (or you assemble)

### Estimated Cost (1 Unit)

| Item | Cost |
|------|------|
| PCB + components + assembly | $30-60 |
| Programming + testing | $10-20 |
| **Total (PCB only)** | **$40-80** |
| **With your enclosure** | **Add $5-15** |

### Pros
- 1-unit friendly
- ESP32 specialist
- Can do firmware

### Cons
- May need to ship them your enclosure
- Final assembly may be separate

---

## Option 3: PCBark

### What They Do
- Full PCBA + enclosure integration + wiring + programming + packaging
- No MOQ advertised

### How to Order

1. Go to https://pcbark.com/
2. Submit full design package
3. They quote the complete product

### Estimated Cost (1 Unit)

| Item | Cost |
|------|------|
| Full product assembly | $50-100 (estimated) |
| **Total** | **$50-100 + shipping** |

### Pros
- No MOQ
- Full product assembly
- Custom order

### Cons
- Not instant checkout
- Need to contact them
- Pricing unclear

---

## Option 4: The Hybrid Approach (Cheapest)

### Step 1: Design a Custom PCB
- Use KiCad or EasyEDA
- Put ESP32-S3 module + all components on one board
- JLCPCB assembles it: $8 setup + $0.0016/joint
- **Cost: $10-15 for 2 assembled boards**

### Step 2: Order Enclosure
- JLC3DP: $0.30-5 per enclosure
- **Cost: $1-5**

### Step 3: Order Components Not on PCB
- Sensors, motors, batteries from AliExpress/LCSC
- **Cost: $5-15**

### Step 4: Assembly
- **This is the hard part**
- Option A: Pay someone locally (UK Electronics, Prism)
- Option B: Ship parts to Makerfabs for assembly
- Option C: Pay a local maker/hacker space

### Total Cost

| Item | Cost |
|------|------|
| PCB (JLCPCB) | $10-15 |
| Enclosure (JLC3DP) | $1-5 |
| Components (AliExpress) | $5-15 |
| Assembly (someone) | $20-50 |
| **Total** | **$36-85** |

---

## The Real Solution

### For Prototyping (1-3 units)

1. **Design custom PCB** (KiCad/EasyEDA)
2. **Order from PCBWay** with Box Build Assembly
3. **Get 1 working product** for $80-150
4. **Test thoroughly**

### For Small Batch (5-10 units)

1. **Design custom PCB**
2. **Order from JLCPCB** (PCB + assembly)
3. **Order enclosures from JLC3DP**
4. **Assemble at UK Electronics or M-TEK**
5. **Cost: $30-50 per unit**

### For Production (50+ units)

1. **Design custom PCB**
2. **Order from Seeed Fusion ODM**
3. **Full turnkey: $15-25 per unit**

---

## What You Need to Do Now

### 1. Design the PCB
- Choose 1 engine (Desk Agent is simplest)
- Design custom PCB with ESP32-S3 + OLED + buzzer + LED
- Use KiCad (free) or EasyEDA (free, integrates with JLCPCB)

### 2. Test PCBWay Box Build
- Submit the design
- Get quote for 1 assembled unit
- This gives you the real number

### 3. Test Makerfabs
- Submit same design
- Compare pricing
- This is your backup

### 4. Build Prototype
- Get 1 working unit
- Test all functions
- Document assembly process
- Then decide: scale or iterate

---

## The Numbers

| Approach | 1-Unit Cost | Time | Skill Needed |
|----------|-------------|------|--------------|
| PCBWay Box Build | $80-150 | 7-14 days | PCB design |
| Makerfabs | $40-80 | 7-14 days | PCB design |
| PCBark | $50-100 | 7-14 days | PCB design |
| Hybrid (DIY assembly) | $36-85 | 5-10 days | PCB + soldering |
| Seeed Fusion (full turnkey) | $189-299 | 7-15 days | None |

**The cheapest way to get 1 working unit: PCBWay Box Build at $80-150.**

**The cheapest way to get 10 working units: JLCPCB + UK Electronics at $30-50 each.**

---

## Bottom Line

| Question | Answer |
|----------|--------|
| Can we get 1 assembled unit? | **YES** — PCBWay, Makerfabs, or PCBark |
| What's the cost? | **$80-150** for 1 unit |
| Is there a cheaper way? | **Not really** — assembly is the hard step |
| What's the real solution? | **Design custom PCB** → **PCBWay Box Build** |

**The trick is to design a custom PCB that puts everything on one board, then let a factory assemble the whole thing.**
