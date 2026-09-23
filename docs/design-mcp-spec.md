# Design MCP: Limitations + Required Inputs

## The Insight

**We don't need to build a design tool. We need to build a VALIDATOR.**

1. Define constraints (what's allowed)
2. Define required inputs (what user must provide)
3. Let people use whatever tool they want
4. MCP validates and quotes

### Tools People Can Use

| Tool | Type | Cost |
|------|------|------|
| Blender | 3D modelling | Free |
| Fusion360 | CAD | Free for personal |
| OpenSCAD | Parametric | Free |
| Meshy | AI 3D generation | Paid |
| Tripo | AI 3D generation | Paid |
| three.ws | AI 3D generation | Free tier |
| Hand drawing | Sketch | Free |

**MCP just says: "Yes, that fits" or "No, here's why"**

---

## Limitations Per Engine

### SENSE Engine

| Parameter | Constraint |
|-----------|------------|
| **Size min** | 50mm × 40mm × 25mm |
| **Size max** | 80mm × 60mm × 40mm |
| **Weight** | 50g max |
| **Cost** | £19 total |
| **Required features** | USB-C port opening, Sensor exposure (light, temp) |
| **Forbidden** | Moving parts, Waterproofing (unless specified) |
| **Material** | SLA resin or MJF nylon |
| **Power** | USB-C only (5V, 500mA) |
| **Assembly** | Snap-fit rails, 2mm deep, 1mm lip |
| **Compliance** | RoHS, WEEE (if selling in UK) |

### REMEMBER Engine

| Parameter | Constraint |
|-----------|------------|
| **Size min** | 50mm × 40mm × 20mm |
| **Size max** | 70mm × 50mm × 30mm |
| **Weight** | 40g max |
| **Cost** | £17 total |
| **Required features** | USB-C port opening |
| **Forbidden** | Moving parts |
| **Material** | SLA resin or MJF nylon |
| **Power** | USB-C only (5V, 500mA) |
| **Assembly** | Snap-fit rails, 2mm deep, 1mm lip |
| **Compliance** | RoHS, WEEE |

### ACT Engine

| Parameter | Constraint |
|-----------|------------|
| **Size min** | 60mm × 50mm × 30mm |
| **Size max** | 90mm × 70mm × 50mm |
| **Weight** | 80g max |
| **Cost** | £20.30 total |
| **Required features** | USB-C port opening, Display window (27×28mm), Encoder access, Buzzer sound opening |
| **Forbidden** | Moving parts (unless external servo) |
| **Material** | SLA resin or MJF nylon |
| **Power** | USB-C only (5V, 500mA) |
| **Assembly** | Snap-fit rails, 2mm deep, 1mm lip |
| **Compliance** | RoHS, WEEE |

### TALK Engine

| Parameter | Constraint |
|-----------|------------|
| **Size min** | 70mm × 60mm × 40mm |
| **Size max** | 100mm × 80mm × 60mm |
| **Weight** | 100g max |
| **Cost** | £22.80 total |
| **Required features** | USB-C port opening, Speaker openings (multiple holes or grille), Mic access (small hole), Button access |
| **Forbidden** | Sealed enclosures (needs air for speaker/mic) |
| **Material** | SLA resin or MJF nylon |
| **Power** | USB-C only (5V, 500mA) |
| **Assembly** | Snap-fit rails, 2mm deep, 1mm lip |
| **Compliance** | RoHS, WEEE |

### SEE Engine

| Parameter | Constraint |
|-----------|------------|
| **Size min** | 40mm × 35mm × 25mm |
| **Size max** | 60mm × 50mm × 35mm |
| **Weight** | 40g max |
| **Cost** | £24.49 total |
| **Required features** | USB-C port opening, Camera lens opening (8mm diameter) |
| **Forbidden** | Opaque lens covers, Moving parts |
| **Material** | SLA resin or MJF nylon |
| **Power** | USB-C only (5V, 500mA) |
| **Assembly** | Snap-fit rails, 2mm deep, 1mm lip |
| **Compliance** | RoHS, WEEE |

### COMPANION Engine

| Parameter | Constraint |
|-----------|------------|
| **Size min** | 100mm × 80mm × 50mm |
| **Size max** | 150mm × 120mm × 80mm |
| **Weight** | 200g max |
| **Cost** | £52.50 total |
| **Required features** | USB-C port opening, Screen opening (154×86mm), Speaker openings, Mic access, Camera opening |
| **Forbidden** | Sealed enclosures (needs air for speaker/mic) |
| **Material** | SLA resin or MJF nylon |
| **Power** | USB-C only (5V, 2A) |
| **Assembly** | Snap-fit rails, 2mm deep, 1mm lip |
| **Compliance** | RoHS, WEEE, Radio equipment (Wi-Fi) |

---

## Required Data Inputs

### For Any Engine (Required)

| Input | Type | Validation |
|-------|------|------------|
| Character name | Text | Max 20 chars, no special characters |
| Character description | Text | Max 200 chars |
| Colour preference | Hex code or name | Must be valid colour |
| Engine selection | Enum | SENSE/REMEMBER/ACT/TALK/SEE/COMPANION |
| Enclosure file | STL or STEP | Must pass geometry validation |
| Shipping address | Address | Must be valid UK address |

### For SENSE Engine (Additional)

| Input | Type | Validation |
|-------|------|------------|
| Plant name | Text | Max 30 chars (if garden product) |
| Sensor exposure | Enum | Top/Side/Bottom |

### For ACT Engine (Additional)

| Input | Type | Validation |
|-------|------|------------|
| Display content | Enum | Face/Text/Animation |
| Control preference | Enum | Encoder/Button/Touch |

### For TALK Engine (Additional)

| Input | Type | Validation |
|-------|------|------------|
| Speaker volume | Enum | Quiet/Normal/Loud |
| Microphone sensitivity | Enum | Low/Medium/High |

### For SEE Engine (Additional)

| Input | Type | Validation |
|-------|------|------------|
| Camera angle | Enum | Forward/Upward/Downward |
| Field of view | Enum | Wide/Narrow |

### For COMPANION Engine (Additional)

| Input | Type | Validation |
|-------|------|------------|
| Screen content | Enum | Face/Info/Both |
| Camera usage | Enum | Video calls/Monitoring/Both |
| Audio preference | Enum | Speaker/Mic/Both |

---

## How the MCP Works

### Step 1: User Provides Inputs

```
User: "I want a Desk Goblin named Grizelda, green, with OLED face"
  → Engine: ACT
  → Name: Grizelda
  → Colour: #00FF00
  → Display content: Face
  → Control: Encoder
```

### Step 2: User Provides Enclosure

```
User uploads: grizelda_enclosure.stl
  → MCP validates geometry
  → Checks size constraints
  → Checks required features
```

### Step 3: MCP Validates

```python
def validate_design(engine, inputs, enclosure_file):
    # Check size
    if enclosure.size > ENGINE_MAX_SIZE[engine]:
        return REJECT, f"Too big: {enclosure.size} > {ENGINE_MAX_SIZE[engine]}"
    
    # Check required features
    if engine == "ACT":
        if not has_display_window(enclosure):
            return REJECT, "ACT needs display window (27×28mm)"
        if not has_encoder_access(enclosure):
            return REJECT, "ACT needs encoder access"
    
    # Check cost
    if calculate_cost(engine, enclosure) > ENGINE_MAX_COST[engine]:
        return REJECT, f"Over budget: £{cost} > £{ENGINE_MAX_COST[engine]}"
    
    return PASS, "Design is valid"
```

### Step 4: MCP Quotes

```
MCP: "Design is valid!
  Parts: £11.30
  Enclosure: £2.50 (JLC3DP)
  Packaging: £3.00
  Shipping: £3.50
  Total: £20.30
  Retail: £39.99
  Margin: 49%
  
  Estimated delivery: 5-9 days
  Assemble time: 3 minutes"
```

### Step 5: User Orders

```
User: "Approved, ship to [address]"
  → MCP submits enclosure to JLC3DP
  → MCP orders parts from AliExpress
  → MCP ships kit to customer
```

---

## What MCP Does NOT Do

| MCP Does | MCP Does Not |
|----------|--------------|
| Validate constraints | Design the enclosure |
| Calculate costs | Generate 3D models |
| Provide quotes | Model characters |
| Route to suppliers | Create textures |
| Track orders | Animate characters |
| Handle payments | Store designs |

**People use their own tools. MCP just validates and routes.**

---

## The Architecture

```
USER (any tool)
    ↓
Provides: Character + Engine + Enclosure STL
    ↓
DESIGN MCP
    ↓
Validates: Size, features, cost, compliance
    ↓
Quotes: Parts + enclosure + packaging + shipping
    ↓
Routes: To suppliers (JLC3DP, AliExpress, etc.)
    ↓
Ships: Kit to customer
```

**The MCP is a VALIDATOR and ROUTER, not a DESIGN TOOL.**
