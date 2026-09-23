# Waterproof Options for Garden Products

## The Answer

**Yes, we have waterproof options.** JLC3DP offers waterproof materials and there are waterproof sensor modules.

---

## Waterproof Materials at JLC3DP

### SLA Resin (Waterproof)

| Material | Properties | Cost | Best For |
|----------|------------|------|----------|
| **LEDO 6060** | Waterproof, functional prototypes | $0.30/cm³ | Garden enclosures |
| **8000 Resin** | High toughness, good surface | $1.00/cm³ | Outdoor products |
| **8228 Resin** | Batch production, waterproof | $1.00/cm³ | Garden sensors |

### MJF Nylon (Water-Resistant)

| Material | Properties | Cost | Best For |
|----------|------------|------|----------|
| **PA12** | Medium water resistance, tough | $1.00/cm³ | Garden enclosures |
| **PA11** | Higher water resistance | $1.20/cm³ | Outdoor products |

### FDM (Outdoor-Ready)

| Material | Properties | Cost | Best For |
|----------|------------|------|----------|
| **ASA** | UV resistant, weather proof | $0.15/cm³ | Outdoor enclosures |
| **PETG** | Water resistant, durable | $0.12/cm³ | Garden sensors |
| **TPU** | Flexible, waterproof gaskets | $0.20/cm³ | Seals and gaskets |

---

## Waterproof Sensors for Garden

| Sensor | Type | Waterproof? | Cost | Use Case |
|--------|------|-------------|------|----------|
| **DFRobot SEN0193** | Soil moisture | ✅ Probe is waterproof | £8.00 | Plant monitoring |
| **DFRobot SEN0308** | Soil moisture | ✅ Fully waterproof | £12.00 | Outdoor soil |
| **DS18B20** | Temperature | ✅ Waterproof probe | £2.00 | Water temperature |
| **DHT22** | Temp/humidity | ❌ Not waterproof | £2.00 | Indoor only |
| **BMP280** | Barometric | ❌ Not waterproof | £3.00 | Weather station |
| **Capacitive soil** | Moisture | ⚠️ Partially | £1.50 | Indoor plants |

---

## Waterproof Enclosure Design

### IP Rating System

| Rating | Protection | Use Case |
|--------|------------|----------|
| **IP54** | Dust protected, splash proof | Light rain, sprinklers |
| **IP65** | Dust tight, water jets | Garden watering, rain |
| **IP66** | Dust tight, powerful water jets | Heavy rain, pressure wash |
| **IP67** | Dust tight, temporary immersion | Puddles, flooding |
| **IP68** | Dust tight, continuous immersion | Submersion (not needed) |

**For garden products: IP65 is sufficient.**

### Design Features for Waterproofing

```
1. SEALING
   - TPU gaskets at joints
   - O-rings around cables
   - Silicone sealant on seams

2. DRAINAGE
   - Drain holes at bottom
   - Sloped surfaces
   - No water pooling

3. VENTILATION
   - Gore-tex vents (air passes, water doesn't)
   - Desiccant packs inside
   - Conformal coating on PCB

4. CABLE ENTRY
   - Cable glands (M12, M16)
   - Strain relief
   - Sealed connectors

5. MATERIAL
   - UV-resistant (ASA, PA12)
   - No PLA (degrades in sun)
   - Dark colours (hide dirt)
```

---

## Garden Product Waterproofing

### Mosswick (Garden Frog)

| Component | Waterproof Solution |
|-----------|---------------------|
| Enclosure | ASA or PA12, IP65 |
| Soil sensor | DFRobot SEN0193 (waterproof probe) |
| Cable entry | M12 cable gland |
| Sealing | TPU gasket between halves |
| LED | Sealed behind clear resin window |

### Sporebert (Garden Mushroom)

| Component | Waterproof Solution |
|-----------|---------------------|
| Enclosure | ASA or PA12, IP65 |
| Soil sensor | DFRobot SEN0193 (waterproof probe) |
| Cable entry | M12 cable gland |
| Sealing | TPU gasket between halves |
| LED | Sealed behind clear resin window |

### Boo Bloom (Garden Ghost)

| Component | Waterproof Solution |
|-----------|---------------------|
| Enclosure | SLA resin (waterproof LEDO 6060) |
| Soil sensor | DFRobot SEN0193 (waterproof probe) |
| Cable entry | M12 cable gland |
| Sealing | Resin is naturally waterproof |
| LED | Glow through translucent resin |

---

## Waterproof Enclosure Template

```openscad
// Waterproof garden enclosure
module waterproof_enclosure(width, length, height) {
    wall = 2.5;  // Thicker for waterproofing
    
    difference() {
        // Outer shell
        cube([width, length, height]);
        
        // Inner cavity
        translate([wall, wall, wall])
            cube([width-2*wall, length-2*wall, height-2*wall]);
        
        // Cable gland hole (bottom)
        translate([width/2, length/2, -1])
            cylinder(d=12, h=wall+2);  // M12 gland
        
        // Drain holes (bottom corners)
        translate([wall+5, wall+5, -1])
            cylinder(d=3, h=wall+2);
        translate([width-wall-5, wall+5, -1])
            cylinder(d=3, h=wall+2);
    }
    
    // Gasket groove (between halves)
    translate([wall-0.5, wall-0.5, height/2])
        difference() {
            cube([width-2*wall+1, length-2*wall+1, 1.5]);
            translate([0.75, 0.75, 0])
                cube([width-2*wall-0.5, length-2*wall-0.5, 1.5]);
        }
}
```

---

## Cost Impact

| Item | Standard | Waterproof |
|------|----------|------------|
| Enclosure | £2.00 | £3.50 |
| Sensor | £1.50 | £8.00 |
| Cable gland | £0.00 | £1.50 |
| Gasket | £0.00 | £0.50 |
| **Total** | **£3.50** | **£13.50** |
| **Price increase** | | **+£10.00** |

### Garden Product Pricing (Waterproof)

| Product | Standard | Waterproof | Retail |
|---------|----------|------------|--------|
| Mosswick | £19.00 | £29.00 | £49.99 |
| Sporebert | £19.00 | £29.00 | £49.99 |
| Boo Bloom | £24.00 | £34.00 | £54.99 |

**Waterproof adds ~£10 to cost, ~£10 to retail.**

---

## Recommendations

### For Indoor Products
- Use standard MJF Nylon
- No waterproofing needed
- Cheaper, simpler

### For Outdoor Products (Garden)
- Use ASA or PA12
- Add TPU gaskets
- Use waterproof sensors (DFRobot SEN0193)
- Add cable glands
- Add drainage holes
- IP65 rating

### For Premium Outdoor
- Use SLA resin (LEDO 6060)
- Full IP66 rating
- Conformal coating on PCB
- Sealed connectors
- UV-resistant material

---

## The Garden Engine (Updated)

### Components

| Part | Supplier | Cost | Waterproof |
|------|----------|------|------------|
| ESP32-S3 DevKit | LCSC/Alibaba | £5.50 | ❌ (needs enclosure) |
| DFRobot SEN0193 | DFRobot | £8.00 | ✅ Probe |
| BH1750 Light | LCSC/Alibaba | £1.50 | ❌ (needs enclosure) |
| DHT22 | LCSC/Alibaba | £2.00 | ❌ (needs enclosure) |
| WS2812B LED | LCSC/Alibaba | £0.50 | ❌ (needs enclosure) |
| USB-C cable | Alibaba | £1.00 | ⚠️ (use gland) |
| Cable gland M12 | Amazon | £1.50 | ✅ |
| TPU gasket | JLC3DP | £0.50 | ✅ |

### Total Cost (Waterproof Garden)

| Item | Cost |
|------|------|
| Parts | £20.50 |
| Enclosure (ASA) | £3.50 |
| Packaging | £3.00 |
| Shipping | £3.50 |
| **Total** | **£30.50** |
| **Retail** | **£49.99** |
| **Margin** | **39%** |

---

## Summary

| Question | Answer |
|----------|--------|
| Waterproof options? | **Yes** — ASA, PA12, SLA LEDO 6060 |
| Waterproof sensors? | **Yes** — DFRobot SEN0193 (soil), DS18B20 (temp) |
| IP rating needed? | **IP65** for garden products |
| Cost impact? | **+£10** per unit |
| Retail impact? | **+£10** per product |
| Margin impact? | **39%** (still good) |

**Garden products are viable with waterproofing. The extra £10 cost is justified by outdoor use.**
