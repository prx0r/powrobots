# Assembly Solution + New Engine Ideas

## The Assembly Problem — Solved

### The Problem
Customer assembles themselves = bad experience

### The Solution
**WE ASSEMBLE BEFORE SHIPPING.**

```
1. Pre-assemble snap-in modules (ESP32 + sensors)
2. Test each module
3. Print enclosure
4. Snap module into enclosure
5. Ship finished product

Customer receives: Ready-to-use Glimling
Customer does: Plug in USB-C power
That's it.
```

### The Cost

| Item | Cost |
|------|------|
| Electronics | £5-15 |
| Enclosure | £2-5 |
| Assembly labour | £5-10 (our time) |
| Packaging | £3 |
| Shipping | £3.50 |
| **Total** | **£20-35** |

| Retail | Margin |
|--------|--------|
| £49.99 | 30-50% |
| £59.99 | 40-55% |
| £69.99 | 50-60% |

**Lower margin than DIY kit, but better experience.**

---

## How to Create Designs for Each Product

### Step 1: Create Parametric Templates

We have 8 templates in `enclosures/templates/`:
- `frog.scad` — Garden frog (SENSE)
- `mushroom.scad` — Garden mushroom (SENSE)
- `ghost.scad` — Garden ghost (SENSE)
- `goblin.scad` — Desk goblin (ACT)
- `familiar.scad` — Desk familiar (ACT)
- `weather.scad` — Home weather (SENSE)
- `mood.scad` — Home mood (SENSE)
- `bookworm.scad` — Bookworm (REMEMBER)

### Step 2: Generate Default STLs

```bash
# Generate default designs
python enclosures/generate.py --product frog --colour green
python enclosures/generate.py --product mushroom --colour purple
# ... etc
```

### Step 3: Character-Specific Designs

| Product | Character | Key Features |
|---------|-----------|--------------|
| Mosswick | Frog | Round body, big eyes, sensor hole |
| Sporebert | Mushroom | Cap + stem, LED window |
| Boo Bloom | Ghost | Wispy shape, LED glow |
| Puck | Goblin | Pointy ears, OLED window, encoder |
| Mab | Familiar | Compact, OLED window, encoder |
| Nimbus | Weather | Cloud shape, sensor vents |
| Chroma | Mood | Diffuser shape, LED window |
| Wormington | Bookworm | Book shape, NFC window |

### Step 4: Validate Each Design

- Check against constraints
- Verify electronics fit
- Test snap-fit
- Document assembly

### Step 5: Pre-Print Inventory

- Order 5-10 of each from JLC3DP
- Store in inventory
- Ship when order comes in

---

## New Engine Ideas

### MOVE Engine

| Parameter | Value |
|-----------|-------|
| Capability | Motors, servos, movement |
| Components | ESP32 + servo + motor driver |
| Products | Pet robot, desk companion, interactive toy |
| Cost | £25-35 |
| Complexity | Medium (moving parts) |

### POWER Engine

| Parameter | Value |
|-----------|-------|
| Capability | Battery, charging, power management |
| Components | ESP32 + battery + BMS + solar |
| Products | Outdoor sensor, portable device, garden monitor |
| Cost | £20-30 |
| Complexity | Medium (battery safety) |

### CONNECT Engine

| Parameter | Value |
|-----------|-------|
| Capability | LoRa, BLE, mesh networking |
| Components | ESP32 + LoRa module + antenna |
| Products | Long-range sensor, mesh network node, outdoor monitor |
| Cost | £25-35 |
| Complexity | Medium (antenna design) |

### DISPLAY Engine

| Parameter | Value |
|-----------|-------|
| Capability | E-ink, kindle-like display |
| Components | ESP32 + e-ink display + touch |
| Products | Calendar, weather display, note taker, photo frame |
| Cost | £30-40 |
| Complexity | Low (no moving parts) |

### MUSIC Engine

| Parameter | Value |
|-----------|-------|
| Capability | Audio synthesis, playback, recording |
| Components | ESP32 + DAC + amp + speakers |
| Products | Music box, sound machine, voice recorder |
| Cost | £25-35 |
| Complexity | Medium (acoustics) |

### VISION Engine

| Parameter | Value |
|-----------|-------|
| Capability | Camera + AI processing |
| Components | ESP32-S3 + camera + SD card |
| Products | Security camera, pet monitor, time-lapse |
| Cost | £30-40 |
| Complexity | High (AI processing) |

### HEALTH Engine

| Parameter | Value |
|-----------|-------|
| Capability | Heart rate, SpO2, temperature |
| Components | ESP32 + health sensors + display |
| Products | Health monitor, elderly companion, fitness tracker |
| Cost | £35-50 |
| Complexity | High (medical accuracy) |

### GARDEN Engine

| Parameter | Value |
|-----------|-------|
| Capability | Soil, water, light, weather |
| Components | ESP32 + soil sensor + weather station |
| Products | Garden monitor, plant care, weather station |
| Cost | £20-30 |
| Complexity | Low (outdoor housing) |

---

## Engine Priority

| Priority | Engine | Why |
|----------|--------|-----|
| 1 | **SENSE** | Already defined, simple, outdoor use |
| 2 | **ACT** | Already defined, display + controls |
| 3 | **TALK** | Already defined, audio + voice |
| 4 | **SEE** | Already defined, camera + AI |
| 5 | **MOVE** | New, adds movement, high appeal |
| 6 | **DISPLAY** | New, e-ink, low power |
| 7 | **GARDEN** | New, outdoor, practical |
| 8 | **HEALTH** | New, elderly care, high value |

---

## The Plan

### Immediate (This Week)
1. Order M5Stack module for Desk Goblin prototype
2. Design snap-fit enclosure
3. Flash firmware
4. Test assembly

### Short-Term (Next 2 Weeks)
5. Create all 8 product designs
6. Validate against constraints
7. Order 5 of each from JLC3DP
8. Pre-assemble electronics modules

### Medium-Term (Next Month)
9. List on Etsy
10. Start selling
11. Collect feedback
12. Iterate designs

### Long-Term (Next Quarter)
13. Add MOVE engine
14. Add DISPLAY engine
15. Add GARDEN engine
16. Scale to 100+ orders/month
