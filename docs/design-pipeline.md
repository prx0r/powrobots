# Design-to-Manufacture Pipeline

Customer designs in Blender via Muse. POW resolves the BOM. Manufacturer builds it.

---

## The pipeline

```
Customer: "Design me a plant watering robot in the shape of a frog"
    ↓
Muse: calls Blender MCP → creates 3D model in Blender
    ↓
Blender: exports STL + BOM (parts list from the scene)
    ↓
Muse: calls POW MCP → pow_resolve_bom(design)
    ↓
POW: resolves each part → finds suppliers → returns UK prices
    ↓
Muse: "Here's your quote:
       ESP32-C3: £8.90 (Kunkune UK, next day)
       Water pump: £1.50 (AliExpress, 2 weeks)
       Servo: £3.99 (Amazon UK)
       Enclosure: £3.00 (JLC3DP, 2 days)
       Total: £17.39
       Or assembled kit: £39.99 from our store"
    ↓
Customer: "Get me the kit"
    ↓
Muse: places order via POW → Seeed/JLCPCB assembles
    ↓
Customer: receives assembled robot
```

## MCP tools (what we expose)

### Design tools (called by Muse)
```
pow_resolve_bom(design_file)     → BOM with prices per part
pow_find_substitutes(part_id)    → alternatives with evidence
pow_optimize_bom(design, strategy) → cheapest or fastest
pow_quote_build(design)          → full assembly quote
pow_list_components(query)       → search our parts graph
pow_robot_info(model_id)         → specs, compatibility
```

### Manufacturing tools (called by Muse)
```
pow_submit_design(design, config) → order created
pow_track_order(order_id)         → delivery status
pow_get_assembly_guide(model)     → step-by-step instructions
```

## Blender MCP integration

```
Muse connects to:
  1. Blender MCP (design tools)
  2. POW MCP (parts intelligence)
  3. Manufacturing APIs (JLCPCB, Seeed)

The flow:
  Muse → Blender MCP → creates model
  Muse → POW MCP → resolves BOM
  Muse → customer → approves quote
  Muse → manufacturing → places order
```

## What the customer sees

1. Describe what they want in natural language
2. Muse designs it in Blender (via MCP)
3. POW resolves parts and pricing (via MCP)
4. Customer approves the design and quote
5. Manufacturing begins (JLCPCB/Seeed)
6. Product ships to customer

**The customer never touches Blender, BOMs, or supplier APIs. Muse does everything.**
