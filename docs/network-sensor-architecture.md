# The Two Gift Products — Network Sensor Architecture

## The Concept

**One Glimling looks after your entire garden. Inexpensive wireless sensors live beside individual plants.**

Two mainstream gifts: one for indoor, one for outdoor. Both use the same sensor network.

---

## The Two Gift Products

### Sporebert — Houseplant Guardian (Indoor)

| Parameter | Value |
|-----------|-------|
| Price | £44.99-59.99 |
| What | Glowing mushroom for shelf/windowsill |
| Features | Manages sensors, learns plant names, changes expression |
| Customisation | New cap, personality, AI assistant connection |
| Waterproof | No (indoor only) |

### Mosswick — Garden Guardian (Outdoor)

| Parameter | Value |
|-----------|-------|
| Price | £59.99-79.99 |
| What | Rain-resistant frog for patio/greenhouse |
| Features | Manages outdoor sensors, tracks drying areas |
| Customisation | Swappable head, sealed electronic enclosure |
| Waterproof | YES (IP66 target) |

---

## Competitive Evidence: Ecowitt

**Ecowitt already sells almost exactly this architecture.**

| Product | Price | Features |
|---------|-------|----------|
| WH51 Sensor | $17.99 | IP66 wireless moisture sensor |
| Starter Kit | $48.99 | 1 sensor + WiFi gateway |
| Gateway capacity | 16 sensors | Supports up to 16 soil sensors |

**This validates the network concept. POW's differentiation is the character, plant identification, species-specific care, accessories and AI interface.**

---

## Waterproofing: IP66 Target

### Mosswick's Two-Part Construction

```
OUTER CHARACTER:
  - Swappable frog heads, crowns, costumes
  - Can get wet without exposing electronics
  - Decorative, collectible

INNER SEALED CAPSULE:
  - Electronics, battery, antenna
  - Mechanically secured, gasketed enclosure
  - Gore vents for pressure equalisation

EXTERNAL PROBE:
  - Replaceable, weather-resistant soil sensor
  - Sealed cable interface
  - Never compromises waterproof seal
```

### Key Rules

1. **Swapping character head must never compromise waterproof seal**
2. **No exposed USB-C on outdoor frog** — Use replaceable battery behind gasket
3. **Gore vents for condensation management** — Outdoor temperature changes create pressure differences
4. **Test range through walls, foliage, wet soil** — Before committing to radio

---

## The Sensor Network Architecture

```
                  Glimlings app / AI agent
                            |
                       Home Wi-Fi
                            |
                    Powered gateway
                     /     |     \
              Sensor 1  Sensor 2  Sensor 3
              Monstera   Basil    Fern
                  |
          Optional outdoor Mosswick
          (display and character)
```

### Indoor (Sporebert)

- Gateway built into USB-powered mushroom
- WiFi connects to internet
- BLE/ESP-NOW connects to sensors

### Outdoor (Mosswick)

- Communicates with indoor gateway over sensor network
- Battery-powered (low power)
- Or include small indoor plug-in gateway

---

## Sensor Specifications

### Communication: ESP-NOW

| Parameter | Value |
|-----------|-------|
| Protocol | ESP-NOW (Espressif) |
| Range | 10-100m (depending on obstacles) |
| Power | Very low (deep sleep 5µA) |
| Battery life target | 6+ months (readings every 15-30 min) |
| Capacity | 8 sensors (expandable to 16) |

### Sensor Node (ESP32-C3)

| Component | Purpose |
|-----------|---------|
| ESP32-C3 | WiFi + BLE + deep sleep |
| Capacitive soil moisture | Read plant moisture |
| Battery | 18650 or CR2477 |
| Enclosure | IP66, gasketed |

### Identity System

- Each sensor has unique ID
- QR code for pairing
- Customer names each plant
- Species-specific care profiles
- Historical measurements stored

---

## The Customer Experience

### Setup

1. Buy Sporebert or Mosswick
2. Plug in (Sporebert) or place (Mosswick)
3. Connect to WiFi
4. Add sensor 1: Scan QR, name "Monstera", select species
5. Add sensor 2: Scan QR, name "Basil", select species
6. Done!

### Daily Use

```
User: "Muse, how are my plants?"
Muse: Calls Glimling MCP "get_all_sensors"
Glimling: Returns [
  {name: "Monstera", moisture: 42%, status: "healthy"},
  {name: "Basil", moisture: 24%, status: "dry"},
  {name: "Fern", moisture: 62%, status: "healthy"}
]
Muse: "Your Basil needs water! Monstera and Fern are fine."
```

### Plant History

- Track moisture over time
- Detect drying patterns
- Species-specific care tips
- AI suggestions based on data

---

## The Q4 Development Checkpoint

### Software (Build Now)

| Feature | Status |
|---------|--------|
| Sensor pairing | QR code scanning |
| Plant assignment | Name + species selection |
| Historical measurements | Store and display |
| Low-battery alerts | Notify when sensor battery low |
| Missing-sensor detection | Alert if sensor stops reporting |
| AI access | Connect to Muse/ChatGPT |
| Capacity | 8 sensors (expandable to 16) |

### Hardware (Build Later)

| Feature | Status |
|---------|--------|
| Indoor gateway | Sporebert hub |
| Outdoor gateway | Mosswick hub |
| Sensor nodes | ESP32-C3 + moisture |
| Waterproofing | IP66 target |
| Battery life | 6+ months target |

### Shortcut: Ecowitt Integration

- Ecowitt publishes local HTTP API
- GW1200 gateway supports 16 sensors
- Test plant registry and AI against Ecowitt
- Build own waterproof hardware in parallel

---

## The Product

**A character that adopts your garden, not a gadget attached to one pot.**

The sensor network creates recurring accessory demand. The Glimling gives people a reason to enjoy using it.

---

## Christmas 2026 Plan

### Launch

1. **Sporebert** — Indoor guardian (£44.99-59.99)
2. **Mosswick** — Outdoor guardian (£59.99-79.99)
3. **Plant sensors** — £14.99 indoor / £19.99 outdoor
4. **Starter kit** — Hub + 3 sensors
5. **Expansion packs** — 3 sensors

### Post-Christmas

6. **Fern** — Kinetic demo product
7. **Specialist sensors** — pH, EC, camera
8. **Seasonal accessories** — Caps, costumes
9. **Build-a-Glimling** — Customisation experience

### The Play

```
Christmas 2026: Launch Sporebert + Mosswick
Post-Christmas: Add Fern + accessories
2027: Expand to Desk + Pet
2028: Full platform with specialist sensors
```

**The product is a character that adopts your garden. The sensor network is the platform.**
