# Sensor Comparison & MCP Integration

## 1. Sensor Comparison: My Findings vs Document

### Soil Moisture Sensors

| Sensor | My Finding | Document Reference | Price | Winner |
|--------|------------|-------------------|-------|--------|
| Capacitive v1.2 | AliExpress £0.50 | Not mentioned | £0.50 | **Cheapest** |
| Capacitive v2.0 | AliExpress £1.50 | Not mentioned | £1.50 | Better accuracy |
| Capacitive IP65 | AliExpress £2.50 | Not mentioned | £2.50 | Waterproof |
| Ecowitt WH51 | Not found | $17.99 | £14.50 | **Proven** |
| Ecowitt WH52 | Not found | $27.99 | £22.50 | **Best (3-in-1)** |
| DFRobot SEN0193 | Not found | $5.90 | £4.75 | Indoor only |
| DFRobot SEN0308 | Not found | $14.90 | £12.00 | IP65 outdoor |

**Verdict:** My AliExpress sensors are cheaper (£0.50-2.50) but unproven. Ecowitt sensors are more expensive (£14-23) but proven and waterproof.

### Temperature/Humidity

| Sensor | My Finding | Document Reference | Price | Winner |
|--------|------------|-------------------|-------|--------|
| DHT22 | AliExpress £1.50 | Not mentioned | £1.50 | **Cheapest** |
| BME280 | AliExpress £2.50 | Mentioned (recommended) | £2.50 | **Better** |
| DS18B20 | Not found | DFRobot $6.90 | £5.55 | Waterproof probe |

**Verdict:** BME280 is better than BMP280 (adds humidity). DS18B20 for waterproof soil temp.

### Light/UV

| Sensor | My Finding | Document Reference | Price | Winner |
|--------|------------|-------------------|-------|--------|
| BH1750 | AliExpress £1.00 | Not mentioned | £1.00 | **Cheapest** |
| VEML6075 | AliExpress £3.00 | Not mentioned | £3.00 | UV index |
| TSL2591 | Not found | Not mentioned | £5-10 | Light spectrum |

### Water/Rain

| Sensor | My Finding | Document Reference | Price | Winner |
|--------|------------|-------------------|-------|--------|
| Rain sensor | AliExpress £2.00 | DFRobot $29.90 | £24.00 | **Cheapest** |
| Ecowitt WN20 | Not found | $19.99 | £16.00 | **Proven** |
| Water level | AliExpress £2.00 | Seeed $7.99 | £6.45 | **Cheapest** |
| Leak detector | AliExpress £1.00 | Seeed $3.20 | £2.60 | **Cheapest** |

### Specialist

| Sensor | My Finding | Document Reference | Price | Winner |
|--------|------------|-------------------|-------|--------|
| pH sensor | Not found | DFRobot $39.50-99 | £32-80 | Expensive |
| EC sensor | Not found | DFRobot $69.90 | £56 | Expensive |
| Load cell | AliExpress £2-5 | Seeed $4.30 | £3.50 | **Cheapest** |

---

## 2. Can We Put Our Own Logos?

### YES — Multiple Options

| Method | MOQ | Cost per Unit | Quality | Best For |
|--------|-----|---------------|---------|----------|
| **PCB Silkscreen** | 1 (JLCPCB) | £0.00 | Good | Logo on circuit board |
| **Laser Engraving** | 1 (JLC3DP) | £0.50-1.00 | Excellent | Logo on enclosure |
| **UV Printing** | 1 (JLC3DP) | £1.00-2.00 | Excellent | Full colour on enclosure |
| **Sticker/Label** | 100+ | £0.10-0.20 | Good | Quick branding |
| **Custom PCB (OEM)** | 1000+ | £0.50-1.00 | Excellent | Full custom board |

### Recommended for Glimlings

**Enclosure:** Laser engraving or UV printing on JLC3DP
- Add POW logo to every enclosure
- Add character name/ID
- Add QR code for pairing
- Cost: £0.50-1.00 per unit

**PCB:** Silkscreen on JLCPCB
- Add POW logo to PCB
- Add version number
- Add serial number
- Cost: £0.00 (included in PCB price)

---

## 3. Can We Hook Them Up to Local MCP Network?

### YES — Multiple Integration Paths

#### Option A: Ecowitt Gateway (Recommended for Start)

```
Ecowitt Sensors → Ecowitt Gateway (WiFi) → Local HTTP API → Glimling Hub → MCP
```

**How it works:**
1. Ecowitt sensors connect to Ecowitt gateway via 915MHz/868MHz
2. Gateway exposes local HTTP API (documented)
3. Glimling hub polls gateway via HTTP
4. Data exposed via MCP to Muse/ChatGPT

**Existing integrations:**
- Home Assistant official integration
- ha-ecowitt-iot (local HTTP polling)
- ha-ecowitt-online-api (cloud API)

**Advantages:**
- Already works
- Proven reliability
- 16 sensors supported
- No custom firmware needed

**Disadvantages:**
- Additional gateway hardware
- Proprietary radio protocol
- Can't customise sensors

#### Option B: ESP-NOW Direct (Custom Sensors)

```
ESP32-C3 Sensors → ESP-NOW → Glimling Hub → MCP
```

**How it works:**
1. Custom ESP32-C3 sensors broadcast via ESP-NOW
2. Glimling hub receives broadcasts
3. Data exposed via MCP

**Advantages:**
- No gateway needed
- Full customisation
- Cheaper per sensor
- Can add our branding

**Disadvantages:**
- Need custom firmware
- Range limitations (10-100m)
- Power management complexity

#### Option C: Zigbee (via Coordinator)

```
Zigbee Sensors → Zigbee Coordinator → Glimling Hub → MCP
```

**How it works:**
1. Zigbee sensors connect to coordinator
2. Coordinator exposes data via serial/USB
3. Glimling hub reads coordinator
4. Data exposed via MCP

**Advantages:**
- Existing ecosystem (THIRDREALITY, etc.)
- Mesh networking
- Low power

**Disadvantages:**
- Need Zigbee coordinator hardware
- More complex setup
- Proprietary protocols

---

## 4. Recommended Integration Stack

### For Christmas 2026 (Quick Win)

```
Ecowitt WH51 sensors (£14-18 each)
    ↓
Ecowitt GW1200 gateway (£50-80)
    ↓
Local HTTP API
    ↓
Glimling Hub (ESP32-S3)
    ↓
MCP Server
    ↓
Muse/ChatGPT
```

**Total cost:** £14-18 per sensor + £50-80 gateway
**Time to market:** 2-3 weeks
**Risk:** Low (proven hardware)

### For Post-Christmas (Custom Sensors)

```
ESP32-C3 sensors (£5-10 each)
    ↓
ESP-NOW radio
    ↓
Glimling Hub (ESP32-S3)
    ↓
MCP Server
    ↓
Muse/ChatGPT
```

**Total cost:** £5-10 per sensor
**Time to market:** 4-6 weeks
**Risk:** Medium (need custom firmware)

### For Production (Full Custom)

```
Custom PCB sensors with POW branding
    ↓
Custom radio protocol
    ↓
Glimling Hub (ESP32-S3)
    ↓
MCP Server
    ↓
Muse/ChatGPT
```

**Total cost:** £3-7 per sensor (at volume)
**Time to market:** 8-12 weeks
**Risk:** High (need full development)

---

## 5. The Answer

### Can we put logos on sensors?

**YES:**
- PCB silkscreen: £0.00 (JLCPCB)
- Laser engraving: £0.50-1.00 (JLC3DP)
- UV printing: £1.00-2.00 (JLC3DP)
- Stickers: £0.10-0.20 (100+ MOQ)

### Can we hook them up to local MCP?

**YES:**
- **Ecowitt gateway** → Local HTTP API → Glimling Hub → MCP (easiest)
- **ESP-NOW direct** → Glimling Hub → MCP (cheapest)
- **Zigbee coordinator** → Glimling Hub → MCP (most compatible)

### Recommended Path

1. **Christmas 2026:** Use Ecowitt sensors (proven, quick)
2. **Post-Christmas:** Develop custom ESP32-C3 sensors
3. **Production:** Full custom with POW branding

**The moat is the software layer, not the hardware.**
