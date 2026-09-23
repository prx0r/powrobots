# Canonical Product Stack — Final

## The One-Box Gift

**One personalised shell + one voice module + one plant sensor. Packed together. Ready to gift.**

---

## The Two Starter Products

### 1. Sporebert Indoor (Christmas Gift)

| Item | Source | Price | Notes |
|------|--------|-------|-------|
| Custom shell | JLC3DP (our design) | £3-5 | POW branding |
| M5Stack Atom Voice | The Pi Hut | £13.00 | C008-C, in stock |
| Seeed XIAO Soil Sensor | Seeed direct | $10.90 (£8.70) | SKU 114993632 |
| USB-C cable | Included | £0.50 | |
| Adoption card | Printed | £0.20 | |
| Gift packaging | Elecrow/Custom | £1.00 | |
| **Total cost** | | **£23.40-25.40** | |
| **Retail** | | **£49.99** | |
| **Margin** | | **49-53%** | |

### 2. Mosswick Outdoor (Garden Bundle)

| Item | Source | Price | Notes |
|------|--------|-------|-------|
| Custom shell | JLC3DP (our design) | £3-5 | POW branding, IP65 |
| M5Stack Atom Voice | The Pi Hut | £13.00 | C008-C |
| Seeed XIAO Soil Sensor | Seeed direct | $10.90 (£8.70) | SKU 114993632 |
| USB-C cable | Included | £0.50 | |
| Adoption card | Printed | £0.20 | |
| Gift packaging | Elecrow/Custom | £1.00 | |
| **Total cost** | | **£23.40-25.40** | |
| **Retail** | | **£59.99** | |
| **Margin** | | **58-61%** | |

---

## Expansion Sensors

### Budget (DIY, No Soldering)

| Sensor | Source | Price | Connection |
|--------|--------|-------|------------|
| ESP32-C3 SuperMini | AliExpress | £1.20 | Pre-soldered |
| Capacitive Soil Moisture v1.2 | AliExpress | £0.40 | Pre-soldered + wire |
| DHT22 Module | AliExpress | £1.00 | Pre-soldered |
| Jumper Wires | AliExpress | £0.30 | Plug and play |
| **Total** | | **£2.90** | |

### Premium (Plug-and-Play)

| Sensor | Source | Price | Connection |
|--------|--------|-------|------------|
| Seeed XIAO Soil Sensor | Seeed direct | $10.90 | Wireless (BLE) |
| HHCC Flower Care | AliExpress | $22.93 | Wireless (BLE) |
| M5Stack PIR Unit | M5Stack | $5.50 | Grove cable |
| M5Stack ENV III | M5Stack | $5.95 | Grove cable |

---

## The Complete Product Line

| Product | Contents | Retail | Margin |
|---------|----------|--------|--------|
| **Shell Only** | Character shell | £24.99 | 75-85% |
| **Shell + Voice** | Shell + M5Stack | £39.99 | 49-55% |
| **Sporebert Starter** | Shell + Voice + Seeed Sensor | £49.99 | 49-53% |
| **Mosswick Starter** | Shell + Voice + Seeed Sensor (IP65) | £59.99 | 58-61% |
| **Expansion Sensor** | Seeed XIAO (wireless) | £14.99 | 42% |
| **Budget Sensor Kit** | ESP32 + probes (DIY) | £9.99 | 71% |

---

## The Key Finding

**AliExpress isn't automatically cheaper.**

| Product | AliExpress | Direct | Winner |
|---------|------------|--------|--------|
| M5Stack Atom Voice | $22.44 | $13.50 (M5Stack) | **Direct** |
| HHCC Flower Care | $22.93 | ~$15 (varies) | **Direct** |
| Seeed XIAO Sensor | $25.86 | $10.90 (Seeed) | **Direct** |
| Capacitive v1.2 | $0.80 | $0.40 (AliExpress) | **AliExpress** |

**Compare same SKU across AliExpress, manufacturer-direct and regional distributors.**

---

## The Cheapest Wireless Sensor

**Seeed XIAO Soil Sensor — $10.90 direct from Seeed**

- SKU: 114993632
- Runs on 1 AA battery
- BLE connectivity
- ESPHome/Home Assistant support
- IP54 rated
- **This is the sensor to use.**

---

## The First Purchasing Basket

| Item | Source | Price |
|------|--------|-------|
| M5Stack Atom Voice C008-C | The Pi Hut | £13.00 |
| Seeed XIAO Soil Sensor | Seeed direct | $10.90 (£8.70) |
| PIR Motion Sensor (optional) | M5Stack U004 | $5.50 (£4.40) |
| **Total** | | **£21.70-26.10** |

**Everything works together. No wiring needed.**

---

## Branding Strategy

| What | Branding | Who |
|------|----------|-----|
| Shell | POW logo (laser engraved) | Us |
| Electronics | Original manufacturer | M5Stack/Seeed |
| Packaging | POW branded | Us |
| App | Glimlings | Us |
| Compatibility | "Glimling Compatible" badge | Us |

**Keep original manufacturer identity on electronics. Our branding on character, packaging, app.**

---

## The Canonical Stack

```
HUB (Glimling):
  - M5Stack Atom Voice C008-C
  - Custom shell (POW branded)
  - Firmware
  - MCP server

SENSORS:
  - Seeed XIAO Soil Sensor (wireless, BLE)
  - M5Stack PIR Unit (optional)
  - M5Stack ENV III (optional)

FULFILMENT:
  - Elecrow or CJdropshipping
  - Custom packaging
  - Direct to customer

SOFTWARE:
  - Glimlings app
  - Plant registry
  - MCP integration
  - AI assistant
```

**This is the canonical stack. Tested, priced, sourced.**
