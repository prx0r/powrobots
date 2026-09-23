# Snap-In Design Constraints — Canonical Specification

## The Key Insight

**Constraints breed creativity.**

Without constraints, you get 1m tall mushrooms that cost £500 to print.

WITH constraints, you get:
- Realistic products that actually ship
- Predictable costs
- Repeatable manufacturing
- Fun creative challenges (design within limits)

Think of it like:
- LEGO has constraints (brick sizes, connection points)
- Haiku has constraints (5-7-5 syllables)
- Game jams have constraints (48 hours, one theme)

---

## The Five Constraint Layers

### Layer 1: Electronics (Fixed)

| Component | Dimensions | Weight |
|-----------|------------|--------|
| ESP32-S3 DevKit | 25.8mm × 50.8mm × 3.6mm | 10g |
| OLED 0.96" | 27.3mm × 27.8mm × 4mm | 5g |
| DHT22 | 15.1mm × 25mm × 7.7mm | 3g |
| BH1750 | 32mm × 18mm × 3mm | 2g |
| MAX98357 | 18mm × 18mm × 3mm | 2g |
| INMP441 | 14mm × 10mm × 1mm | 1g |
| WS2812B | 5mm × 5mm × 1.5mm | 1g |
| USB-C | 8.94mm × 7.3mm × 3.2mm | 2g |

### Layer 2: Connectors (Fixed)

| Connector | Pitch | Notes |
|-----------|-------|-------|
| Pin headers | 2.54mm | Standard ESP32 breakout |
| JST connectors | 2.5mm | Optional quick-connect |
| USB-C port | 8.94mm wide | Must have opening in enclosure |

### Layer 3: Enclosure (Constrained)

| Parameter | Value |
|-----------|-------|
| Minimum size | ESP32 + 1 module + USB-C port |
| Maximum size | ESP32 + 6 modules + battery + speaker |
| Wall thickness | 1.5-2mm (SLA) or 2-3mm (FDM) |
| Snap-fit rails | 2mm deep, 1mm lip |
| Tolerance | ±0.2mm (SLA) or ±0.3mm (FDM) |

### Layer 4: Cost (Constrained)

| Item | Range |
|------|-------|
| Parts | £5-25 (depending on engine) |
| Enclosure | £2-5 (JLC3DP) |
| Packaging | £3 |
| Shipping | £3.50 |
| **Total** | **£17-52** |

### Layer 5: Character (Free)

| Parameter | Freedom |
|-----------|---------|
| Shape | Any (within enclosure constraints) |
| Colour | Any (JLC3DP SLA/MJF supports many) |
| Face | Any (printed, painted, or sticker) |
| Name | Any (engraved or printed) |
| Texture | Any (smooth, rough, patterned) |

---

## Constraint Table Per Engine

### SENSE Engine

| Parameter | Value |
|-----------|-------|
| Electronics | ESP32 + BH1750 + DHT22 + LED + USB-C |
| Min size | 50mm × 40mm × 25mm |
| Max size | 80mm × 60mm × 40mm |
| Max weight | 50g |
| Allowed shapes | Any (must fit electronics + sensor exposure) |
| Forbidden | No moving parts, no waterproofing (unless specified) |
| Character freedom | HIGH — face, colour, name, texture |

### REMEMBER Engine

| Parameter | Value |
|-----------|-------|
| Electronics | ESP32 + RTC + LED + USB-C |
| Min size | 50mm × 40mm × 20mm |
| Max size | 70mm × 50mm × 30mm |
| Max weight | 40g |
| Allowed shapes | Any (compact, desktop-friendly) |
| Forbidden | No moving parts |
| Character freedom | HIGH — face, colour, name, texture |

### ACT Engine

| Parameter | Value |
|-----------|-------|
| Electronics | ESP32 + OLED + encoder + buzzer + LED + USB-C |
| Min size | 60mm × 50mm × 30mm |
| Max size | 90mm × 70mm × 50mm |
| Max weight | 80g |
| Allowed shapes | Any (must have display window + control access) |
| Forbidden | No moving parts (unless external servo) |
| Character freedom | MEDIUM — face is OLED, colour/name free |

### TALK Engine

| Parameter | Value |
|-----------|-------|
| Electronics | ESP32 + speaker amp + mic + speaker + button + USB-C |
| Min size | 70mm × 60mm × 40mm |
| Max size | 100mm × 80mm × 60mm |
| Max weight | 100g |
| Allowed shapes | Any (must have speaker openings + mic access) |
| Forbidden | No sealed enclosures (needs air for speaker/mic) |
| Character freedom | MEDIUM — face features, colour/name free |

### SEE Engine

| Parameter | Value |
|-----------|-------|
| Electronics | Seeed XIAO ESP32-S3 Sense + USB-C |
| Min size | 40mm × 35mm × 25mm |
| Max size | 60mm × 50mm × 35mm |
| Max weight | 40g |
| Allowed shapes | Any (must have camera lens opening) |
| Forbidden | No opaque lens covers, no moving parts |
| Character freedom | HIGH — camera is eye, colour/name free |

### COMPANION Engine

| Parameter | Value |
|-----------|-------|
| Electronics | ESP32 + touchscreen + speaker amp + mic + camera + USB-C |
| Min size | 100mm × 80mm × 50mm |
| Max size | 150mm × 120mm × 80mm |
| Max weight | 200g |
| Allowed shapes | Any (must have screen, speaker, mic, camera access) |
| Forbidden | No sealed enclosures (needs air for speaker/mic) |
| Character freedom | LOW — screen dominates, colour/name free |

---

## Answer: Can Someone Design a 1m Thing?

**NO. The constraints prevent it.**

### Maximum Sizes

| Engine | Max Height | Max Width | Max Depth |
|--------|------------|-----------|-----------|
| SENSE | 80mm (8cm) | 60mm | 40mm |
| REMEMBER | 70mm (7cm) | 50mm | 30mm |
| ACT | 90mm (9cm) | 70mm | 50mm |
| TALK | 100mm (10cm) | 80mm | 60mm |
| SEE | 60mm (6cm) | 50mm | 35mm |
| COMPANION | 150mm (15cm) | 120mm | 80mm |

### What Happens If Someone Tries

A 1m tall mushroom would:
1. Exceed max size constraints
2. Cost £50+ to print (JLC3DP charges by volume)
3. Not fit the snap-in electronics
4. Be rejected by the design validation

---

## The Design MCP

### How It Works

```
Input: "I want a 1m tall mushroom with eyes"
    ↓
Design MCP validates:
  - Exceeds max size (80mm for SENSE)
  - Would cost £50+ to print
  - Won't fit electronics
    ↓
Output: "Sorry, max height is 80mm. Would you like a 7cm mushroom instead?"
```

### MCP Tools

| Tool | What It Does |
|------|--------------|
| `validate_design` | Check if design fits constraints |
| `calculate_cost` | Estimate print cost based on volume |
| `suggest_modifications` | How to fit within limits |
| `generate_enclosure` | Create STL within constraints |

### Validation Rules

```python
def validate_design(engine, dimensions, cost):
    # Check size constraints
    if dimensions > ENGINE_MAX_SIZE[engine]:
        return REJECT, f"Max size is {ENGINE_MAX_SIZE[engine]}"
    
    # Check cost constraints
    if cost > ENGINE_MAX_COST[engine]:
        return REJECT, f"Max cost is £{ENGINE_MAX_COST[engine]}"
    
    # Check required features
    if engine == "ACT" and not has_display_window:
        return REJECT, "ACT engine needs display window"
    
    if engine == "TALK" and not has_speaker_openings:
        return REJECT, "TALK engine needs speaker openings"
    
    if engine == "SEE" and not has_camera_opening:
        return REJECT, "SEE engine needs camera opening"
    
    return PASS, "Design is valid"
```

---

## The Creative Challenge

**Design within constraints is MORE fun, not less.**

Examples:
- "Design a mushroom that's 7cm tall and holds a temperature sensor"
- "Design a ghost that's 6cm tall and has a camera eye"
- "Design a frog that's 8cm tall and glows in the dark"

The constraints force creative solutions:
- How to make a small mushroom look like a mushroom?
- How to hide a camera in a ghost's eye?
- How to make a frog glow without making it too big?

**This is the design MCP: creative characters within manufacturing constraints.**
