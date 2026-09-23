# How It Becomes One Box + What Glimlings Are Possible

## The One-Box Process

```
1. DESIGN: Create custom shell (OpenSCAD/Blender)
2. PRINT: Elecrow 3D prints shell
3. SOURCE: Elecrow buys M5Stack + Seeed sensor
4. ASSEMBLE: Elecrow puts shell + electronics together
5. FLASH: Elecrow flashes firmware
6. TEST: Elecrow tests functionality
7. PACK: Elecrow packs with adoption card
8. SHIP: Elecrow ships to customer

CUSTOMER RECEIVES:
  - One box
  - Custom character shell
  - M5Stack Atom Voice (inside shell)
  - Seeed XIAO Soil Sensor
  - USB-C cable
  - Adoption card
  - Setup instructions

CUSTOMER DOES:
  1. Open box
  2. Plug in USB-C
  3. Connect sensor to plant
  4. Scan QR code
  5. Done!

NO SOLDERING. NO WIRING. NO TOOLS. JUST PLUG IN.
```

---

## What Glimlings Are Possible

### Sporebert — Mushroom

| Parameter | Value |
|-----------|-------|
| Concept | Glowing mushroom that watches over plants |
| Sensors | Soil moisture, Light, Temperature |
| Features | LED glow, Voice output, Plant alerts |
| Price | £49.99 |
| Indoor/Outdoor | Indoor |

### Mosswick — Frog

| Parameter | Value |
|-----------|-------|
| Concept | Friendly frog that monitors garden |
| Sensors | Soil moisture, Temperature, Humidity |
| Features | LED eyes, Croak sound, Waterproof |
| Price | £59.99 |
| Indoor/Outdoor | Outdoor |

### Boo Bloom — Ghost

| Parameter | Value |
|-----------|-------|
| Concept | Ghost that glows in the dark |
| Sensors | Light, Motion, Temperature |
| Features | LED glow, Motion detection, Night light |
| Price | £49.99 |
| Indoor/Outdoor | Indoor |

### Nimbus — Cloud

| Parameter | Value |
|-----------|-------|
| Concept | Cloud that shows weather conditions |
| Sensors | Temperature, Humidity, Pressure, Light |
| Features | LED glow, Weather display, UV tracking |
| Price | £49.99 |
| Indoor/Outdoor | Indoor |

### Rootkin — Tree

| Parameter | Value |
|-----------|-------|
| Concept | Tree guardian with NFC plant tracking |
| Sensors | Soil moisture, NFC |
| Features | LED roots, NFC tags, Plant history |
| Price | £54.99 |
| Indoor/Outdoor | Indoor |

### Pebble — Stone

| Parameter | Value |
|-----------|-------|
| Concept | Minimalist zen stone |
| Sensors | Soil moisture, Touch |
| Features | Subtle LED, Touch control, Minimalist |
| Price | £39.99 |
| Indoor/Outdoor | Indoor |

---

## The Platform

### One Base

M5Stack Atom Voice:
- ESP32
- Microphone
- Speaker
- RGB LED
- Button
- Grove port

### Many Heads

- Mushroom (Sporebert)
- Frog (Mosswick)
- Ghost (Boo Bloom)
- Cloud (Nimbus)
- Tree (Rootkin)
- Stone (Pebble)

### Many Sensors

- Seeed XIAO (wireless, BLE)
- M5Stack PIR (motion)
- M5Stack ENV (environment)
- M5Stack Watering (water)

**Same base. Different heads. Different sensors. Same software.**
