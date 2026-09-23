# Existing Sensors — We Don't Need Custom

## The Insight

**We don't need to design custom sensors. Off-the-shelf sensors already exist. We just need to CONNECT them to our Glimling hub.**

This is MUCH cheaper and faster than custom development.

---

## Off-the-Shelf Options

### THIRDREALITY Smart Soil Moisture Gen2 (Recommended for Indoor)

| Parameter | Value |
|-----------|-------|
| Type | Zigbee |
| Features | Soil moisture, temperature, waterproof |
| Price | £20-30 |
| Connectivity | Zigbee 3.0 |
| Battery | 1 year+ |
| Waterproof | Yes (indoor/outdoor) |
| Smart home | SmartThings, Home Assistant, Hubitat |
| Proven | Yes (tens of thousands sold) |

### b-parasite (Recommended for Budget)

| Parameter | Value |
|-----------|-------|
| Type | BLE |
| Features | Soil moisture, temperature, humidity, light |
| Price | £5-10 (DIY) |
| Connectivity | BLE |
| Battery | 2 years+ |
| Waterproof | With coating |
| Smart home | Home Assistant (BLE-MQTT bridge) |
| Proven | Yes (open source community) |

### Dragino SE02-NB (Recommended for Outdoor)

| Parameter | Value |
|-----------|-------|
| Type | NB-IoT |
| Features | Soil moisture, temperature, EC (nutrients) |
| Price | £50-80 |
| Connectivity | NB-IoT |
| Battery | 5 years+ |
| Waterproof | Yes (IP67) |
| Smart home | MQTT, custom |
| Proven | Yes (agricultural use) |

### Milesight EM500-SMT (Recommended for LoRaWAN)

| Parameter | Value |
|-----------|-------|
| Type | LoRaWAN |
| Features | Soil moisture, temperature, NFC config |
| Price | £80-120 |
| Connectivity | LoRaWAN |
| Battery | 10 years+ |
| Waterproof | Yes (IP67) |
| Smart home | LoRaWAN gateway |
| Proven | Yes (industrial use) |

### Netafim SM150T (Professional)

| Parameter | Value |
|-----------|-------|
| Type | Analog |
| Features | Soil moisture |
| Price | £40-60 |
| Connectivity | Analog (0-1V) |
| Battery | N/A (wired) |
| Waterproof | Yes (IP68) |
| Smart home | Custom ADC |
| Proven | Yes (professional agriculture) |

### Netafim WET150 (Specialist)

| Parameter | Value |
|-----------|-------|
| Type | SDI-12 |
| Features | Soil moisture, EC (nutrients), temperature |
| Price | £150-200 |
| Connectivity | SDI-12 |
| Battery | N/A (wired) |
| Waterproof | Yes (IP68) |
| Smart home | Custom SDI-12 |
| Proven | Yes (professional agriculture) |

### VODESON Multi-Zone (Consumer)

| Parameter | Value |
|-----------|-------|
| Type | Wireless |
| Features | Soil moisture (12 zones), LCD display |
| Price | £30-50 |
| Connectivity | Wireless (proprietary) |
| Battery | 1 year+ |
| Waterproof | Yes |
| Smart home | LCD display (no smart home) |
| Proven | Yes (consumer product) |

---

## The Strategy

### 1. Don't Build Custom Sensors

- Use off-the-shelf sensors
- Much cheaper
- Much faster
- Already proven

### 2. Build the Hub

- ESP32-S3
- WiFi + BLE
- MCP server
- Connects to existing sensors

### 3. Integrate Existing Sensors

| Sensor | Use For | Price |
|--------|---------|-------|
| THIRDREALITY | Indoor plants | £20-30 |
| b-parasite | Budget prototyping | £5-10 |
| Dragino SE02-NB | Outdoor plants | £50-80 |
| Netafim WET150 | Specialist/hydroponics | £150-200 |

### 4. Sell the Platform

- Hub + sensor bundles
- Sensor expansion packs
- Specialist upgrades

**This is the fastest path to market. No custom sensor development needed.**

---

## The Product Line (Updated)

### Indoor

- Sporebert Hub: £49.99
- THIRDREALITY Sensor: £20-30 (or include in bundle)
- Starter Kit (Hub + 3 sensors): £99.99
- Expansion Pack (3 sensors): £54.99

### Outdoor

- Mosswick Hub: £59.99
- Dragino SE02-NB: £50-80 (or include in bundle)
- Starter Kit (Hub + 3 sensors): £149.99
- Expansion Pack (3 sensors): £129.99

### Specialist

- Netafim WET150: £150-200
- Hydroponic Bundle: £299.99

---

## The Key Insight

**We're not a sensor company. We're a PLATFORM company.**

- Build the hub (Glimling)
- Integrate existing sensors
- Provide the AI/MCP layer
- Sell the experience

**The sensors are commoditised. The intelligence is our value.**
