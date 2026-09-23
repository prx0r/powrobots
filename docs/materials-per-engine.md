# Materials Per Engine — Canonical Specification

## Material Options

### SLA Resin
| Property | Value |
|----------|-------|
| Finish | Smooth, high detail |
| Colours | Many (white, black, grey, clear, coloured) |
| Strength | Low-medium |
| Flexibility | Low (brittle) |
| Water resistance | Low (porous) |
| Temperature | Up to 60°C |
| Cost | From $0.30/cm³ |
| Lead time | 2 days |
| Best for | Decorative characters, detailed features |
| Avoid for | Moving parts, outdoor use, high stress |

### MJF Nylon
| Property | Value |
|----------|-------|
| Finish | Matte, slightly rough |
| Colours | Grey (dyeable) |
| Strength | High |
| Flexibility | Medium (tough) |
| Water resistance | Medium |
| Temperature | Up to 120°C |
| Cost | From $1.00/cm³ |
| Lead time | 3 days |
| Best for | Snap-fit parts, functional enclosures, moving parts |
| Avoid for | High-detail decorative features |

### FDM Plastic
| Property | Value |
|----------|-------|
| Finish | Layered, visible lines |
| Colours | Many (PLA, ABS, PETG) |
| Strength | Medium |
| Flexibility | Medium |
| Water resistance | Low-medium |
| Temperature | Up to 80°C (PLA), 100°C (ABS) |
| Cost | From $0.10/cm³ |
| Lead time | 3 days |
| Best for | Prototyping, low-cost functional parts |
| Avoid for | High-detail features, snap-fit (weak layers) |

### SLS Nylon
| Property | Value |
|----------|-------|
| Finish | Matte, slightly rough |
| Colours | White (dyeable) |
| Strength | Very high |
| Flexibility | High (tough) |
| Water resistance | High |
| Temperature | Up to 150°C |
| Cost | From $3.00/cm³ |
| Lead time | 4 days |
| Best for | Functional parts, outdoor use, high stress |
| Avoid for | Cost-sensitive products |

### SLM Metal
| Property | Value |
|----------|-------|
| Finish | Metallic, rough |
| Colours | Silver (stainless steel, aluminium) |
| Strength | Very high |
| Flexibility | None (rigid) |
| Water resistance | High |
| Temperature | Up to 500°C |
| Cost | From $10.00/cm³ |
| Lead time | 5 days |
| Best for | Structural parts, heat-resistant components |
| Avoid for | Consumer products (too heavy, expensive) |

---

## Material Per Engine

### SENSE Engine

| Parameter | Value |
|-----------|-------|
| **Primary** | MJF Nylon |
| **Why** | Tough, snap-fit rails, outdoor-friendly |
| **Alternative** | SLA Resin (decorative only) |
| **Forbidden** | FDM (weak layers break at snap points) |
| **Colour** | Grey (dyeable to any colour) |
| **Notes** | Sensor exposure holes need clean edges |

### REMEMBER Engine

| Parameter | Value |
|-----------|-------|
| **Primary** | MJF Nylon |
| **Why** | Compact, needs snap-fit, desktop use |
| **Alternative** | SLA Resin (if decorative priority) |
| **Forbidden** | FDM (snap-fit unreliable) |
| **Colour** | Grey (dyeable) |
| **Notes** | Small enclosure, needs precise fit |

### ACT Engine

| Parameter | Value |
|-----------|-------|
| **Primary** | MJF Nylon |
| **Why** | Display window needs precise cutout, encoder access |
| **Alternative** | SLA Resin (higher detail for face) |
| **Forbidden** | FDM (display window warps) |
| **Colour** | Grey (dyeable) or SLA clear (for LED glow) |
| **Notes** | Display window must be optically clear if using LED behind |

### TALK Engine

| Parameter | Value |
|-----------|-------|
| **Primary** | MJF Nylon |
| **Why** | Acoustic properties, speaker openings need clean edges |
| **Alternative** | SLA Resin (smoother surface for sound) |
| **Forbidden** | FDM (porous, bad acoustics) |
| **Colour** | Grey (dyeable) |
| **Notes** | Speaker holes must not have stringing/defects |

### SEE Engine

| Parameter | Value |
|-----------|-------|
| **Primary** | SLA Resin |
| **Why** | Camera lens needs optical clarity, high detail |
| **Alternative** | MJF Nylon (if camera not behind resin) |
| **Forbidden** | FDM (layer lines block camera) |
| **Colour** | Clear or black (to prevent light bleed) |
| **Notes** | Camera opening must be precise 8mm diameter |

### COMPANION Engine

| Parameter | Value |
|-----------|-------|
| **Primary** | MJF Nylon |
| **Why** | Large enclosure, needs strength, screen cutout |
| **Alternative** | SLA Resin (if decorative priority) |
| **Forbidden** | FDM (too large, warps) |
| **Colour** | Grey (dyeable) |
| **Notes** | Screen opening must be precise 154×86mm |

---

## JLC3DP Pricing

### SLA Resin
| Type | Cost |
|------|------|
| Standard | $0.30/cm³ |
| High-temp | $0.50/cm³ |
| Flexible | $0.60/cm³ |
| Clear | $0.80/cm³ |
| Coloured | $1.00/cm³ |

### MJF Nylon
| Type | Cost |
|------|------|
| PA12 | $1.00/cm³ |
| PA12 GB (glass bead) | $1.50/cm³ |
| PA11 | $1.20/cm³ |

### FDM
| Type | Cost |
|------|------|
| PLA | $0.10/cm³ |
| ABS | $0.15/cm³ |
| PETG | $0.12/cm³ |
| TPU (flexible) | $0.20/cm³ |

### SLS Nylon
| Type | Cost |
|------|------|
| PA12 | $3.00/cm³ |
| PA11 | $3.50/cm³ |

### SLM Metal
| Type | Cost |
|------|------|
| Stainless Steel | $10.00/cm³ |
| Aluminium | $8.00/cm³ |

---

## Material Selection Logic

```python
def select_material(engine, requirements):
    if requirements["outdoor"]:
        return "MJF Nylon"  # Water resistant, UV stable
    
    if requirements["optical_clarity"]:
        return "SLA Resin"  # Clear, high detail
    
    if requirements["snap_fit"]:
        return "MJF Nylon"  # Tough, flexible
    
    if requirements["high_detail"]:
        return "SLA Resin"  # Smooth finish
    
    if requirements["low_cost"]:
        return "FDM PLA"  # Cheapest
    
    if requirements["high_strength"]:
        return "SLS Nylon"  # Strongest
    
    # Default
    return "MJF Nylon"  # Best all-around
```

---

## The Rule

**MJF Nylon is the default.** It works for most engines.

**Use SLA Resin only when:**
- Optical clarity needed (camera, LED glow)
- High detail needed (decorative face)
- Smooth finish needed (acoustic properties)

**Never use FDM for:**
- Snap-fit parts (layers break)
- Display windows (warp)
- Camera openings (layer lines block)
- Outdoor use (porous)

**Never use SLS or SLM unless:**
- Extreme strength needed
- High temperature environment
- Budget allows ($3-10/cm³)
