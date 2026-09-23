# Engine → Supplier Stack → Pricing → Lead Time → Who Assembles

## Summary Table

| Engine | Cost | Landed | Total Lead | Assembler |
|--------|------|--------|------------|-----------|
| **SENSE** | £37.10 | £49.10 | 10-16 days | Makerfabs (China direct) |
| **REMEMBER** | £30.10 | £42.10 | 10-16 days | Makerfabs (China direct) |
| **ACT** | £40.30 | £52.30 | 10-16 days | Makerfabs (China direct) |
| **TALK** | £44.00 | £56.00 | 10-16 days | Makerfabs (China direct) |
| **SEE** | £32.99 | £44.99 | 10-16 days | Makerfabs (China direct) |
| **COMPANION** | £100.80 | £112.80 | 15-29 days | Makerfabs/PCBWay (integrated) |

---

## SENSE Engine

**Board Family:** SENSE/REMEMBER/ACT (shared)
**Products:** Mosswick, Sporebert, Boo Bloom, Nimbus, Chroma

### Components

| Part | Supplier | Cost |
|------|----------|------|
| ESP32-S3 DevKit | LCSC/Alibaba | £5.50 |
| BH1750 Light Sensor | LCSC/Alibaba | £1.50 |
| DHT22 Temp/Humidity | LCSC/Alibaba | £2.00 |
| WS2812B RGB LED | LCSC/Alibaba | £0.30 |
| USB-C Breakout | LCSC/Alibaba | £0.80 |
| **Parts total** | | **£10.10** |

### Supply Chain

| Stage | Supplier | Cost | Lead Time |
|-------|----------|------|-----------|
| PCB assembly | JLCPCB | £10.00 | 3-5 days |
| Enclosure | JLC3DP | £2.00 | 2-4 days |
| Final assembly | Makerfabs | £15.00 | 5-7 days |
| Shipping | China → UK | £12.00 | 5-7 days |
| **Total** | | **£49.10** | **15-23 days** |

---

## REMEMBER Engine

**Board Family:** SENSE/REMEMBER/ACT (shared)
**Products:** Wormington, Keys Goblin

### Components

| Part | Supplier | Cost |
|------|----------|------|
| ESP32-S3 DevKit | LCSC/Alibaba | £5.50 |
| DS3231 RTC (optional) | LCSC/Alibaba | £1.50 |
| WS2812B RGB LED | LCSC/Alibaba | £0.30 |
| USB-C Breakout | LCSC/Alibaba | £0.80 |
| **Parts total** | | **£8.10** |

### Supply Chain

| Stage | Supplier | Cost | Lead Time |
|-------|----------|------|-----------|
| PCB assembly | JLCPCB | £8.00 | 3-5 days |
| Enclosure | JLC3DP | £2.00 | 2-4 days |
| Final assembly | Makerfabs | £12.00 | 5-7 days |
| Shipping | China → UK | £12.00 | 5-7 days |
| **Total** | | **£42.10** | **15-23 days** |

---

## ACT Engine

**Board Family:** ACT/DISPLAY
**Products:** Puck, Mab (Desk)

### Components

| Part | Supplier | Cost |
|------|----------|------|
| ESP32-S3 DevKit | LCSC/Alibaba | £5.50 |
| SSD1306 OLED 0.96" | LCSC/Alibaba | £3.00 |
| Rotary Encoder | LCSC/Alibaba | £1.50 |
| Active Buzzer 5V | LCSC/Alibaba | £0.20 |
| WS2812B RGB LED | LCSC/Alibaba | £0.30 |
| USB-C Breakout | LCSC/Alibaba | £0.80 |
| **Parts total** | | **£11.30** |

### Supply Chain

| Stage | Supplier | Cost | Lead Time |
|-------|----------|------|-----------|
| PCB assembly | JLCPCB | £12.00 | 3-5 days |
| Enclosure | JLC3DP | £2.00 | 2-4 days |
| Final assembly | Makerfabs | £15.00 | 5-7 days |
| Shipping | China → UK | £12.00 | 5-7 days |
| **Total** | | **£52.30** | **15-23 days** |

---

## TALK Engine

**Board Family:** TALK
**Products:** Postie, Mab (Sleep)

### Components

| Part | Supplier | Cost |
|------|----------|------|
| ESP32-S3 DevKit | LCSC/Alibaba | £5.50 |
| MAX98357 Speaker Amp | LCSC/Alibaba | £2.50 |
| INMP441 MEMS Mic | LCSC/Alibaba | £2.00 |
| Push Button | LCSC/Alibaba | £0.20 |
| USB-C Breakout | LCSC/Alibaba | £0.80 |
| **Parts total** | | **£11.00** |

### Supply Chain

| Stage | Supplier | Cost | Lead Time |
|-------|----------|------|-----------|
| PCB assembly | JLCPCB | £12.00 | 3-5 days |
| Enclosure | JLC3DP | £3.00 | 2-4 days |
| Final assembly | Makerfabs | £18.00 | 5-7 days |
| Shipping | China → UK | £12.00 | 5-7 days |
| **Total** | | **£56.00** | **15-23 days** |

---

## SEE Engine

**Board Family:** SEE (camera module)
**Products:** Pickles, Camera Agent, Pet Agent

### Components

| Part | Supplier | Cost |
|------|----------|------|
| Seeed XIAO ESP32-S3 Sense | Seeed | £13.99 |
| USB-C Cable | Alibaba | £1.00 |
| **Parts total** | | **£14.99** |

### Supply Chain

| Stage | Supplier | Cost | Lead Time |
|-------|----------|------|-----------|
| PCB | Seeed (pre-made) | £0.00 | 3-5 days |
| Enclosure | JLC3DP | £3.00 | 2-4 days |
| Final assembly | Makerfabs | £15.00 | 5-7 days |
| Shipping | China → UK | £12.00 | 5-7 days |
| **Total** | | **£44.99** | **10-16 days** |

---

## COMPANION Engine

**Board Family:** COMPANION (dedicated)
**Products:** Elderly Companion

### Components

| Part | Supplier | Cost |
|------|----------|------|
| ESP32-S3 DevKit | LCSC/Alibaba | £5.50 |
| Waveshare 7" Touchscreen | Waveshare | £25.00 |
| MAX98357 Speaker Amp | LCSC/Alibaba | £2.50 |
| INMP441 MEMS Mic | LCSC/Alibaba | £2.00 |
| OV2640 Camera | LCSC/Alibaba | £5.00 |
| USB-C Breakout | LCSC/Alibaba | £0.80 |
| **Parts total** | | **£40.80** |

### Supply Chain

| Stage | Supplier | Cost | Lead Time |
|-------|----------|------|-----------|
| PCB assembly | Seeed Fusion/PCBWay | £25.00 | 5-10 days |
| Enclosure | JLC3DP | £5.00 | 3-5 days |
| Final assembly | Makerfabs/PCBWay | £30.00 | 7-14 days |
| Shipping | China → UK | £12.00 | 5-7 days |
| **Total** | | **£112.80** | **20-36 days** |

---

## The Logic

**Yes, each engine has a different supplier stack** based on:

1. **Component complexity** — More components = more assembly time
2. **Specialist parts** — Camera, touchscreen, speaker need different handling
3. **Assembly difficulty** — Simple snap-in vs complex wiring
4. **Volume** — Some engines share board families, reducing cost

### Board Family Sharing

| Board Family | Engines | Why Shared |
|--------------|---------|------------|
| SENSE/REMEMBER/ACT | SENSE, REMEMBER, ACT | Same ESP32-S3 base, different components populated |
| TALK | TALK | Needs speaker amp + mic, different layout |
| SEE | SEE | Pre-made camera module, no custom PCB |
| COMPANION | COMPANION | Dedicated touchscreen + camera, complex |

### Pricing Logic

| Engine | Landed Cost | Retail Price | Margin |
|--------|-------------|--------------|--------|
| SENSE | £49.10 | £59.99 | 18% |
| REMEMBER | £42.10 | £49.99 | 16% |
| ACT | £52.30 | £59.99 | 13% |
| TALK | £56.00 | £69.99 | 20% |
| SEE | £44.99 | £59.99 | 25% |
| COMPANION | £112.80 | £149.99 | 25% |

**Note:** These are estimated margins. Real margins depend on actual supplier quotes, volume discounts, and Etsy fees (~11%).

### Lead Time Logic

| Engine | Total Lead | Why |
|--------|------------|-----|
| SENSE/REMEMBER/ACT | 15-23 days | Standard components, standard assembly |
| TALK | 15-23 days | Speaker + mic need careful assembly |
| SEE | 10-16 days | Pre-made camera module, less assembly |
| COMPANION | 20-36 days | Complex, touchscreen + camera, more testing |

### Who Assembles

| Engine | Assembler | Why |
|--------|-----------|-----|
| SENSE/REMEMBER/ACT | Makerfabs | Simple assembly, standard components |
| TALK | Makerfabs | Speaker + mic need careful handling |
| SEE | Makerfabs | Camera module needs alignment |
| COMPANION | Makerfabs/PCBWay | Complex, needs integrated factory |

---

## Next Steps

1. **Contact Makerfabs** — Get actual quotes for each engine
2. **Verify lead times** — Confirm 15-23 days is realistic
3. **Test assembly** — Build 1 prototype of each engine
4. **Update costs** — Replace estimates with real quotes
5. **Set retail prices** — Based on actual margins

**The milestone: One working Desk Goblin (ACT engine) delivered to a UK address.**
