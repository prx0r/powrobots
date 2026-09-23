# Cheap Waterproof Sensors — The Reality

## The Problem

**Waterproof sensors are expensive. The cheap sensors (£0.50-2.50) are NOT waterproof.**

| Sensor | Price | Waterproof? | Notes |
|--------|-------|-------------|-------|
| Capacitive v1.2 | £0.50 | ❌ NO | Corrosion-resistant, not waterproof |
| Capacitive v2.0 | £1.50 | ❌ NO | Better accuracy, still not waterproof |
| DFRobot SEN0193 | £4.75 | ❌ NO | Indoor only, waterproof sensing area only |
| DFRobot SEN0308 | £12.00 | ✅ YES (IP65) | Outdoor, but expensive |
| Ecowitt WH51 | £14.50 | ✅ YES (IP66) | Proven, but expensive |
| Ecowitt WH52 | £22.50 | ✅ YES (IP66) | 3-in-1, expensive |

**The outdoor challenge: A waterproof probe alone costs almost as much as the proposed £19.99 retail price.**

---

## The Options

### Option 1: Use Ecowitt (Proven, Expensive)

| Product | Price | MOQ | Waterproof |
|---------|-------|-----|------------|
| Ecowitt WH51 | $17.99 | 1 | IP66 |
| Ecowitt WH52 | $27.99 | 1 | IP66 |

**Pros:** Proven, reliable, works immediately
**Cons:** Expensive, can't customise, need gateway

### Option 2: Use DFRobot (Mid-range)

| Product | Price | MOQ | Waterproof |
|---------|-------|-----|------------|
| DFRobot SEN0193 | $5.90 | 1 | ❌ Indoor only |
| DFRobot SEN0308 | $14.90 | 10 | IP65 |

**Pros:** Good quality, documented
**Cons:** Still expensive for outdoor

### Option 3: Generic Alibaba (Cheap, Unproven)

| Product | Price | MOQ | Waterproof |
|---------|-------|-----|------------|
| IP67 Capacitive Probe | $15 | 1 | IP67 |
| IP68 Soil Sensor | $20+ | 1 | IP68 |
| RS485 Soil Sensor | $15-20 | 1 | IP68 |

**Pros:** Cheapest waterproof option
**Cons:** Unproven quality, need custom integration

### Option 4: Build Custom (Cheapest at Volume)

| Component | Price | MOQ | Notes |
|-----------|-------|-----|-------|
| ESP32-C3 | $1.50 | 1 | Brain |
| Capacitive probe | $1-2 | 1 | Sensor |
| Waterproof enclosure | $2-3 | 1 | JLC3DP |
| Cable gland | $0.50 | 1 | Sealed entry |
| **Total** | **$5-7** | | At volume |

**Pros:** Cheapest at volume, full customisation
**Cons:** Need development, testing, certification

---

## The Honest Answer

### For Christmas 2026

**Use Ecowitt sensors.** They're expensive but proven. The alternative is no product.

| Product | Cost | Retail | Margin |
|---------|------|--------|--------|
| Sporebert + 1 WH51 | £14.50 + £9.60 = £24.10 | £49.99 | 52% |
| Mosswick + 1 WH51 | £14.50 + £14.60 = £29.10 | £59.99 | 51% |

**This works.** 52% margin is viable.

### For Post-Christmas

**Develop custom waterproof sensors.** Target cost: £5-7 per sensor.

| Component | Source | Cost |
|-----------|--------|------|
| ESP32-C3 | AliExpress | £1.50 |
| Capacitive probe | AliExpress | £1.50 |
| Waterproof enclosure | JLC3DP | £2.50 |
| Cable gland | AliExpress | £0.50 |
| Battery | AliExpress | £2.00 |
| PCB | JLCPCB | £2.00 |
| **Total** | | **£10.00** |

**Target retail:** £19.99 (50% margin)

### For Production (1000+ units)

**Full custom with POW branding.** Target cost: £3-5 per sensor.

| Component | Source | Cost (1000) |
|-----------|--------|-------------|
| ESP32-C3 module | LCSC | £2.50 |
| Capacitive probe | Alibaba OEM | £1.00 |
| Waterproof enclosure | JLC3DP | £1.50 |
| Cable gland | Alibaba | £0.30 |
| Battery | Alibaba | £1.50 |
| PCB | JLCPCB | £1.00 |
| Assembly | Factory | £1.00 |
| **Total** | | **£8.80** |

**Target retail:** £14.99 (41% margin)

---

## The Strategy

### Christmas 2026 (Immediate)

```
Use Ecowitt sensors (proven, expensive)
Bundle 1 sensor with hub
Sell expansion packs
Accept lower margins (52%)
```

### Post-Christmas (Next Quarter)

```
Develop custom waterproof sensor
Target cost: £10 per sensor
Test with 10 units
Validate waterproofing
```

### Production (2027+)

```
Full custom with POW branding
Target cost: £5-7 per sensor
Order 1000+ units
Achieve 40-50% margins
```

---

## The Key Insight

**Waterproofing is the hard part, not the electronics.**

- Electronics: £3-5 (ESP32 + probe + PCB)
- Waterproofing: £5-10 (enclosure + gasket + gland + vent)
- Total: £8-15

**The waterproof enclosure costs more than the electronics inside it.**

That's why Ecowitt charges $17.99 for a "simple" moisture sensor. The value is in the waterproofing, not the electronics.

---

## What to Tell Customers

### Indoor (Sporebert)

"Your Sporebert comes with one wireless plant sensor. Add more as your garden grows."

### Outdoor (Mosswick)

"Your Mosswick comes with one weather-resistant sensor. It's IP66 rated and works in rain."

### Expansion Packs

"Buy additional sensors for £14.99-19.99 each. Each sensor gets its own name and plant history."

**Don't promise custom waterproof sensors yet. Use Ecowitt, prove the concept, then develop custom hardware.**
