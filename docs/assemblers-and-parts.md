# Assemblers, Parts & Suppliers Review

## Current Assemblers (8 partners)

| # | Name | Location | MOQ | Services | Best For |
|---|------|----------|-----|----------|----------|
| 1 | **LCSC** | China | 1 piece | Components | Sourcing parts |
| 2 | **JLCPCB** | China | 2 boards | PCB + SMT + firmware flash | PCB assembly |
| 3 | **Seeed Fusion** | China | 1 kit | Full turnkey (PCB + assembly + firmware + packaging) | Production runs |
| 4 | **JLC3DP** | China | 1 piece | 3D printing (SLA/MJF/FDM/SLS) | Enclosures |
| 5 | **UK Electronics** | Hampshire, UK | 10+ units | Full box build (SMT + wiring + test + packaging) | UK production |
| 6 | **M-TEK Assembly** | Reading, UK | Small batches | SMT + PTH + BGA + test + programming | Small batch UK |
| 7 | **Prism Electronics** | UK | Prototypes | PCB assembly + test + rework + design | Prototyping |
| 8 | **esp32s.com** | China | 5+ units | ESP32 custom boards + firmware + test | ESP32 specialist |

### Assembly Pipeline

```
Components (LCSC/Mouser/Farnell)
    ↓
PCB Assembly (JLCPCB - min 2 boards)
    ↓
Enclosure (JLC3DP - 1 piece min)
    ↓
Box Build (UK Electronics/M-TEK/Prism)
    ↓
Testing (included in box build)
    ↓
Packaging (branded box + instructions)
    ↓
Shipping (Royal Mail £3.50)
```

### Cost Summary (per unit at 10 units)

| Component | Cost |
|-----------|------|
| ESP32-S3 DevKit | £5.50 |
| Sensors (3-4 per kit) | £5-8 |
| LEDs/Display | £3-5 |
| Enclosure (JLC3DP) | £1-3 |
| PCB (JLCPCB) | £2-4 |
| Assembly (UK Electronics) | £5-10 |
| Packaging | £2-3 |
| **Total COGS** | **£25-40** |

---

## Components by Category

### Core Electronics (for Glimlings engines)

| Category | Components | With Price | Missing Price |
|----------|-----------|------------|---------------|
| **microcontroller** | 2 | ESP32-S3 (£5.50) | POW Agent Node |
| **sensor** | 17 | 16 (94%) | 1 (MPU-6050) |
| **led** | 4 | 4 (100%) | - |
| **audio** | 5 | 3 (60%) | INMP441, 3W Speaker |
| **camera** | 4 | 2 (50%) | OV2640, Basler, Cognex |
| **display** | 3 | 2 (67%) | Waveshare 7" |
| **relay** | 3 | 3 (100%) | - |
| **power_management** | 5 | 5 (100%) | - |
| **battery** | 13 | 11 (85%) | 14.4V, 14.8V, 25V |
| **enclosure** | 5 | 4 (80%) | Companion |
| **connector** | 4 | 3 (75%) | - |

### Robot Components (for repair/replacement)

| Category | Components | With Price | Missing Price |
|----------|-----------|------------|---------------|
| **servo_motor** | 8 | 6 (75%) | ABB, KUKA, Siemens, Yaskawa |
| **brush** | 15 | 8 (53%) | Many robot brushes |
| **filter** | 8 | 6 (75%) | 2 filters |
| **battery** | 13 | 11 (85%) | 3 robot batteries |
| **motor** | 6 | 4 (67%) | 2 motors |
| **wheel** | 3 | 1 (33%) | 2 wheels |

---

## Pricing Coverage

### By Supplier

| Supplier | Parts | Price Range | Avg Price |
|----------|-------|-------------|-----------|
| **Alibaba** | 52 | £0.20 - £14.39 | £3.82 |
| **Amazon UK** | 39 | £3.50 - £159.95 | £23.65 |
| **Husqvarna UK** | 11 | £5.54 - £217.90 | £91.86 |
| **Taobao** | 6 | £3.10 - £178.00 | £55.12 |
| **eBay UK** | 1 | £25.00 | £25.00 |
| **Feetech** | 1 | £16.38 | £16.38 |
| **PartaBot** | 1 | £189.00 | £189.00 |
| **Seeed Studio** | 1 | £189-299 | £244.00 |

### Key Components with Multiple Prices

| Component | Alibaba | Amazon UK | Best Price |
|-----------|---------|-----------|------------|
| ESP32-S3 DevKit | £5.50 | £8.99 | Alibaba |
| WS2812B RGB LED | £0.30 | - | Alibaba |
| Capacitive Soil Moisture | £1.20 | - | Alibaba |
| DHT22 Sensor | £2.00 | - | Alibaba |
| MAX98357 Speaker Amp | £2.50 | £5.99 | Alibaba |
| USB-C Breakout | £0.80 | - | Alibaba |
| 5V Relay Module | £1.00 | - | Alibaba |
| ESP32-CAM Module | £7.50 | £12.99 | Alibaba |
| SSD1306 OLED 0.96" | £3.00 | - | Alibaba |
| HC-SR04 Ultrasonic | £1.00 | - | Alibaba |
| SG90 Micro Servo | - | - | Need price |
| Feetech STS3215 | £11.18 | - | Alibaba |

---

## Kit/Engine Definitions

### Available Kits (10 total)

| Kit | Type | Components | Price |
|-----|------|------------|-------|
| **Plant Agent** | Build | ESP32-S3, sensors, LED, relay, enclosure | £25.10 |
| **Desk Agent** | Build | ESP32-S3, OLED, buzzer, LED, enclosure | £15.30 |
| **Pet Agent** | Build | ESP32-S3, camera, mic, speaker, relay | £21.30 |
| **Lamp Agent** | Build | ESP32-S3, LED strip, buck converter | £16.30 |
| **Speaker Agent** | Build | ESP32-S3, speaker amp, mic, LED ring | £17.80 |
| **Camera Agent** | Build | ESP32-S3, camera, OLED, servos | £20.30 |
| **Robot Agent** | Build | ESP32-S3, motors, battery, ultrasonic, servo | £17.00 |
| **SO-101 Build** | Build | Feetech servos, controller, cables | £229.88 |
| **SO-101 Maintenance** | Maintenance | Servos, cables | £38.27 |

### Kit Components Breakdown

**Plant Agent Kit** (£25.10):
- ESP32-S3 DevKit (1x)
- Capacitive Soil Moisture Sensor (1x)
- BH1750 Light Sensor (1x)
- DHT22 Temp/Humidity Sensor (1x)
- WS2812B RGB LED (1x)
- 5V Relay Module (1x)
- USB-C Breakout Board (1x)
- Jumper Wire Set (1x)

**Desk Agent Kit** (£15.30):
- ESP32-S3 DevKit (1x)
- SSD1306 OLED Display 0.96" (1x)
- Active Buzzer 5V (1x)
- WS2812B RGB LED (1x)
- USB-C Breakout Board (1x)
- Jumper Wire Set (1x)

**Pet Agent Kit** (£21.30):
- ESP32-S3 DevKit (1x)
- ESP32-CAM Module (1x)
- MAX9814 Electret Microphone (1x)
- MAX98357 I2S Speaker Amp (1x)
- 5V Relay Module (1x)
- USB-C Breakout Board (1x)
- Jumper Wire Set (1x)

---

## Missing Components (Need to Source)

### For Glimlings Engines

| Component | Engine | Needed For | Est. Price |
|-----------|--------|------------|------------|
| MPU-6050 IMU | COMPANION | Fall detection | £1.50-2.50 |
| INMP441 Mic | COMPANION | Voice input | £2.00-3.00 |
| PN532 NFC | COMPANION | Medication tracking | £3.00-5.00 |
| NEO-6M GPS | COMPANION | Location sharing | £8.00-12.00 |
| OV2640 Camera | COMPANION/SEE | Video calls | £5.00-8.00 |
| 7" Touchscreen | COMPANION | Display | £25.00-35.00 |
| 18650 Battery | COMPANION | Backup power | £4.00-6.00 |
| SG90 Micro Servo | ACT | Movement | £1.00-2.00 |

### For Robot Repair

| Component | Robot Type | Needed For | Est. Price |
|-----------|------------|------------|------------|
| ABB Servo Motor | Industrial | Replacement | £500-2000 |
| KUKA Servo Module | Industrial | Replacement | £800-3000 |
| Siemens Servo | Industrial | Replacement | £600-2500 |
| Yaskawa Servo | Industrial | Replacement | £400-1500 |

---

## How to Find More Assemblers

### UK Assemblers

| Search Term | Where to Look |
|-------------| Google, LinkedIn, industry directories |
| "electronic contract manufacturing UK" | ACM, Kitron, Vario |
| "PCB assembly UK" | Newbury Electronics, PCD |
| "box build assembly UK" | Intec, Synergiser |
| "electronics prototyping UK" | Sprint PCB, Eurocircuits |

### China Assemblers

| Search Term | Where to Look |
|-------------| Alibaba, Made-in-China |
| "PCB assembly China" | JLCPCB, PCBWay, AllPCB |
| "3D printing China" | JLC3DP, Hubs, Xometry |
| "ESP32 manufacturing" | esp32s.com, Waveshare, Seeed |

### Specialist Assemblers

| Speciality | Examples |
|------------|----------|
| **ESP32 boards** | esp32s.com, Waveshare, Seeed |
| **IoT devices** | Particle, Heltec, TTGO |
| **Wearable electronics** | Adafruit, SparkFun |
| **Robotics** | Feetech, Dynamixel, RobotShop |

### Directories

| Directory | URL | Focus |
|-----------|-----|-------|
| UK Electronics Association | ukelectronics.org | UK members |
| IPC Members | ipc.org | Global certified |
| Farnell/element14 | farnell.com | Supplier network |
| RS Components | rs-online.com | UK distributor |
| Digi-Key | digikey.com | Global distributor |

### How to Evaluate

1. **Check certifications** - ISO 9001, IPC-A-610, IPC Class 2/3
2. **Request quotes** - Get 3 quotes for same BOM
3. **Order samples** - Test with 5-10 units first
4. **Check lead times** - Prototype vs production
5. **Verify MOQ** - Some need 10+, some do 1
6. **Ask about test** - Functional test included?
7. **Check shipping** - UK vs China, customs, VAT

---

## Recommendations

### For Prototyping (1-5 units)
1. **Components**: Alibaba (cheapest)
2. **PCB**: JLCPCB (min 2 boards)
3. **Enclosure**: JLC3DP (1 piece min)
4. **Assembly**: Manual or Prism Electronics
5. **Total**: £25-40 per unit

### For Small Batch (10-50 units)
1. **Components**: LCSC (MOQ 1, good prices)
2. **PCB**: JLCPCB (50 boards)
3. **Enclosure**: JLC3DP (50 units)
4. **Assembly**: UK Electronics or M-TEK
5. **Total**: £20-35 per unit

### For Production (50+ units)
1. **Full turnkey**: Seeed Fusion ODM
2. **Or**: JLCPCB + JLC3DP + UK Electronics
3. **Total**: £15-30 per unit

### For ESP32-Specific
1. **esp32s.com** - ESP32 specialist, 5+ units
2. **Waveshare** - ESP32 boards + displays
3. **Seeed** - Full turnkey ESP32 solutions

---

## Next Steps

1. **Get quotes from UK Electronics** - Box build for Plant Agent kit
2. **Get quotes from M-TEK** - Small batch assembly
3. **Order samples from JLCPCB** - Test PCB quality
4. **Order samples from JLC3DP** - Test enclosure quality
5. **Build first prototype** - Plant Agent or Desk Agent
6. **Test with real sensors** - Validate readings
7. **Document assembly process** - Time, steps, tools needed
8. **Create test fixture** - Bed-of-nails for production testing

---

**Bottom line:** We have 8 assembly partners covering the full pipeline from components to shipped product. The main gap is UK-based box build (10+ unit MOQ) and ESP32-specific manufacturing. For prototyping, use Alibaba + JLCPCB + JLC3DP + manual assembly. For production, use Seeed Fusion ODM or JLCPCB + UK Electronics.
