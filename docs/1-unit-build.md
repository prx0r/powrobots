# 1-Unit Build: The Real Answer

## YES, there's a cheaper way

The trick: **Design a custom PCB** with all components on it, then JLCPCB assembles it.

---

## How It Works

### Old Way (Expensive)
```
Buy dev boards + sensors separately → Assemble manually → £189-299 via Seeed
```

### New Way (Cheap)
```
Design custom PCB → JLCPCB assembles it → Plug in enclosure → Ship
```

---

## JLCPCB Pricing (The Real Deal)

| Item | Cost |
|------|------|
| PCB fabrication | $2 per board |
| Setup fee | $8 one-time |
| SMT assembly | $0.0016 per solder joint |
| Components | From their stock (720,000+ parts) |
| **Total for 2 boards** | **~$10-15** |

**MOQ: 2 boards** (but at $2 each, that's $4 for 2 PCBs)

---

## Example: Desk Agent Custom PCB

Instead of buying 6 separate parts and wiring them together:

| Component | Dev Board Way | Custom PCB Way |
|-----------|---------------|----------------|
| ESP32-S3 | £5.50 (dev board) | £1.80 (module on PCB) |
| OLED Display | £3.00 (separate) | £1.50 (mounted on PCB) |
| Buzzer | £0.20 (separate) | £0.10 (on PCB) |
| LED | £0.30 (separate) | £0.05 (on PCB) |
| USB-C | £0.80 (breakout) | £0.20 (on PCB) |
| Wiring | £1.50 (jumper wires) | £0 (traces on PCB) |
| **Assembly** | Manual (30 min) | JLCPCB ($8 + joints) |
| **Total** | **£11.30 + your time** | **~$10 for 2 boards** |

---

## What You Need to Design

A simple PCB with:
1. ESP32-S3 module footprint
2. OLED display connector
3. Buzzer footprint
4. WS2812B LED footprint
5. USB-C connector
6. Sensor connectors (I2C/GPIO)
7. Power regulation

**Tools:** KiCad (free) or EasyEDA (free, integrates with JLCPCB)

---

## Cost Comparison

| Method | 1-Unit Cost | Time | Skill Needed |
|--------|-------------|------|--------------|
| Seeed Fusion (full turnkey) | £189-299 | 7-15 days | None |
| Manual assembly | £26 + your time | 1 day | Soldering |
| **Custom PCB + JLCPCB** | **~$10-15** | **3-5 days** | **PCB design** |

---

## The Pipeline (Custom PCB)

```
1. Design PCB in KiCad/EasyEDA (1-2 days)
2. Export Gerber + BOM + CPL files
3. Upload to JLCPCB
4. JLCPCB sources components + assembles ($8-15)
5. Receive assembled boards (2-4 days)
6. Flash firmware via USB
7. Plug into 3D printed enclosure (JLC3DP)
8. Ship via Royal Mail
```

**Total time: 5-10 days**
**Total cost: ~$15-20 all-in per unit (at 2 boards)**

---

## Other Cheap Assemblers (1 Unit)

| Assembler | MOQ | Estimated Cost | Notes |
|-----------|-----|----------------|-------|
| **POE PCBA** | 1 | £30-60 | No MOQ, turnkey |
| **BELI Technologies** | 1 | £30-60 | No MOQ for prototypes |
| **MKT PCB** | 1 | £30-60 | Low volume specialist |
| **JLCPCB** | 2 | ~$10-15 | Cheapest, but need 2 |

---

## AI Agents + Python Visuals

You're right — AI agents are great at Python visuals. For a screen product:

```python
# Example: Glimling mood display
from PIL import Image, ImageDraw, ImageFont

def create_glimling_display(mood, name):
    img = Image.new('RGB', (128, 64), color='black')
    draw = ImageDraw.Draw(img)
    
    # Draw mood face
    if mood == 'happy':
        draw.ellipse([32, 10, 96, 54], outline='green', width=2)
        draw.ellipse([45, 25, 55, 35], fill='green')  # left eye
        draw.ellipse([73, 25, 83, 35], fill='green')  # right eye
        draw.arc([45, 35, 83, 50], 0, 180, fill='green', width=2)  # smile
    
    # Add name
    draw.text((32, 55), name, fill='white')
    
    return img
```

**This runs on the ESP32-S3 with a small OLED display.**

---

## Updated 1-Unit Cost (Custom PCB)

| Engine | Components | PCB Assembly | Enclosure | Shipping | **All-In** |
|--------|-----------|--------------|-----------|----------|------------|
| Desk Agent | £1.80 (module) | ~$10 (JLCPCB) | £1.50 | £3.50 | **~£17** |
| Plant Agent | £1.80 (module) | ~$12 (JLCPCB) | £1.50 | £3.50 | **~£19** |
| Lamp Agent | £1.80 (module) | ~$10 (JLCPCB) | £1.50 | £3.50 | **~£17** |
| Speaker Agent | £1.80 (module) | ~$15 (JLCPCB) | £1.50 | £3.50 | **~£22** |
| Tiny Robot | £1.80 (module) | ~$18 (JLCPCB) | £1.50 | £3.50 | **~£25** |
| Camera Agent | £1.80 (module) | ~$15 (JLCPCB) | £1.50 | £3.50 | **~£22** |
| Pet Agent | £1.80 (module) | ~$18 (JLCPCB) | £1.50 | £3.50 | **~£25** |

**That's £17-25 all-in for 1 assembled unit.** vs £189-299 via Seeed.

---

## Bottom Line

| Question | Answer |
|----------|--------|
| Can we use Mirage/Tesseract? | **No** — it's for video editing, not product design |
| Is there a cheaper way? | **YES** — custom PCB + JLCPCB = $10-15 for 2 assembled boards |
| Can AI agents help? | **YES** — Python visuals for OLED displays, KiCad scripting |
| 1-unit cost? | **£17-25** (custom PCB) vs £189-299 (Seeed) |

**The trick is to stop buying dev boards and start designing custom PCBs.**
