# Consumer Agent Products — Muse Hardware via MCP

Physical AI agents that connect to Muse. Personalised. Sold on Etsy.

---

## The concept

Muse is the brain. POW is the body supplier. Etsy is the shop.

```
User: "Muse, I want a plant monitor"
Muse:  connects to POW MCP → resolves BOM → places order
User:  receives personalised plant agent → connects to Muse
Muse:  monitors moisture → alerts when thirsty → waters automatically
```

**The product isn't the hardware. It's the Muse integration + personalisation.**

---

## The 7 products

### 1. POW Plant Agent — "Your plant's voice"

**What it does:** Monitors soil moisture, light, temperature. Alerts Muse when plant needs water. Muse can schedule watering, send reminders, log plant health.

**BOM:** ESP32-S3 + soil moisture sensor + light sensor + temp/humidity + RGB LED + water pump relay + 3D printed enclosure
**Cost:** ~£15 | **Etsy:** £39.99 | **Margin:** ~60%

**Personalisation options:**
- Plant name engraved on base ("Gerald the Monstera")
- LED colour matches plant mood (green=healthy, blue=thirsty, red=urgent)
- Enclosure colour (match room decor)
- Muse personality (formal/casual/playful)
- Watering schedule (daily/weekly/custom)

**Muse integration:**
```
"Your monstera Gerald is getting thirsty — soil moisture at 22%"
"Shall I schedule watering for tomorrow morning?"
"Gerald's light levels have been low this week"
```

---

### 2. POW Desk Agent — "Your AI's physical presence"

**What it does:** Physical button, rotary knob, OLED display, status LED for Muse. Push-to-talk, volume control, task indicators.

**BOM:** ESP32-S3 + OLED display + rotary encoder + push button + RGB LED + buzzer + 3D printed stand
**Cost:** ~£12 | **Etsy:** £29.99 | **Margin:** ~60%

**Personalisation options:**
- Stand design (minimal/wood grain/industrial)
- LED ring colour (matches Muse's current mood)
- Engraved name or desk label
- Button function (push-to-talk, pomodoro, volume)

**Muse integration:**
```
"Your next meeting is in 15 minutes" (display shows)
"New email from Sarah" (LED pulses blue)
"Pomodoro break — stand up and stretch" (buzzer + LED)
```

---

### 3. POW Pet Agent — "Your pet's eyes and voice"

**What it does:** ESP32-CAM + speaker + treat dispenser servo. Muse can check on pets, play sounds, dispense treats remotely.

**BOM:** ESP32-CAM + MAX98357 speaker amp + SG90 servo (treat dispenser) + enclosure
**Cost:** ~£20 | **Etsy:** £49.99 | **Margin:** ~60%

**Personalisation options:**
- Pet name on base
- Voice personality (friendly/serious/silly)
- Treat dispensing schedule
- Camera angle preset

**Muse integration:**
```
"Checking on Whiskers..." (camera activates)
"Whiskers is napping on the sofa" (photo + description)
"Dispensing treat for Whiskers" (servo activates)
"Whiskers has been alone for 4 hours — want me to play some music?"
```

---

### 4. POW Lamp Agent — "Light that thinks"

**What it does:** RGB LED strip + dimmer + ambient light sensor. Muse controls lighting based on time, mood, activity.

**BOM:** ESP32-S3 + WS2812B LED strip + light sensor + dimmer + USB-C
**Cost:** ~£10 | **Etsy:** £24.99 | **Margin:** ~60%

**Personalisation options:**
- Base design (geometric/organic/minimal)
- Default colour palette (warm/cool/rainbow)
- Engraved name
- Scheduling presets (morning energise, evening calm)

**Muse integration:**
```
"Switching to evening mode — warm white at 40%"
"Your focus session starts in 5 minutes — brightening to 80%"
"Movie night detected — dimming to 10%"
```

---

### 5. POW Speaker Agent — "Muse with a voice"

**What it does:** I2S speaker + microphone + rotary volume control. Muse speaks through it, listens for voice commands.

**BOM:** ESP32-S3 + MAX98357 speaker amp + MEMS microphone + rotary encoder + speaker driver + enclosure
**Cost:** ~£15 | **Etsy:** £34.99 | **Margin:** ~57%

**Personalisation options:**
- Enclosure style (wood/acrylic/3D printed)
- Speaker grill design
- Voice personality selection
- Name engraved

**Muse integration:**
```
"Good morning, here's your weather and schedule"
"Your package has been delivered" (voice announcement)
"Play my morning playlist" (voice command → Muse action)
```

---

### 6. POW Camera Agent — "Muse's eyes"

**What it does:** ESP32-CAM + pan/tilt servos. Muse can look around, record events, monitor spaces.

**BOM:** ESP32-CAM + 2x SG90 servos (pan/tilt) + 3D printed mount + USB-C
**Cost:** ~£18 | **Etsy:** £39.99 | **Margin:** ~55%

**Personalisation options:**
- Mount style (wall/desk/shelf)
- Recording schedule
- Motion detection sensitivity
- Alert preferences

**Muse integration:**
```
"Motion detected in the living room" (camera pans to source)
"Recording started — 10 second clip saved"
"Check who's at the door" (camera activates, streams to Muse)
```

---

### 7. POW Tiny Robot — "Muse with wheels"

**What it does:** Wheels + ultrasonic sensor + servo head + RGB LED. Muse controls movement, obstacle avoidance, expressions.

**BOM:** ESP32-S3 + 2x DC motors + L298N driver + ultrasonic sensor + SG90 servo (head) + RGB LED + 18650 battery + enclosure
**Cost:** ~£17 | **Etsy:** £39.99 | **Margin:** ~57%

**Personalisation options:**
- Enclosure design (robot face/custom character)
- Movement personality (curious/cautious/bold)
- LED expressions (happy/sad/alert/thinking)
- Name + voice

**Muse integration:**
```
"Roaming the kitchen" (robot moves)
"Found something interesting under the table" (ultrasonic trigger)
"Wave hello!" (servo + LED animation)
```

---

## The product architecture

```
All 7 products share:
  ├── ESP32-S3 (compute + Wi-Fi/BLE)
  ├── USB-C (power)
  ├── RGB LED (status/mood)
  └── 3D printed enclosure (personalised)

Per-product additions:
  ├── Plant: moisture + light + temp + pump relay
  ├── Desk: OLED + encoder + button + buzzer
  ├── Pet: camera + speaker + servo
  ├── Lamp: LED strip + light sensor
  ├── Speaker: I2S amp + mic + encoder + driver
  ├── Camera: ESP32-CAM + 2x pan/tilt servos
  └── Robot: motors + driver + ultrasonic + servo head
```

**One codebase. One BOM core. Seven products. Infinite personalisation.**

---

## The Muse integration layer

### How products connect to Muse

```
Product boots → connects to Wi-Fi → registers with POW MCP
                                      ↓
                                 POW MCP exposes:
                                   - device status
                                   - sensor readings
                                   - actuator controls
                                   - personalisation profile
                                      ↓
                                 Muse discovers device via MCP
                                   - "I see a plant monitor named Gerald"
                                   - "Gerald's soil moisture is 22%"
                                   - "Gerald prefers watering on Tuesdays"
```

### MCP tools for Muse

| Tool | What it does |
|------|-------------|
| `pow_device_status(device_id)` | Get current sensor readings |
| `pow_device_control(device_id, action)` | Control actuators (LED, servo, pump) |
| `pow_device_profile(device_id)` | Get personalisation settings |
| `pow_device_history(device_id)` | Get historical sensor data |
| `pow_resolve_bom(product_type)` | Get parts list for a product |

### Muse workflows

**Plant monitoring:**
```
Muse: checks pow_device_status() every hour
If moisture < 30% → alerts user
If user approves → pow_device_control(pump, on)
Logs outcome to POW graph
```

**Pet monitoring:**
```
Muse: checks pow_device_status() for motion
If motion detected → pow_device_control(camera, capture)
Sends photo to user via WhatsApp
If no motion for 4 hours → alerts user
```

**Desk assistance:**
```
Muse: pushes task to pow_device_control(display, show)
User: presses button → pow_device_control(buzzer, beep)
Muse: receives confirmation → marks task complete
```

---

## The Etsy listing template

### Title
```
POW [Product Name] — Personalised AI Agent for Your [Context]
```

### Examples
```
POW Plant Agent — Personalised for Your Monstera
POW Desk Agent — Your AI Assistant's Physical Home
POW Pet Agent — Watch Over Your Cat from Anywhere
POW Lamp Agent — Smart Light That Knows Your Mood
POW Speaker Agent — Muse With a Voice
POW Camera Agent — Muse's Eyes for Your Home
POW Tiny Robot — A Little Robot That Follows Your Commands
```

### Description template
```
Meet [Name], your personal [product type].

This [product] monitors [what it monitors] and connects to
Muse, Meta's personal AI agent. When [trigger], Muse
[action] — all automatic, all personalised for you.

What's included:
- Assembled [product] with [key features]
- Personalised [enclosure/engraving/LED colour]
- USB-C cable
- Quick start guide
- Muse integration instructions

Personalisation:
- Name: [custom name]
- Colour: [LED/enclosure colour]
- [Product-specific options]

How it works:
1. Plug in via USB-C
2. Connect to your Wi-Fi
3. Open Muse → it finds your [product]
4. [Product] starts [monitoring/controlling]

Made with ❤️ by POW Systems
```

### Pricing strategy

| Product | BOM | Assembly | Personalisation | Etsy price | Margin |
|---------|-----|----------|----------------|-----------|--------|
| Plant Agent | £15 | £5 | £3 (engraving, colour) | £39.99 | ~55% |
| Desk Agent | £12 | £5 | £3 | £29.99 | ~55% |
| Pet Agent | £20 | £5 | £3 | £49.99 | ~52% |
| Lamp Agent | £10 | £5 | £3 | £24.99 | ~52% |
| Speaker Agent | £15 | £5 | £3 | £34.99 | ~52% |
| Camera Agent | £18 | £5 | £3 | £39.99 | ~50% |
| Tiny Robot | £17 | £5 | £3 | £39.99 | ~50% |

---

## The flywheel (final form)

```
POW graph (221 robots, 137 components, pricing)
        ↓
7 consumer agent products (ESP32-based, personalised)
        ↓
Etsy listings (personalised "made for you")
        ↓
Muse integration (AI controls the hardware)
        ↓
User feedback (which products work, what fails)
        ↓
POW graph improves (better BOMs, better parts)
        ↓
More products, better products
```

**The graph feeds the products. The products generate outcome data. The outcome data improves the graph. Muse is the distribution channel.**

---

## What to build first

1. **Plant Agent prototype** — simplest product, highest Etsy demand
2. **Muse MCP integration** — connect device to Muse
3. **Personalisation system** — name, colour, enclosure
4. **Etsy listing** — first product live
5. **Repeat for Desk Agent** — second product

**Week 1:** Plant Agent hardware + code + enclosure
**Week 2:** Muse MCP integration + personalisation
**Week 3:** Etsy listing + first sales
**Week 4:** Collect feedback → iterate
