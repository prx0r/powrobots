# Expanded Garden Range — Modular Sensor System

## The Key Insight

**Organise by what customers want, not what the ESP32 can support.**

There's a meaningful difference between:
- A £45 mushroom that tells you when to water a plant
- A £150 hydroponics companion that measures nutrient-solution chemistry

---

## The Correction: pH and EC

pH and EC are **specialist, not universal**.

- Soil pH affects nutrient availability, but isn't the #1 cause of plant death
- DFRobot liquid pH kit: $39.50
- DFRobot laboratory EC kit: $69.90
- DFRobot wet-soil pH probe: $99
- These are supplier list prices, before integration or delivery

**Two distinct opportunities:**
1. Affordable, expressive Garden Glimlings for general plant owners
2. More capable specialist Glimlings for hydroponics, greenhouses, automated growing

---

## The Expanded Garden Range

### Gift Range (Affordable, Expressive)

| Product | What It Does | Price | Engineering Reality |
|---------|--------------|-------|---------------------|
| **Sporebert Garden** | Glows, changes expression, warns when plant needs attention | £44.99 | Moisture, light, ambient temperature — straightforward |
| **Fern Kinetic** | Physically curls/unfurls in response to moisture | £59.99-79.99 | Needs tested actuator and replaceable frond |
| **Nimbus Weather** | Cloud showing temp, humidity, pressure, UV | £69.99 | BME280 (not BMP280) + UV sensor |
| **Boo Bloom Vision** | Ghost that takes periodic photos, growth time-lapse | £79.99-99.99 | Photography achievable; disease detection is separate problem |
| **Mosswick Irrigation** | Frog that controls watering from reservoir | £99.99+ | Requires leak detection, dry-run protection, hardware limits |

### Specialist Range (Hydroponics, Greenhouses)

| Product | What It Does | Price | Engineering Reality |
|---------|--------------|-------|---------------------|
| **Rootkin Hydro** | Monitors hydroponic nutrient-solution pH and EC | Price unconfirmed | Specialist probes, calibration, replacement costs |

---

## Technical Corrections

### Nimbus Weather

- **BMP280** measures pressure and temperature, NOT humidity
- **BME280** combines pressure, humidity, and temperature
- **UV sensor** is separate component
- **UV exposure ≠ photosynthetically active light**
- Need appropriate sensor combination, not just BMP280

### Boo Bloom Vision

- Photography is achievable
- **Reliable disease diagnosis is a separate research problem**
- Espressif has neural-network framework for ESP32-S3
- But plant-disease model needs:
  - Suitable training images
  - Testing across plant species
  - Way to handle uncertain results
- **Start with growth time-lapses and visual check-ins**

### Mosswick Irrigation (The Interesting One)

**Features:**
- Monitors moisture
- Checks reservoir level
- Operates low-voltage pump
- Eyes change colour when reservoir needs refilling

**The valuable part:**
- Knows what happened AFTER watering
- Did moisture actually increase?
- Was reservoir unexpectedly depleted?
- Has plant remained wet too long?

**Safety requirements:**
- Default to safe stopped state
- Local maximum-run limits
- Reservoir-level detection
- Leak detection
- Fault handling when WiFi/AI fails
- **AI agent should never have unrestricted water control**

---

## Modular Sensor Upgrades

### The Concept

Sporebert's sensor can be a **removable part**. Customer keeps character while changing what it measures.

### Module Families

| Family | Purpose | Connector | Examples |
|--------|---------|-----------|----------|
| **Low-voltage sensing** | Soil moisture, light, temp | Standardised 3-pin | DFRobot SEN0193 ($5.90) |
| **Electrochemical** | pH, EC, dissolved oxygen | Specialised (calibration needed) | Atlas Scientific kits |
| **Actuators** | Pumps, servos, motors | Power-rated connector | Water pumps, servos |
| **Camera** | Photography, time-lapse | CSI/USB | ESP32-CAM |

**Key rule:** Different families should NOT share a universal connector if it creates unsafe or electrically incompatible combinations.

### How It Works in POW Studio

| Upgrade | Unlocks |
|---------|---------|
| Moisture probe | Plant-monitoring abilities |
| Approved actuator | Specific movement actions |
| Camera | Photography controls (after owner enables) |

### Calibration and Quality

Each measurement needs its own:
- Calibration procedure
- Quality history
- Maintenance schedule

**Important:**
- EC measures total dissolved ions, NOT nitrogen/phosphorus/potassium separately
- pH electrodes require calibration and maintenance
- pH drifts during prolonged use

---

## The Christmas Play

### Keep Sporebert Simple

- Moisture + light + temperature
- Glowing mushroom
- Interchangeable caps
- No specialist sensors

### Make Upgrade System Part of the Gift

The recipient gets:
1. Delightful creature immediately
2. Possibility of adding plant probe later
3. Different heads
4. Compatible accessories

### Use Same Architecture for Specialist Products

- Same hardware platform
- Same data pipeline
- Different sensor modules
- Different firmware configurations

---

## The Product Strategy

```
CHRISTMAS 2026:
  Sporebert Garden (£44.99)
  + Seasonal caps
  + Build-a-Glimling option

POST-CHRISTMAS:
  + Fern Kinetic (£59.99-79.99)
  + Nimbus Weather (£69.99)
  + Mosswick Irrigation (£99.99+)

SPECIALIST (Later):
  + Rootkin Hydro (price TBD)
  + Boo Bloom Vision (£79.99-99.99)

ACCESSORIES (Always):
  + Seasonal caps
  + Sensor upgrades
  + Replacement parts
```

---

## The Bigger Picture

Garden Glimlings is a promising consumer acquisition wedge, but not necessarily POW's most valuable long-term business. Robot repair and procurement still have stronger connections to POW's specialised parts and outcome data.

**Glimlings gives you a way to develop that manufacturing intelligence using products you control.**

---

## The Decision

### For Christmas 2026

1. **Sporebert** — One standard electronic core
2. **Seasonal accessories** — Caps, scarves, gift messages
3. **Build-a-Glimling** — Gift experience
4. **Fern** — Demo product, not initial fulfillment

### For Post-Christmas

1. **Fern Kinetic** — Mechanical product
2. **Nimbus Weather** — Environmental sensors
3. **Mosswick Irrigation** — Smart watering

### For Specialist Market

1. **Rootkin Hydro** — Hydroponics monitoring
2. **Boo Bloom Vision** — Plant photography

**Keep Christmas simple. Build the platform for later.**
