# The Network Sensor System

## The Concept

**One Glimling (hub) manages multiple wireless sensors (one per plant).**

Not one plant monitor. A WHOLE PLANT MANAGEMENT SYSTEM.

---

## The Architecture

### Hub (Glimling)

| Component | Purpose |
|-----------|---------|
| ESP32-S3 | Main controller |
| Display (optional) | Show plant status |
| LED | Visual feedback |
| WiFi | Connects to internet |
| BLE | Connects to sensors |
| MCP server | AI integration |

### Spokes (Plant Sensors)

| Component | Purpose |
|-----------|---------|
| ESP32-C3 | Cheaper, smaller controller |
| Soil moisture sensor | Read plant moisture |
| BLE | Connects to hub |
| Battery | 1 year+ life |
| Small, discrete | Fits in any pot |

### Network

```
Hub ← BLE → Sensor 1 (Monstera)
Hub ← BLE → Sensor 2 (Fern)
Hub ← BLE → Sensor 3 (Cactus)
Hub ← WiFi → Internet → Muse/ChatGPT

Up to 10 sensors per hub.
```

---

## The User Experience

### Setup

1. Plug in Glimling hub
2. Connect to WiFi
3. Open glimlings.app
4. Add sensor 1: "This is my Monstera"
5. Add sensor 2: "This is my Fern"
6. Add sensor 3: "This is my Cactus"
7. Done!

### Daily Use

```
User: "Muse, how are my plants?"
Muse: Calls Glimling MCP "get_all_sensors"
Glimling: Returns [
  {name: "Monstera", moisture: 65%, status: "healthy"},
  {name: "Fern", moisture: 30%, status: "dry"},
  {name: "Cactus", moisture: 80%, status: "wet"}
]
Muse: "Your Fern needs water! Monstera and Cactus are fine."
```

### Automation

- Glimling checks all sensors every 5 minutes
- Alerts when any plant needs attention
- Tracks history per plant
- Learns watering patterns
- Suggests care tips

**This is the killer feature. One device manages ALL your plants.**

---

## Indoor vs Outdoor

### Sporebert Indoor

| Parameter | Value |
|-----------|-------|
| Type | Indoor Hub + Sensors |
| Hub | Glow hub (display, LED, WiFi, BLE) |
| Sensors | BLE moisture sensors |
| Waterproof | No (indoor only) |
| Hub price | £49.99 |
| Sensor price | £14.99 |
| Bundle | £89.99 (hub + 3 sensors) |
| Target | Indoor plant parents |

### Mosswick Outdoor

| Parameter | Value |
|-----------|-------|
| Type | Outdoor Hub + Sensors |
| Hub | Glow hub (display, LED, WiFi, BLE) |
| Sensors | BLE moisture sensors (waterproof) |
| Waterproof | YES (IP65) |
| Hub price | £59.99 |
| Sensor price | £19.99 |
| Bundle | £109.99 (hub + 3 sensors) |
| Target | Outdoor gardeners |

---

## The Economics

### Per Unit

| Item | Cost | Retail | Margin |
|------|------|--------|--------|
| Hub (Indoor) | £15-20 | £49.99 | 60-70% |
| Hub (Outdoor) | £20-25 | £59.99 | 58-67% |
| Sensor (Indoor) | £3-5 | £14.99 | 67-80% |
| Sensor (Outdoor) | £5-8 | £19.99 | 60-75% |

### Bundles

| Bundle | Cost | Retail | Margin |
|--------|------|--------|--------|
| Indoor (Hub + 3) | £24-35 | £89.99 | 61-73% |
| Outdoor (Hub + 3) | £35-49 | £109.99 | 55-68% |

### Customer Lifetime Value

```
Hub: £49.99 (one-time)
Sensors: £14.99 × 10 plants = £149.90
Total: £199.89

THIS IS THE RECURRING REVENUE.
Buy hub once, buy sensors forever.
```

---

## Why This Is Better

### Before (Single Plant Monitor)

- One sensor per device
- One plant per Glimling
- Buy multiple Glimlings for multiple plants
- £44.99 × 5 plants = £224.95

### After (Network Sensor System)

- One hub manages all plants
- Multiple sensors per hub
- Buy sensors as you add plants
- £49.99 + (£14.99 × 5) = £124.94

**Saves customer £100. Still generates recurring revenue. Much more valuable product.**

---

## The Product Line

### Indoor

- Sporebert Hub: £49.99
- Plant Sensor: £14.99 each
- Starter Kit (Hub + 3): £89.99
- Expansion Pack (3 sensors): £39.99

### Outdoor

- Mosswick Hub: £59.99
- Plant Sensor (waterproof): £19.99 each
- Starter Kit (Hub + 3): £109.99
- Expansion Pack (3 sensors): £54.99

### Specialist

- pH Sensor: £49.99
- EC Sensor: £69.99
- Camera Module: £39.99
- Weather Module: £29.99

---

## The Play

```
1. Buy hub (£49.99)
2. Buy 3 sensors (£39.99)
3. Add more plants (£14.99 each)
4. Add specialist sensors (£30-70 each)

This is the platform.
This is the recurring revenue.
This is the killer product.
```

---

## Waterproofing (Outdoor Version)

### Sensor Requirements

| Requirement | Solution |
|-------------|----------|
| IP65 rating | Dust tight, water jets protected |
| Material | ASA or PA12 (UV resistant) |
| Sealing | TPU gasket between halves |
| Cable entry | M12 cable gland |
| Battery | Sealed compartment |

### Cost Impact

| Item | Indoor | Outdoor |
|------|--------|---------|
| Sensor cost | £3-5 | £5-8 |
| Retail price | £14.99 | £19.99 |
| Margin | 67-80% | 60-75% |

**Waterproof adds £2-3 cost, £5 retail. Margin drops 7-10%.**

---

## The Vision

```
CUSTOMER BUYS:
  Starter Kit (£89.99)
  Hub + 3 sensors

CUSTOMER SETS UP:
  - Plugs in hub
  - Connects to WiFi
  - Labels each sensor:
    "Monstera", "Fern", "Cactus"

CUSTOMER USES:
  - Asks Muse about plants
  - Gets alerts when water needed
  - Tracks growth over time
  - Adds more plants later

CUSTOMER COLLECTS:
  - Buys more sensors (£14.99 each)
  - Adds specialist sensors
  - Builds plant management system

THIS IS THE FUTURE.
One hub, infinite sensors, whole garden managed.
```
