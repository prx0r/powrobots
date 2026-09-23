# POW Engines — 5 Core Platforms → Infinite Products

Build 5 electronics platforms. Map them to 16+ products. MCP built from engine capabilities.

---

## The 5 engines

### Engine 1: SENSE — physical world perception

```
ESP32-S3 DevKit          £8.90
Capacitive Soil Sensor    £1.20
BH1750 Light Sensor       £1.50
DHT22 Temp/Humidity       £2.00
NFC Reader (optional)     £3.00
USB-C Cable               £1.00
                        --------
BOM total:              ~£16.60
```

**What it does:** Reads moisture, light, temperature, humidity, NFC tags.
**What it knows:** The physical state of the world around it.
**Products it powers:** Plant Sprite, Coffee Goblin, Guitar Guardian, Sourdough Familiar, Fridge Goblins, Tool Familiar, Seedling Family.

### Engine 2: REMEMBER — history and routines

```
ESP32-S3 DevKit          £8.90
DS3231 RTC Module         £1.50
MicroSD Module (optional) £2.00
USB-C Cable               £1.00
                        --------
BOM total:              ~£13.40
```

**What it does:** Keeps time, tracks events, stores history locally.
**What it knows:** When things happened, routines, schedules.
**Products it powers:** Clock Goblin, Bookworm, Laundry Gremlin, Reading Lamp.

### Engine 3: ACT — physical world control

```
ESP32-S3 DevKit          £8.90
SG90 Micro Servo          £1.00
5V Relay Module           £1.00
WS2812B RGB LED           £0.30
USB-C Cable               £1.00
                        --------
BOM total:              ~£12.20
```

**What it does:** Controls physical things — lights, pumps, servos, relays.
**What it knows:** What actions are possible, what's been done.
**Products it powers:** Plant Sprite (pump), Coffee Goblin (weight sensor + display), Desk Goblin (LED + buzzer), Weather Mushroom, Mood Mushroom.

### Engine 4: TALK — voice and interaction

```
ESP32-S3 DevKit          £8.90
MAX98357 I2S Speaker Amp  £2.50
MEMS Microphone           £1.50
Push Button               £0.50
USB-C Cable               £1.00
                        --------
BOM total:              ~£14.40
```

**What it does:** Listens, speaks, button presses, voice commands.
**What it knows:** What the user says, what they want.
**Products it powers:** The Familiar, Desk Familiar, Parcel Owl, Keys Goblin.

### Engine 5: SEE — visual perception

```
ESP32-CAM Module          £7.50
SG90 Micro Servo x2       £2.00
USB-C Cable               £1.00
                        --------
BOM total:              ~£10.50
```

**What it does:** Captures images, tracks motion, recognises objects.
**What it knows:** What's in front of it.
**Products it powers:** Pet Bowl Sprite (pet recognition), Camera Familiar, 3D Printer Sprite (print monitoring).

---

## Engine → Product mapping

| Product | Engines needed | BOM | Price |
|---------|---------------|-----|-------|
| **Plant Sprite** | SENSE + ACT | £16.60 + £1.00 relay | £79 |
| **Coffee Goblin** | SENSE + REMEMBER | £16.60 + £1.50 RTC | £59-89 |
| **Sourdough Familiar** | SENSE + REMEMBER | £16.60 + £1.50 RTC | £59-99 |
| **Pet Bowl Sprite** | SENSE + SEE | £16.60 + £10.50 camera | £59-89 |
| **Bookworm** | REMEMBER | £13.40 + £3.00 NFC | £15-35 |
| **Guitar Guardian** | SENSE + REMEMBER | £16.60 + £1.50 RTC | £39-69 |
| **Parcel Owl** | SENSE + ACT | £16.60 + £1.00 relay | £39-59 |
| **Laundry Gremlin** | REMEMBER + ACT | £13.40 + £1.00 relay | £29-49 |
| **Fridge Goblins** | SENSE + REMEMBER | £16.60 + £3.00 NFC | £19-39 |
| **Seedling Family** | SENSE ×3 | £16.60 × 3 | £69-119 |
| **Desk Familiar** | TALK | £14.40 | £49-79 |
| **Keys Goblin** | SENSE + REMEMBER | £16.60 + £3.00 NFC | £39-59 |
| **Reading Lamp** | SENSE + REMEMBER + ACT | £16.60 + £1.50 + £1.00 | £59-99 |
| **Tool Familiar** | SENSE + REMEMBER | £16.60 + £3.00 NFC | £19-59 |
| **3D Printer Sprite** | SENSE + SEE | £16.60 + £7.50 camera | £59-99 |
| **Friendship Spirits** | ACT ×2 | £12.20 × 2 | £79-119/pair |

**Pattern: SENSE is the most reused engine (10 products). REMEMBER is second (7 products). ACT is third (5 products).**

---

## MCP interface (derived from engines)

### SENSE tools
```
pow_get_readings(device_id) → {moisture, light, temp, humidity}
pow_read_nfc(device_id) → {tag_id, data}
pow_get_history(device_id, hours) → [{timestamp, reading}]
```

### REMEMBER tools
```
pow_get_alarms(device_id) → [{time, label, repeat}]
pow_set_alarm(device_id, time, label, repeat)
pow_log_event(device_id, event_type, data)
pow_get_routine(device_id) → {schedule, history}
```

### ACT tools
```
pow_set_led(device_id, r, g, b)
pow_activate_relay(device_id, duration_ms)
pow_move_servo(device_id, angle)
pow_play_sound(device_id, sound)
pow_trigger_action(device_id, action)
```

### TALK tools
```
pow_speak(device_id, text)
pow_record(device_id, duration_ms) → {audio_data}
pow_button_press(device_id) → {timestamp}
```

### SEE tools
```
pow_capture_image(device_id) → {image_url}
pow_detect_motion(device_id) → {motion: bool}
pow_get_feed(device_id) → {stream_url}
```

### Cross-engine tools
```
pow_list_devices() → [{id, name, type, engines, status}]
pow_get_device_info(device_id) → {name, engines, config, history}
pow_configure_device(device_id, config) → {status}
```

---

## Product → Engine → MCP mapping

| Product | Engines | MCP tools used |
|---------|---------|---------------|
| Plant Sprite | SENSE + ACT | get_readings, set_led, trigger_action |
| Coffee Goblin | SENSE + REMEMBER | get_readings, log_event, get_routine |
| Sourdough Familiar | SENSE + REMEMBER | get_readings, get_history, log_event |
| Pet Bowl Sprite | SENSE + SEE | get_readings, capture_image, detect_motion |
| Bookworm | REMEMBER | log_event, get_routine |
| Guitar Guardian | SENSE + REMEMBER | get_readings, get_history |
| Parcel Owl | SENSE + ACT | get_readings, trigger_action |
| Laundry Gremlin | REMEMBER + ACT | log_event, trigger_action |
| Fridge Goblins | SENSE + REMEMBER | read_nfc, log_event, get_routine |
| Seedling Family | SENSE ×3 | get_readings (×3 devices) |
| Desk Familiar | TALK | speak, button_press |
| Keys Goblin | SENSE + REMEMBER | read_nfc, get_routine |
| Reading Lamp | SENSE + REMEMBER + ACT | get_readings, set_led |
| Tool Familiar | SENSE + REMEMBER | read_nfc, get_routine |
| 3D Printer Sprite | SENSE + SEE | get_readings, capture_image |
| Friendship Spirits | ACT ×2 | trigger_action (×2 devices) |

---

## The architecture

```
5 ENGINES (reusable electronics platforms)
    ↓ mapped to
16+ PRODUCTS (different enclosures + customisations)
    ↓ expose via
MCP TOOLS (derived from engine capabilities)
    ↓ connect to
MUSE (personal AI agent)
```

**Build 5 things. Sell hundreds of variations. Connect to one AI.**

---

## What to build next

1. **Prototype Engine 1 (SENSE)** — build and test the core sensor platform
2. **Prototype Engine 3 (ACT)** — build and test the core actuator platform
3. **Build Plant Sprite** — first product using SENSE + ACT
4. **Build Desk Goblin** — second product using ACT + display
5. **Wire to MCP** — expose engine capabilities
6. **Test with Muse** — verify end-to-end flow
7. **List on Etsy** — first sales
