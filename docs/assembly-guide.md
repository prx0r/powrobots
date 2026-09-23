# How to Assemble a Glimling

## The Shortcut

**M5Stack Atom Voice IS the electronics. We just put it in a character shell.**

No soldering. No wiring. Just snap-in.

---

## Assembly Steps

1. Design shell (OpenSCAD/Blender)
2. Print shell (JLC3DP)
3. Insert Atom Voice into shell
4. Flash firmware
5. Test
6. Package

**That's it. 6 steps. 10 minutes.**

---

## The Physical Assembly

### Atom Voice (What You Buy)

```
┌─────────────────────┐
│  ESP32              │
│  Microphone ●       │
│  Speaker ◉          │
│  RGB LED ●          │
│  Button ●           │
│  USB-C ○            │
│  Grove port ◇       │
└─────────────────────┘
Size: 24mm × 24mm × 13mm
Weight: ~10g
```

### Character Shell (What You Design)

```
┌─────────────────────┐
│  ▲▲▲ Mushroom cap   │
│  ┌─────────────┐    │
│  │ Atom Voice  │    │
│  │ (snaps in)  │    │
│  └─────────────┘    │
│  ═══════════════    │
│  USB-C access ○     │
│  Speaker holes ◉    │
│  LED window ●       │
└─────────────────────┘
Size: ~60mm × 60mm × 80mm
Material: MJF Nylon or SLA Resin
```

### Assembly

1. Push Atom Voice into shell (snaps into place)
2. USB-C port aligns with opening
3. Speaker aligns with holes
4. LED aligns with window
5. Button accessible through shell
6. Done.

---

## Design Constraints

### Atom Voice Dimensions

- Width: 24mm
- Length: 24mm
- Height: 13mm

### Shell Design Rules

1. Internal cavity: 26mm × 26mm × 15mm (clearance)
2. USB-C opening: 9mm × 4mm (bottom or back)
3. Speaker holes: 4-6 holes, 3mm diameter (front or bottom)
4. LED window: 5mm × 5mm (front, translucent)
5. Button access: 3mm hole (top or front)
6. Snap-fit rails: 2mm deep, 1mm lip

### Material

- MJF Nylon (tough, snap-fit friendly)
- Or SLA Resin (smooth, detailed)
- NOT FDM (layers break at snap points)

### Colour

- Any colour (MJF dyeable)
- Translucent for LED window (SLA)

---

## The Mushroom Example

### Mushroom Cap (Top)
- Translucent (lets LED glow through)
- Round shape
- Character features (eyes, face)

### Mushroom Stem (Middle)
- Holds Atom Voice
- Speaker holes on sides
- Button on top

### Mushroom Base (Bottom)
- USB-C port opening
- Stable base
- Optional: plant sensor connector

### Assembly

1. Push Atom Voice into stem cavity
2. USB-C aligns with base opening
3. Speaker aligns with side holes
4. LED shines through translucent cap
5. Button accessible through top
6. Cap snaps onto stem
7. Done.

**Total assembly time: 30 seconds**
**Tools required: None**
**Skills required: Can hold object**

---

## The Complete Kit

### What Customer Receives

1. M5Stack Atom Voice (pre-programmed)
2. 3D printed character shell (2 pieces)
3. USB-C cable
4. Quick start card
5. Gift box

### What Customer Does

1. Open box
2. Push Atom Voice into shell
3. Snap lid on
4. Plug in USB-C
5. Done!

**Time: 30 seconds**
**Skills: None**
**Tools: None**
**Satisfaction: High (built it themselves)**
