# Default Designs for Each Product

## The Idea

Create default designs that are:
1. **Ready to sell on Etsy** (pre-made)
2. **Easy to modify** (parametric)
3. **Customisable** (name, colour, features)
4. **Manufacturable** (within constraints)

### Two Products

| Product | Description | Price | Lead Time |
|---------|-------------|-------|-----------|
| **PRE-MADE** | Default design, ships now | £34.99-49.99 | 2-3 days |
| **CUSTOM** | Modified colour/name, made to order | £39.99-54.99 | 5-7 days |

---

## Default Designs

### Mosswick — Garden Frog

| Parameter | Value |
|-----------|-------|
| Engine | SENSE |
| Material | MJF Nylon |
| Default colour | Green |
| Size | 70×55×40mm |
| Features | Moisture sensor hole, LED window, USB-C port |
| Customisable | Colour, Name engraved, Sensor position |
| **Pre-made price** | **£39.99** |
| **Custom price** | **£44.99** |

### Sporebert — Garden Mushroom

| Parameter | Value |
|-----------|-------|
| Engine | SENSE |
| Material | MJF Nylon |
| Default colour | Purple |
| Size | 65×60×45mm |
| Features | Moisture sensor hole, LED window, USB-C port |
| Customisable | Colour, Name engraved, Mushroom cap shape |
| **Pre-made price** | **£39.99** |
| **Custom price** | **£44.99** |

### Boo Bloom — Garden Ghost

| Parameter | Value |
|-----------|-------|
| Engine | SENSE |
| Material | SLA Resin |
| Default colour | White |
| Size | 60×55×35mm |
| Features | Moisture sensor hole, LED glow, USB-C port |
| Customisable | Colour, Name engraved, Ghost shape |
| **Pre-made price** | **£44.99** |
| **Custom price** | **£49.99** |

### Puck — Desk Goblin

| Parameter | Value |
|-----------|-------|
| Engine | ACT |
| Material | MJF Nylon |
| Default colour | Green |
| Size | 80×65×45mm |
| Features | OLED window, Encoder knob, Buzzer hole, USB-C port |
| Customisable | Colour, Name engraved, Face expression |
| **Pre-made price** | **£49.99** |
| **Custom price** | **£54.99** |

### Mab — Desk Familiar

| Parameter | Value |
|-----------|-------|
| Engine | ACT |
| Material | MJF Nylon |
| Default colour | Blue |
| Size | 75×60×40mm |
| Features | OLED window, Encoder knob, Buzzer hole, USB-C port |
| Customisable | Colour, Name engraved, Face expression |
| **Pre-made price** | **£49.99** |
| **Custom price** | **£54.99** |

### Nimbus — Home Weather

| Parameter | Value |
|-----------|-------|
| Engine | SENSE |
| Material | MJF Nylon |
| Default colour | Light Blue |
| Size | 70×55×35mm |
| Features | Temp/humidity vents, Light window, USB-C port |
| Customisable | Colour, Name engraved, Vent pattern |
| **Pre-made price** | **£39.99** |
| **Custom price** | **£44.99** |

### Chroma — Home Mood

| Parameter | Value |
|-----------|-------|
| Engine | SENSE |
| Material | SLA Resin |
| Default colour | Clear |
| Size | 65×50×40mm |
| Features | LED diffuser, USB-C port |
| Customisable | Colour, Name engraved, Diffuser pattern |
| **Pre-made price** | **£44.99** |
| **Custom price** | **£49.99** |

### Wormington — Bookworm

| Parameter | Value |
|-----------|-------|
| Engine | REMEMBER |
| Material | MJF Nylon |
| Default colour | Brown |
| Size | 60×45×30mm |
| Features | NFC window, LED window, USB-C port |
| Customisable | Colour, Name engraved, Book shape |
| **Pre-made price** | **£34.99** |
| **Custom price** | **£39.99** |

---

## The System

### Step 1: Create Parametric Templates

Create OpenSCAD templates for each product type:
- `templates/frog.scad` — Garden frog enclosure
- `templates/mushroom.scad` — Garden mushroom enclosure
- `templates/ghost.scad` — Garden ghost enclosure
- `templates/goblin.scad` — Desk goblin enclosure
- `templates/familiar.scad` — Desk familiar enclosure
- `templates/weather.scad` — Home weather enclosure
- `templates/mood.scad` — Home mood enclosure
- `templates/bookworm.scad` — Bookworm enclosure

### Step 2: Generate Default STLs

```bash
# Generate default designs
python enclosures/generate.py --product frog --colour green --name "Mosswick"
python enclosures/generate.py --product mushroom --colour purple --name "Sporebert"
python enclosures/generate.py --product ghost --colour white --name "Boo Bloom"
# ... etc
```

### Step 3: Pre-Print Inventory

Order 5-10 of each from JLC3DP:
- 5× Mosswick (green frog)
- 5× Sporebert (purple mushroom)
- 5× Boo Bloom (white ghost)
- 5× Puck (green goblin)
- 5× Mab (blue familiar)
- 5× Nimbus (light blue weather)
- 5× Chroma (clear mood)
- 5× Wormington (brown bookworm)

**Total: 40 units × ~£20 = £800 inventory**

### Step 4: List on Etsy

```
Mosswick — Garden Sensor Glimling
£39.99 · Ships in 2-3 days

A personalised garden companion that monitors your plant's
soil moisture, light, and temperature. Named Mosswick,
this little frog guardian connects to your Wi-Fi and
reports to your AI assistant.

✅ Pre-made, ready to ship
✅ Default green colour
✅ Includes USB-C cable
✅ 1-year warranty

🎨 Want a custom colour or name? Order the "Custom" variant
   and we'll make it just for you (+£5, ships in 5-7 days)
```

### Step 5: Handle Custom Orders

When custom order comes in:
1. Modify parametric template (colour, name)
2. Generate new STL
3. Upload to JLC3DP
4. Print (2-4 days)
5. Assemble with pre-made electronics
6. Ship to customer (5-7 days total)

---

## Revenue Projections

### Pre-Made (Etsy)

| Product | Price | Units/Month | Revenue |
|---------|-------|-------------|---------|
| Mosswick | £39.99 | 10 | £399.90 |
| Sporebert | £39.99 | 10 | £399.90 |
| Boo Bloom | £44.99 | 5 | £224.95 |
| Puck | £49.99 | 10 | £499.90 |
| Mab | £49.99 | 10 | £499.90 |
| Nimbus | £39.99 | 5 | £199.95 |
| Chroma | £44.99 | 5 | £224.95 |
| Wormington | £34.99 | 5 | £174.95 |
| **Total** | | **60** | **£2,624.40** |

### Custom (Etsy + Website)

| Product | Price | Units/Month | Revenue |
|---------|-------|-------------|---------|
| All products | £44.99-54.99 | 20 | £999.80 |
| **Total** | | **20** | **£999.80** |

### Total Monthly Revenue

| Channel | Revenue |
|---------|---------|
| Pre-made | £2,624.40 |
| Custom | £999.80 |
| **Total** | **£3,624.20** |

### Costs

| Item | Cost |
|------|------|
| Electronics (60 units × £15) | £900.00 |
| Enclosures (60 units × £3) | £180.00 |
| Packaging (80 units × £3) | £240.00 |
| Shipping (80 units × £3.50) | £280.00 |
| Etsy fees (~11%) | £398.66 |
| **Total costs** | **£1,998.66** |

### Profit

| Item | Amount |
|------|--------|
| Revenue | £3,624.20 |
| Costs | £1,998.66 |
| **Profit** | **£1,625.54** |
| **Margin** | **45%** |

---

## Next Steps

1. **Create OpenSCAD templates** for each product
2. **Generate default STLs**
3. **Order 5 of each from JLC3DP** (£800)
4. **Assemble with pre-made electronics**
5. **List on Etsy**
6. **Start selling**

**Milestone: First 10 orders fulfilled**
