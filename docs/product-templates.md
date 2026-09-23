# Product Templates — What Our Graph Can Build Right Now

Mapped to components we already have in the database with verified pricing.

---

## Template 1: Plant Sprite (MUSHROOM)

**Status:** READY TO BUILD — all parts in graph

### BOM

| Component | Supplier | Price | Category |
|-----------|----------|-------|----------|
| ESP32-S3 DevKit | Amazon UK | £8.90 | microcontroller |
| Capacitive Soil Moisture Sensor | Alibaba | $1.20 | sensor |
| BH1750 Ambient Light Sensor | Alibaba | $1.50 | sensor |
| DHT22 Temp/Humidity Sensor | Alibaba | $2.00 | sensor |
| WS2812B RGB LED | Alibaba | $0.30 | led |
| Active Buzzer 5V | Alibaba | $0.20 | audio |
| 5V Relay Module | Alibaba | $1.00 | relay |
| USB-C Cable | Alibaba | $1.00 | connector |

**Total BOM: ~£15**

### Enclosure
- Mushroom shape: `enclosures/generate.py --product plant-sprite --shape mushroom`
- STL files: body + sensor mount + LED diffuser
- 3D print at JLC3DP from $1

### Firmware
- `firmware/plant-sprite/main.py`
- Reads: moisture, light, temp
- Reports to: POW MCP
- Muse integration: plant status events

### Personalisation
- Name: customer chooses
- Character: mushroom/goblin/frog/ghost/robot
- Colour: enclosure + LED
- Plant name: customer chooses
- Personality: friendly/serious/playful

### Pricing
| Item | Cost |
|------|------|
| Components | £15 |
| Enclosure (3D print) | £3 |
| Assembly | £5 |
| Packaging | £3 |
| **Total COGS** | **£26** |
| **Etsy price** | **£79** |
| **Margin** | **~67%** |

---

## Template 2: Desk Goblin (BOX)

**Status:** READY TO BUILD — all parts in graph

### BOM

| Component | Supplier | Price | Category |
|-----------|----------|-------|----------|
| ESP32-S3 DevKit | Amazon UK | £8.90 | microcontroller |
| SSD1306 OLED 0.96" | Alibaba | $3.00 | display |
| Rotary Encoder | Alibaba | $1.50 | input |
| Push Button | Alibaba | $0.50 | input |
| WS2812B RGB LED | Alibaba | $0.30 | led |
| Active Buzzer 5V | Alibaba | $0.20 | audio |
| USB-C Cable | Alibaba | $1.00 | connector |

**Total BOM: ~£12**

### Enclosure
- Box shape: `enclosures/generate.py --product desk-goblin --shape box`
- STL files: body + display bezel + encoder mount
- 3D print from $1

### Firmware
- `firmware/desk-goblin/main.py`
- OLED expressions, rotary control, buzzer
- Reports to: POW MCP
- Muse integration: calendar/task events

### Pricing
| Item | Cost |
|------|------|
| Components | £12 |
| Enclosure | £3 |
| Assembly | £5 |
| Packaging | £3 |
| **Total COGS** | **£23** |
| **Etsy price** | **£49** |
| **Margin** | **~53%** |

---

## Template 3: Desk Companion (BOX — screenless)

**Status:** READY TO BUILD — simplest product

### BOM

| Component | Supplier | Price | Category |
|-----------|----------|-------|----------|
| ESP32-S3 DevKit | Amazon UK | £8.90 | microcontroller |
| WS2812B RGB LED | Alibaba | $0.30 | led |
| Active Buzzer 5V | Alibaba | $0.20 | audio |
| USB-C Cable | Alibaba | $1.00 | connector |

**Total BOM: ~£11**

### Enclosure
- Box or mushroom shape
- No display cutout needed
- Simplest to manufacture

### Pricing
| Item | Cost |
|------|------|
| Components | £11 |
| Enclosure | £3 |
| Assembly | £3 |
| Packaging | £3 |
| **Total COGS** | **£20** |
| **Etsy price** | **£35** |
| **Margin** | **~43%** |

---

## Cross-product component reuse

All three products share the same electronics core:

```
ESP32-S3 DevKit (£8.90)          ← shared by ALL
WS2812B RGB LED (£0.30)          ← shared by ALL
Active Buzzer (£0.20)            ← shared by Plant + Desk
USB-C Cable (£1.00)              ← shared by ALL
```

**Add-ons per product:**
- Plant: moisture + light + temp sensors + relay
- Desk Goblin: OLED + encoder + button
- Desk Companion: nothing (screenless)

**One core platform. Three enclosures. Infinite personalisation.**

---

## What our graph knows that competitors don't

| We know | Who else knows |
|---------|---------------|
| ESP32-S3 costs £8.90 from Kunkune UK | Anyone who googles it |
| Soil moisture sensor costs $1.20 from Alibaba | Anyone who googles it |
| **STS3215 fits SO-101 all joints** | Only us + LeRobot docs |
| **LDS01RR fits 12 Roborock models** | Only us + iFixit community |
| **Roller brush fits 8 Dreame models** | Only us + iFixit community |
| **Cross-brand part compatibility** | **Nobody has this systematically** |
| **UK supplier routing** | **Nobody connects all 15 suppliers** |
| **Failure patterns by model** | **Nobody tracks this** |

**The graph is the moat. Not the products. The products generate the data that makes the graph more valuable.**
