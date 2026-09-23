# Glimlings: Personalised Garden-Creature Studio

## The Vision

**A personalised garden-creature studio sitting on top of an open, verified sensor network.**

Customer designs a Glimling inspired by their cat, chooses electronics, adds smaller characters to plants. Each plant gets its own name, photo, species, sensor history and care recommendations.

**POW doesn't manufacture electronics or every sensor. It owns the experience that makes all these separate products work together.**

---

## Three Physical Products

### 1. The Guardian

The main talking, glowing Glimling. Uses existing voice module (M5Stack Atom Voice).

### 2. Plantlings

Little pet-inspired or mythical characters that decorate compatible moisture sensors and identify individual plants.

### 3. Garden Helpers (Later)

Watering frogs, weather sprites, camera-equipped lookouts. Uses tested third-party hardware.

**The Guardian is the first gift. The Plantlings are the repeat purchases.**

---

## Two Standard Hardware Systems

| Standard | Purpose | Reference |
|----------|---------|-----------|
| M5Stack Atom Voice C008-C | Talking, glowing Guardian | $13.50 / £13 UK |
| Ecowitt GW1200 + WH51 | Expandable plant network | $48.99 starter kit, 16 sensors |

**Separate systems connected by POW software.** Ecowitt sensors don't communicate directly with M5Stack.

For cheapest entry: HHCC Flower Care Bluetooth sensor (single plant, no gateway needed).

For plant identification: Pl@ntNet API (500 free identifications daily).

---

## Canonical Suppliers by Country

### M5Stack Atom Voice

| Region | Supplier | Price | Status |
|--------|----------|-------|--------|
| UK | The Pi Hut | £13 inc VAT | In stock |
| EU | BerryBase | €15.90 inc VAT | 1-3 day dispatch |
| US | DigiKey | $13.50 | In stock |
| Canada | DigiKey Canada | C$21.09 | In stock |
| Australia | DigiKey Australia | A$21.63 inc GST | In stock |
| Japan | Switch Science | ¥2,563 inc tax | In stock |
| Other | M5Stack official | $13.50 | International shipping |

**Standardise hardware globally. Regional suppliers compete to deliver same approved module.**

---

## Three Physical Templates

| Template | Hardware | Customer Designs |
|----------|----------|------------------|
| **Guardian** | M5Stack Atom Voice C008-C | Mushroom, cat spirit, fairy, ghost |
| **Indoor Plantling** | HHCC sensor | Miniature animal surrounding sensor |
| **Outdoor Plantling** | Ecowitt WH51 | Weather-resistant decorative cap |

**Guardian:** Unobstructed mic/speaker openings, USB access, antenna clearance, accessible button.

**Plantlings:** Decorative character separate from functional probe. Cat's ears above pot, but body doesn't stop probe reaching correct depth.

---

## The Plant-Growing Experience

### Step 1: Photograph Your Plant

Upload photos. Pl@ntNet proposes likely species. Owner confirms (not silent AI guess).

### Step 2: Tell Us About Its Home

Name, position, growing medium, pot size, drainage, sunlight.

### Step 3: Assign Its Sensor

Scan/select existing sensor. Check model, connection, battery, calibration.

### Step 4: Give It a Plantling

Design tiny creature inspired by pet. Restricted to approved mounting template.

**Database maintains separate identities: plant, sensor, Plantling.** Sensor breaks → replace without losing history. Repot plant → history continues, care model records change.

---

## Example: Gerald the Tomato

```
Owner: "How is Gerald doing?"
Glimling: "His soil is drying more quickly than earlier this week.
         Last recorded watering was two days ago.
         Would you like to check him now?"
Owner: "Show me his growth."
App: Displays photographs over time alongside moisture and watering events.
```

**Much more defensible than diagnosing from a single measurement.**

---

## MCP and Agent Architecture

```
                 POW Studio
            Designs + plant registry
                       |
                Garden intelligence
             History + care + alerts
                       |
             Authenticated POW gateway
               /                \
          MCP tools          Event service
               \                /
              Hardware adapters
               /             \
        Glimling voice     Plant sensors
        M5Stack / ESP32   BLE / Ecowitt
```

### MCP Tools

- `list_plants`
- `get_plant_history`
- `get_garden_alerts`
- `record_watering`
- `get_care_guidance`

**Separate event system tells Guardian when to glow or speak.**

**Home Assistant already has MCP server and plant-monitoring. Support it for technically inclined customers.**

---

## Country-Aware Purchasing

Customer enters delivery country and postcode. POW compares suppliers using:
- Compatible part numbers
- Stock availability
- Total delivered price
- Estimated arrival
- Taxes
- Return arrangements

**Don't advertise bundled delivery based on fastest item. Different suppliers = separate purchases.**

**Ecowitt radio compatibility:** 915MHz (NA), 868MHz (EU), 433MHz (Oceania). Match gateway and sensors.

---

## First Development Checkpoints

1. **One real Guardian:** M5Stack Atom Voice + validated shell + reliable speech/lighting
2. **One real plant integration:** HHCC Bluetooth + simultaneous voice operation
3. **One complete adoption experience:** Photo → identify → name → sensor → history
4. **One personalised Plantling:** Pet photo → stylised design → manufactured → fit verified
5. **One international purchase:** Genuine quotations UK/US/EU including delivery

---

## The Complete Loop (First Demo)

```
1. Upload photo of cat
2. Turn into garden Guardian
3. Photograph and name basil
4. Connect real sensor
5. Cat-inspired Glimling tells you when basil needs attention
```

**Testable without manufacturing electronics, building sensor catalogue, or solving automated watering.**
