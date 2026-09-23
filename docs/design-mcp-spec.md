# Design MCP — Revised Specification

## Architecture

**Validator-first: other tools create designs, POW determines manufacturability.**

```
USER (Blender/SCAD/Meshy)
    ↓
Provides: Character + Product + Enclosure STL
    ↓
DESIGN MCP (validator)
    ↓
Checks: File → Geometry → Mechanical → Manufacturability → Product → Procurement → Pricing
    ↓
Returns: Validation result + estimate (or rejection with reasons)
```

---

## Mandatory Inputs

### Product Identification (Required)

| Input | Type | Example |
|-------|------|---------|
| Product ID | Enum | `desk-goblin`, `garden-frog` |
| PCB revision | String | `v1`, `v2` |
| Enclosure revision | String | `grizelda-v1` |
| Hardware config | Object | `{display: true, encoder: true, buzzer: true}` |

### Design File (Required)

| Input | Type | Validation |
|-------|------|------------|
| Enclosure file | STL/STEP/OBJ | Format, units, geometry |
| Character name | Text | Max 20 chars |
| Character description | Text | Max 200 chars |
| Colour preference | Hex or name | Valid colour |

### Delivery Region (Required for pricing)

| Input | Type | Example |
|-------|------|---------|
| Country | String | `UK` |
| Region | String | `London` |

**Full address collected only at fulfilment, not design validation.**

---

## Validation Pipeline

### Step 1: File Validity

| Check | Tool | Pass Criteria |
|-------|------|---------------|
| Format | Parser | STL, STEP, OBJ, 3MF |
| Units | Detector | mm (auto-convert if needed) |
| File size | Checker | < 50MB |
| Geometry | Trimesh | Valid mesh, no holes |
| Orientation | Analyzer | Correct build orientation |
| Defects | Trimesh | No non-manifold edges |

### Step 2: Mechanical Compatibility

| Check | Tool | Pass Criteria |
|-------|------|---------------|
| PCB fit | CadQuery | Enclosure cavity fits PCB assembly |
| Connector access | CadQuery | USB-C port accessible |
| Display clearance | CadQuery | OLED window aligned (if ACT) |
| Encoder access | CadQuery | Knob accessible (if ACT) |
| Speaker clearance | CadQuery | Speaker fits (if TALK) |
| Camera clearance | CadQuery | Camera lens aligned (if SEE) |
| Insertion path | CadQuery | PCB can be inserted |

### Step 3: Manufacturability

| Check | Tool | Pass Criteria |
|-------|------|---------------|
| Wall thickness | Trimesh | ≥ 1.0mm (MJF) or ≥ 1.2mm (FDM) |
| Clearances | CadQuery | ≥ 0.2mm (MJF) or ≥ 0.5mm (FDM) |
| Build volume | Checker | Within JLC3DP limits |
| Material | Validator | MJF/SLA/FDM appropriate |
| Snap-fit | Analyzer | Rails meet material rules |

### Step 4: Product Requirements

| Check | Tool | Pass Criteria |
|-------|------|---------------|
| Sensor exposure | Validator | Holes for required sensors |
| Ventilation | Validator | Airflow for speaker/mic |
| Acoustics | Validator | Speaker openings present |
| Camera visibility | Validator | Lens opening unobstructed |
| LED visibility | Validator | Light paths clear |

### Step 5: Procurement Feasibility

| Check | Tool | Pass Criteria |
|-------|------|---------------|
| Component resolution | BOM resolver | Every part identified |
| Revision match | Validator | Correct revisions |
| Stock availability | Supplier API | Parts in stock |
| Alternative validation | Validator | Substitutes approved |

### Step 6: Pricing and Routing

| Check | Tool | Pass Criteria |
|-------|------|---------------|
| Parts cost | BOM resolver | Recorded prices with timestamps |
| Enclosure cost | JLC3DP API | Volume-based estimate |
| Assembly cost | Supplier quote | Or estimate if unavailable |
| Shipping cost | Route calculator | Based on destination |
| Total estimate | Calculator | Sum with uncertainty noted |

### Step 7: Manufacturing Approval

| Check | Tool | Pass Criteria |
|-------|------|---------------|
| Package generation | Generator | STL + BOM + instructions |
| Supplier submission | API/Manual | Files sent to manufacturer |
| Confirmation | Tracker | Manufacturer accepts |
| Status | Validator | `supplier_confirmed` only when accepted |

---

## Response Format

```json
{
  "product": "desk-goblin",
  "pcb_revision": "v1",
  "enclosure_revision": "grizelda-v1",
  "validation": {
    "file": "pass",
    "dimensions": "pass",
    "pcb_fit": "pass",
    "display_clearance": "pass",
    "encoder_access": "pass",
    "manufacturability": "pass",
    "product_requirements": "pass",
    "procurement": "partial",
    "pricing": "estimate_only"
  },
  "quote": {
    "status": "estimate_only",
    "supplier_confirmed": false,
    "parts_cost": 11.30,
    "enclosure_cost": 2.50,
    "assembly_cost": null,
    "shipping_cost": 12.00,
    "total_estimate": 25.80,
    "uncertainty": ["assembly_cost needs supplier quote"]
  },
  "orderable": false,
  "next_steps": [
    "Get assembly quote from Makerfabs",
    "Submit STL to JLC3DP for review"
  ]
}
```

---

## Three Validation Results

| Result | Meaning |
|--------|---------|
| **Geometry and fit** | STL is valid, fits PCB, meets dimensions |
| **Manufacturability** | Can be printed with selected material |
| **Supplier acceptance** | Manufacturer has accepted files |

**A passing geometry check does NOT imply the other two passed.**

---

## Price Status Levels

| Status | Meaning |
|--------|---------|
| `confirmed` | Supplier-quoted, verified |
| `estimate` | Based on recorded prices, may be outdated |
| `partial` | Some items priced, some missing |
| `unavailable` | No pricing data |

---

## Implementation

### powrobots
- Versioned hardware interfaces
- Approved BOMs
- Product constraints
- Component revisions

### CAD Validator (new)
- Trimesh for mesh validation
- CadQuery for STEP geometry
- Material-specific rules
- Feature detection

### powphysical
- Supplier offers
- Cost calculations
- Order management
- Persistent storage

### MCP
- Exposes validation to design tools
- Exposes quoting to AI agents
- Does NOT become database or purchasing system

---

## Acceptance Tests

1. Oversized enclosure → REJECT with reason
2. Metre-scale STL (wrong units) → REJECT with reason
3. Display window misaligned → REJECT with reason
4. Blocked USB-C port → REJECT with reason
5. PCB fits but can't be inserted → REJECT with reason
6. Fragile snap-fit → WARNING with recommendation
7. Missing supplier price → INCOMPLETE estimate
8. Supplier failure → No complete quotation
9. Repeated order requests → No duplicate purchases

---

## First Checkpoint

**POW can:**
1. Accept independently created enclosure
2. Identify exact hardware compatibility
3. Explain geometric/manufacturing failures
4. Return traceable cost estimate
5. Not invent missing information
