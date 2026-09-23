# Corrected Glimlings V1 Specification

## One Guardian, Multiple Appearances, Expandable Abilities

**Electronic core:** M5Stack Atom Voice C008-C
**First plant sensor:** Seeed XIAO Soil Moisture Sensor 114993632
**Manufacturing:** Elecrow sources hardware, prints shells, installs firmware, tests, packs
**Software:** POW's garden assistant receives data, maintains plant histories, exposes agent tools
**Customisation:** Mushroom, cat-inspired, frog, ghost — same mechanical interface

---

## Hardware Pricing

| Component | Published Price | Use |
|-----------|-----------------|-----|
| M5Stack Atom Voice | $13.50 | Core for every talking character |
| Seeed XIAO Soil Sensor | $10.90 | One per plant |
| M5Stack ENV III | $5.95 | Temperature, humidity, pressure |
| M5Stack DLight | £5.50 | Ambient light |
| M5Stack PIR | $5.50 | Motion-triggered interactions |
| M5Stack Watering Unit | $11.50 | Future pump prototype |

**Retail component total: $24.40 before shell, battery, cable, printing, assembly, testing, packaging, delivery, taxes.**

---

## What Each Character Can Actually Do

| Character | V1 Abilities | Additional Hardware |
|-----------|--------------|---------------------|
| Sporebert | Glowing mushroom, voice, named plants, moisture alerts | Seeed moisture sensor |
| Boo Bloom | Glowing ghost, voice, quiet-night lighting | PIR for movement; optional light sensor |
| Nimbus | Cloud with spoken environmental summaries | ENV III and DLight; separate UV sensor |
| Rootkin | Tree spirit managing collection of named plants | Soil sensors; optional NFC reader |
| Pebble | Minimalist stone with voice and subtle lighting | Optional capacitive-touch hardware |
| Mosswick | Frog-themed indoor Guardian | Outdoor version needs weatherproof construction |

**A character's appearance doesn't imply an installed capability.**

---

## Five Corrections

1. **Seeed XIAO is WiFi, not BLE** — Uses 2.4 GHz Wi-Fi, factory firmware for ESPHome/Home Assistant
2. **Starter measures moisture only** — Light and temperature need separate sensors
3. **Not all six characters have identical hardware** — Motion, NFC, touch need additional hardware
4. **Indoor/outdoor distinction matters** — Atom Voice isn't waterproof; outdoor Mosswick needs sealed construction
5. **Software connection needs implementation** — POW must test its own easy onboarding

---

## The One-Box Process (Proposed)

| Step | Who |
|------|-----|
| Design shell | POW |
| Print shell | Elecrow |
| Source M5Stack + Seeed | Elecrow |
| Assemble shell + electronics | Elecrow |
| Flash firmware | Elecrow |
| Test functionality | Elecrow |
| Pack with adoption card | Elecrow |
| Ship to customer | Elecrow |

**Until Elecrow confirms this exact workflow, it remains proposed.**

---

## The First Order to Elecrow

**Just one Guardian design + one sensor + two hardware SKUs.**

Ask for:
- Source exact M5Stack Atom Voice C008-C
- Source Seeed XIAO Soil Sensor 114993632
- Print one custom shell
- Install POW firmware
- Confirm defined functional test
- Deliver finished kit in one box

**Don't quote all six characters before core experience works.**

---

## The Outstanding Proof

> One real M5Stack receiving readings from one real Seeed sensor without requiring the customer to install Home Assistant, inside one beautifully designed, ready-to-use Glimling.

**That's the milestone. Everything else follows.**
