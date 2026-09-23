# Engine → Assembly → Product Pricing

Each engine mapped to its assembly pipeline, limitations, and full product pricing.

---

## Engine 1: SENSE

### Components + pricing
| Component | Supplier | Price | MOQ | UK delivery |
|-----------|----------|-------|-----|-------------|
| ESP32-S3 DevKit | Kunkune UK | £8.90 | 1 | Next day |
| ESP32-C3 Module | LCSC | $1.91 | 1 | 2-5 days |
| Capacitive Soil Sensor | AliExpress | $1.20 | 1 | 2-3 weeks |
| BH1750 Light Sensor | AliExpress | $1.50 | 1 | 2-3 weeks |
| DHT22 Temp/Humidity | AliExpress | $2.00 | 1 | 2-3 weeks |
| NFC Reader | AliExpress | £3.00 | 1 | 2-3 weeks |

### Assembly pipeline
```
Components → JLCPCB (PCB) → JLC3DP (enclosure) → UK Electronics (assembly)
```

### Limitations
- ESP32-S3 needs custom PCB for sensor connections
- Soil probe must be waterproof (IP65 for outdoor)
- NFC reader adds complexity (SPI wiring)
- Power: USB or 3xAA batteries (low-power sleep mode needed)

### Products powered
| Product | Extra parts | BOM | Assembly cost | Total | Etsy price |
|---------|------------|-----|---------------|-------|-----------|
| Plant Sprite | LED + button | £13 | £5 | £18 | £79 |
| Coffee Goblin | Weight sensor + display | £18 | £5 | £23 | £59-89 |
| Guitar Guardian | None (reuse SENSE) | £13 | £5 | £18 | £39-69 |
| Sourdough Familiar | RTC module | £14 | £5 | £19 | £59-99 |

---

## Engine 2: REMEMBER

### Components + pricing
| Component | Supplier | Price | MOQ | UK delivery |
|-----------|----------|-------|-----|-------------|
| ESP32-S3 DevKit | Kunkune UK | £8.90 | 1 | Next day |
| DS3231 RTC Module | AliExpress | £1.50 | 1 | 2-3 weeks |
| MicroSD Module | AliExpress | £2.00 | 1 | 2-3 weeks |

### Assembly pipeline
```
Components → JLCPCB (PCB) → JLC3DP (enclosure) → UK Electronics (assembly)
```

### Limitations
- RTC needs battery backup (CR2032)
- MicroSD adds complexity (SPI wiring)
- Time accuracy depends on RTC crystal quality
- Power: USB or battery (RTC keeps time during sleep)

### Products powered
| Product | Extra parts | BOM | Assembly | Total | Etsy |
|---------|------------|-----|----------|-------|------|
| Bookworm | NFC tag | £14 | £3 | £17 | £15-35 |
| Laundry Gremlin | Relay | £14 | £3 | £17 | £29-49 |

---

## Engine 3: ACT

### Components + pricing
| Component | Supplier | Price | MOQ | UK delivery |
|-----------|----------|-------|-----|-------------|
| ESP32-S3 DevKit | Kunkune UK | £8.90 | 1 | Next day |
| SG90 Micro Servo | AliExpress | $1.00 | 1 | 2-3 weeks |
| 5V Relay Module | AliExpress | $1.00 | 1 | 2-3 weeks |
| WS2812B RGB LED | AliExpress | $0.30 | 1 | 2-3 weeks |
| Active Buzzer 5V | AliExpress | $0.20 | 1 | 2-3 weeks |

### Assembly pipeline
```
Components → JLCPCB (PCB) → JLC3DP (enclosure) → UK Electronics (assembly)
```

### Limitations
- Servo needs PWM (specific GPIO pins)
- Relay needs flyback diode protection
- LED needs level shifter for 5V data
- Power: USB sufficient for LED/buzzer, external for servo/relay

### Products powered
| Product | Extra parts | BOM | Assembly | Total | Etsy |
|---------|------------|-----|----------|-------|------|
| Desk Goblin | OLED + encoder + button | £16 | £5 | £21 | £49 |
| Weather Mushroom | Temp sensor | £12 | £3 | £15 | £39-65 |
| Mood Mushroom | None | £12 | £3 | £15 | £39-65 |

---

## Engine 4: TALK

### Components + pricing
| Component | Supplier | Price | MOQ | UK delivery |
|-----------|----------|-------|-----|-------------|
| ESP32-S3 DevKit | Kunkune UK | £8.90 | 1 | Next day |
| MAX98357 Speaker Amp | AliExpress | $2.50 | 1 | 2-3 weeks |
| MEMS Microphone | AliExpress | £1.50 | 1 | 2-3 weeks |
| Push Button | AliExpress | £0.50 | 1 | 2-3 weeks |

### Assembly pipeline
```
Components → JLCPCB (PCB) → JLC3DP (enclosure) → UK Electronics (assembly)
```

### Limitations
- Speaker needs I2S wiring (specific GPIO pins)
- Microphone needs I2S input
- Audio quality limited by small speaker driver
- Push-to-talk initially (always-on needs wake word)

### Products powered
| Product | Extra parts | BOM | Assembly | Total | Etsy |
|---------|------------|-----|----------|-------|------|
| Desk Familiar | None | £14 | £3 | £17 | £49-79 |
| Parcel Owl | Sensor | £15 | £3 | £18 | £39-59 |
| Keys Goblin | NFC + sensor | £17 | £3 | £20 | £39-59 |

---

## Engine 5: SEE

### Components + pricing
| Component | Supplier | Price | MOQ | UK delivery |
|-----------|----------|-------|-----|-------------|
| ESP32-CAM | AliExpress | $7.50 | 1 | 2-3 weeks |
| SG90 Micro Servo x2 | AliExpress | $2.00 | 1 | 2-3 weeks |

### Assembly pipeline
```
Components → JLCPCB (PCB) → JLC3DP (enclosure) → UK Electronics (assembly)
```

### Limitations
- ESP32-CAM has lower processing power than S3
- Pan/tilt servos need 2 PWM channels
- Camera quality limited (2MP OV2640)
- Power: USB or battery (camera uses more power)

### Products powered
| Product | Extra parts | BOM | Assembly | Total | Etsy |
|---------|------------|-----|----------|-------|------|
| 3D Printer Sprite | Temp sensor | £12 | £5 | £17 | £59-99 |
| Camera Familiar | None | £12 | £5 | £17 | £39-59 |

---

## Full product pricing matrix

| Product | Engines | BOM | Assembly | Packaging | Total COGS | Etsy price | Margin |
|---------|---------|-----|----------|-----------|-----------|-----------|--------|
| Plant Sprite | SENSE+ACT | £13 | £5 | £3 | £21 | £79 | 73% |
| Coffee Goblin | SENSE+REMEMBER | £18 | £5 | £3 | £26 | £59-89 | 56-71% |
| Sourdough Familiar | SENSE+REMEMBER | £19 | £5 | £3 | £27 | £59-99 | 54-73% |
| Guitar Guardian | SENSE+REMEMBER | £13 | £5 | £3 | £21 | £39-69 | 46-70% |
| Bookworm | REMEMBER | £14 | £3 | £3 | £20 | £15-35 | -33% to 43% |
| Laundry Gremlin | REMEMBER+ACT | £14 | £3 | £3 | £20 | £29-49 | 31-59% |
| Desk Goblin | ACT+display | £16 | £5 | £3 | £24 | £49 | 51% |
| Desk Familiar | TALK | £14 | £3 | £3 | £20 | £49-79 | 59-75% |
| Weather Mushroom | SENSE+ACT | £12 | £3 | £3 | £18 | £39-65 | 54-72% |
| Mood Mushroom | ACT | £12 | £3 | £3 | £18 | £39-65 | 54-72% |
| Parcel Owl | SENSE+ACT | £15 | £3 | £3 | £21 | £39-59 | 46-64% |
| Keys Goblin | SENSE+REMEMBER | £17 | £3 | £3 | £23 | £39-59 | 41-61% |
| Pet Bowl Sprite | SENSE+SEE | £22 | £5 | £3 | £30 | £59-89 | 49-66% |
| 3D Printer Sprite | SENSE+SEE | £22 | £5 | £3 | £30 | £59-99 | 49-70% |
| Camera Familiar | SEE | £12 | £5 | £3 | £20 | £39-59 | 49-66% |
| Friendship Spirits | ACT×2 | £24 | £6 | £4 | £34 | £79-119/pair | 57-71% |

**Best margins:** Desk Familiar (75%), Guitar Guardian (70%), Mood Mushroom (72%)
**Worst margins:** Bookworm (-33% at £15) — too cheap for assembly cost
**Sweet spot:** £39-69 products with 50-70% margin
