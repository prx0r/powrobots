# POW Design MCP — Peer Review

## Critical Findings

| Problem | Finding | Required Change |
|---------|---------|-----------------|
| **COMPANION dimensions** | Screen opening (154×86mm) exceeds enclosure max (150×120×80mm) | Correct screen spec or enlarge enclosure |
| **Engine constraints** | ACT requires display+encoder, but Mood Mushroom needs neither | Validate product-specific hardware, not just engine names |
| **Geometry validation** | STL doesn't reveal what openings are for | Introduce reference coordinate system and feature definitions |
| **Pricing** | £20.30 example is estimate, not real quote | Distinguish estimates, quotations, and confirmed costs |
| **Fulfilment** | Parts from separate suppliers presented as shipped kit | Require documented consolidation route |
| **Product identification** | Engine named but no PCB/enclosure revision | Make component revisions mandatory inputs |

## The Key Insight

**An engine describes capabilities. A product determines physical features.**

- Desk Goblin (ACT): display + encoder + buzzer
- Mood Mushroom (ACT): LEDs + diffuser (no display)

Both use ACT capabilities, but have different mechanical requirements.

## Existing Code Issues

| File | Problem |
|------|---------|
| `enclosures/generate.py` | Mesh faces have 4 vertices, STL loop expects 3 |
| `powrobots/mcp.py` | No CAD validator, fixed assembly allowances |
| `powphysical/mcp/server.py` | In-memory storage, not persistent |

## Revised Validation Stack

| Check | Tool | Purpose |
|-------|------|---------|
| Geometry | **Trimesh** | Dimensions, volume, watertightness, mesh inspection |
| Precision CAD | **CadQuery/OpenCascade** | STEP import, units, solids, assembly |
| Electronics pricing | **JLCPCB API** | Official pricing, component inventory |
| 3D printing | **JLC3DP API** | Model upload, automated pricing |

## JLCPCB API Discovery

**JLCPCB has an official developer API:**
- PCB pricing
- 3D-printing quotations
- Model upload
- Order creation and tracking
- Component prices and inventory

**Link:** https://api.jlcpcb.com/
**MCP:** https://github.com/eyalm321/jlcpcb-mcp

**Obstacle:** Application-based access, requires approval.

## Material-Specific Rules

| Parameter | MJF Nylon | FDM Plastic |
|-----------|-----------|-------------|
| Wall thickness | 1.0mm | 1.2mm |
| Clearance | 0.2-0.4mm | 0.5mm |
| Accuracy | ±0.3mm | ±0.3mm |

**Fixed 2mm rail / 1mm lip is not universal.** Must be material-specific.

## Revised Validation Pipeline

### Step 1: File Validity
- Supported format (STL, STEP, OBJ)
- Declared units
- Valid geometry
- No mesh defects

### Step 2: Mechanical Compatibility
- Compare with approved PCB CAD
- Check space for connectors, display, buttons
- Verify mounting features
- Check insertion path

### Step 3: Manufacturability
- Material-specific wall thickness
- Clearance rules
- Minimum features
- Build volume limits

### Step 4: Product Requirements
- Sensor exposure
- Ventilation
- Acoustics
- Camera visibility
- External moving parts

### Step 5: Procurement Feasibility
- Resolve every component
- Exact revision and quantity
- Missing parts block quotation

### Step 6: Pricing and Routing
- Calculate cost for quantity + destination
- Use recorded supplier prices
- Record verification timestamps
- Separate setup fees, shipping, unresolved costs

### Step 7: Manufacturing Approval
- Generate production package
- Supplier-confirmed only when manufacturer accepts

## Response Format

```json
{
  "product": "desk-goblin",
  "pcb_revision": "v1",
  "enclosure_revision": "grizelda-v1",
  "validation": {
    "file": "pass",
    "dimensions": "pass",
    "pcb_fit": "not_checked",
    "display_clearance": "not_checked",
    "manufacturability": "pending_review"
  },
  "quote": {
    "status": "estimate_only",
    "supplier_confirmed": false
  },
  "orderable": false
}
```

**Three results required:**
1. Geometry and fit
2. Manufacturing feasibility
3. Supplier acceptance

**A passing geometry check must NOT imply the other two passed.**

## Implementation Boundaries

| Repo | Responsibility |
|------|----------------|
| **powrobots** | Versioned hardware interfaces, approved BOMs, product constraints |
| **CAD validator** | Geometry checks (Trimesh/CadQuery) |
| **powphysical** | Supplier offers, cost calculations |
| **MCP** | Exposes capabilities to design tools and AI agents |

**MCP does NOT become a second database or purchasing system.**

## Acceptance Tests

1. Oversized enclosure → REJECT
2. Metre-scale STL mistaken for mm → REJECT
3. Display window misaligned → REJECT
4. Blocked USB-C port → REJECT
5. PCB fits but can't be inserted → REJECT
6. Fragile snap-fit → WARNING
7. Missing supplier price → INCOMPLETE estimate
8. Supplier failure → No complete quotation
9. Repeated order requests → No duplicate purchases

## First Checkpoint

**POW can:**
1. Accept independently created enclosure
2. Identify exact hardware compatibility
3. Explain geometric/manufacturing failures
4. Return traceable cost estimate
5. Not invent missing information
