# POW Personal Robotics: the Etsy opportunity

The most interesting version of this is a personalised physical companion that connects to an AI agent. A customer doesn't just buy a plant sensor; they design a little creature, give it a name, choose its personality and connect it to their digital life.

Imagine buying a monstera and a little robot called Gerald. Gerald lives beside the pot, changes expression depending on the plant's condition and can send an alert when it needs attention. The owner could ask their personal AI assistant how Gerald is doing, provided the relevant integrations are supported.

That gives POW three things simultaneously: a consumer product business, real-world manufacturing and reliability data, and an expanding catalogue of reusable electronics and mechanical designs.

There's a significant distinction, though: the easy-to-manufacture products are mostly stationary electronic creatures, not moving robots. I'd use them to establish the business before adding motors, robotic arms or autonomous movement.

## 1. The competition is already proving parts of the concept

**FYTA Beam** — Plant-monitoring competitor. Measures soil moisture, light, temperature. Sold from ~€23. Has developer API (non-commercial).

**Elecrow GrowCube** — $99 system monitoring and watering 4 plants independently. Demonstrates plant care as hardware product.

**EMO** — $279 desktop robot companion. Moves, dances, recognises people. Personality-driven appeal.

**Petoi Nybble** — $299 open-source robot cat. 11 DOF, programmable, but complex assembly.

**The gap:** Customer-designed physical companions built from standardised, repairable modules, with AI compatibility as optional capability.

## 2. Twenty possible products

| # | Product | What makes it interesting | Price |
|---|---------|--------------------------|-------|
| 1 | Plant Sprite | Named creature monitoring a plant | £69-99 |
| 2 | Desk Goblin | Reacts to calendar/deadlines | £49-79 |
| 3 | Long-Distance Stones | Paired creatures for couples | £79-129/pair |
| 4 | Mood Mushroom | Weather/time/notifications display | £39-65 |
| 5 | Terrarium Guardian | Monitors terrarium temp/humidity | £69-99 |
| 6 | AI Summoning Stone | Physical button for AI workflows | £35-59 |
| 7 | Coffee Gremlin | Timer creature for breaks | £29-49 |
| 8 | Mailbox Goblin | Letterbox notification | £49-79 |
| 9 | Reading Familiar | NFC book tracker companion | £19-39 |
| 10 | Birthday Bot | Personalised birthday messages | £39-69 |
| 11 | Plant Family | Group of 3 monitors | £149-199 |
| 12 | Sunbeam Hunter | Light monitoring creature | £49-79 |
| 13 | Desktop Familiar | Pixel creature with animations | £45-75 |
| 14 | Robot Nameplate | Illuminated desk nameplate | £39-65 |
| 15 | Tiny Weather Witch | Weather-reactive character | £39-65 |
| 16 | Pet Feeding Companion | Feeding schedule display | £39-69 |
| 17 | Homecoming Sprite | Household event notifier | £49-79 |
| 18 | Robot Greenhouse | Desktop greenhouse + monitoring | £99-159 |
| 19 | Moving Desk Pet | Head-turning expressive creature | £119-179 |
| 20 | Mini Robot Assistant Arm | LeRobot-derived hobby arm | £199+ |

**Key:** Plant Sprite, Mood Mushroom, Desk Goblin, Tiny Weather Witch share nearly identical electronics. Only enclosure, firmware and sensors differ.

## 3. Three products to prototype first

**Plant Sprite** — moisture sensor + small display + ESP32 + USB power. Personalised character, shell colour, name, expression style. No microphone, camera or auto-watering in v1.

**Desk Goblin** — reacts to calendar/deadlines via USB computer connection. Different characters (robots, mushrooms, frogs, ghosts). Interchangeable shells.

**Long-Distance Stones** — paired creatures, one taps, other lights up. Requires messaging service and secure provisioning. Prototype after common hardware validated.

## 4. Two hardware families

**Family A: Personal electronics.** Stationary creatures. ESP32, sensors, LEDs, displays, one small servo. Open integrations (Home Assistant).

**Family B: Personal robotics.** Moving creatures, articulated heads, arms. LeRobot where hardware-control adds value.

Progression: stationary → articulated head → programmable desktop robot.

## 5. Design-to-product system

Customer description → AI design interpreter → POW compatibility graph → manufacturing output.

Five shell shapes, five facial expressions, multiple colours, one or two tested electronic assemblies.

JLCPCB: PCB from $8. Seeed Fusion: BOM matching. Neither eliminates final assembly/testing/compliance.

## 6. Muse integration

Design devices around independent event interface, not undocumented Muse capability.

```
Plant Sprite → secure event endpoint → customer notification → AI assistant
```

Deterministic sensor thresholds, not AI-decided. AI personalises explanation, not calibration.

## 7. Etsy economics

Plant Sprite at £79: ~£29 contribution (before overheads/tax/labour).

Etsy requirements: original designs (STL/CAD), disclosed production partners, PSTI compliance, WEEE obligations.

Start with 3 products sharing same electronics, changing appearances.

## 8. What to build first

1. Three-product Etsy collection (Plant Sprite, Desk Goblin, non-connected creature)
2. Parametric creature system with constrained customisation
3. Every order generates: design revision, exact BOM, firmware config, manufacturing record, personalised manual
4. Test geometric clearance, sensor readings, display, Wi-Fi, firmware updates
5. Physical acceptance test on every assembled unit
6. Sell replacement shells, sensors, repair parts
