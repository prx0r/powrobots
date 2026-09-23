# Glimlings Should Be Collectible, Modular Creatures

## The Vision

The customer assembles their character, then continues changing and upgrading it over time. Instead of receiving a bag of electronics, they receive an assembled, tested electronic core, a character body and interchangeable accessories. They create their Glimling by snapping the pieces together.

**The customer should enjoy assembling the character, not have to troubleshoot the electronics.**

---

## The Glimlings Modular System

### Character Heads and Accessories

Mushroom caps · Frog heads · Flower petals · Fern fronds

**Collectible and interchangeable**

### Standard Glimling Core

Preassembled electronics · LED · Wi-Fi · Approved connectors

**Shared hardware interface**

### Base and Plant Accessories

Pot clip · Soil probe · Desk stand · USB-C power

**Replaceable functional parts**

---

## 1. Three Kinds of Interchangeable Parts

| Part Type | Examples | Customer Assembly |
|-----------|----------|-------------------|
| **Cosmetic** | Mushroom caps, frog heads, ghost faces, different ears and hats | Twist or snap into place. No electronics connections. |
| **Functional** | Soil probes, LED diffusers, plug-in sensors, sound modules | Keyed, labelled connectors. Power off before changing powered modules. |
| **Mechanical** | Fern fronds, flower heads, movable wings | Compatible only with the correct actuator module and mechanical interface. |

**Key Rule:** An interchangeable head shouldn't automatically imply that every Glimling has every capability. If someone puts a frog head on a silent Glow core, it still cannot croak.

---

## 2. Design Constraints for Each Garden Character

| Character | Swappable Parts | Fixed Design Constraints |
|-----------|-----------------|--------------------------|
| **Sporebert** | Caps, faces, tiny hats, translucent light diffusers | Every cap must fit the same stem socket and preserve the light path. The soil-probe cable exits through the base. |
| **Mosswick** | Frog heads, eyes, crowns, hats, lily-pad stands | Head attachments must not obstruct the LED eyes or sound opening on sound-enabled variants. |
| **Boo Bloom** | Ghost heads, expressions, costumes, illuminated inserts | Retain access to the internal LED diffuser and any installed motion sensor. |
| **Fern** | Different fronds, leaf styles and bases | Every frond must use the same keyed actuator coupling, remain within the servo's permitted load and have enough clearance to curl without striking the body. |
| **Petals** | Interchangeable flower heads, petal sets, centrepieces | Every moving flower head must attach to the approved drive mechanism. No unsupported petal weight or travel. |
| **Nimbus** | Cloud tops, raindrops, display stands | Do not block temperature, humidity or pressure sensing. Decorative raindrops should use a separate mounting position. |
| **Rootkin** | Leaf canopies, tree crowns, seasonal decorations | Maintain access to its plant connector and NFC reader; an interchangeable canopy cannot obstruct the NFC antenna. |
| **Pebble** | Outer stone shells, textured tops, pot stands | Its understated appearance can change, but the selected shell must preserve any touch-sensing area and light-transmitting region. |

---

## Example: One Sporebert, Four Looks

### Classic Cap
Round woodland mushroom

### Wizard Cap
Tall, pointed silhouette

### Moon Cap
Wide, softly illuminated

### Forest Cap
Textured with leaves

**Visual references for the interchangeable-cap concept, not actual POW CAD designs.**

---

## 3. The Common Mechanical Interface

### Garden Socket V1

| Interface | Proposed Standard |
|-----------|-------------------|
| **Cosmetic head** | Keyed quarter-turn or snap-lock attachment |
| **Base** | Universal mounting geometry for compatible Garden bodies |
| **LED** | Fixed location in core, with optional interchangeable diffuser |
| **Plant sensor** | Replaceable external probe with keyed connector |
| **Moving attachment** | Separate keyed motor coupling; mechanically incompatible with passive sockets |
| **USB-C** | Accessible in every assembled configuration |
| **Electronic expansion** | Approved low-voltage accessory port, concealed or protected |

### Manufacturing Constraints

- **Material:** MJF nylon for reusable mechanical connectors
- **Wall thickness:** 1mm minimum
- **Clearance:** 0.2-0.4mm for assembled parts, 0.6mm for moving parts
- **No magnets in V1** — ingestion hazard for children

---

## 4. Make Assembly Part of POW Studio

### Build Flow

```
1. Choose a character
   - Sporebert (Mushroom)
   - Mosswick (Frog)
   - Fern (Moving frond)

2. Choose an attachment
   - Classic cap
   - Wizard cap
   - Moon cap

3. Choose a personality
   - Playful app voice

4. Choose delivery
   - Snap-together character kit
   - Fully assembled

5. Preview
   - See Glimling being assembled in 3D
   - Select cap, watch it lock onto core
   - Change glow, preview expressions
```

### What the Customer Receives

**Snap-together kit:**
- Preassembled electronics in protected housing
- Personalised shell
- Interchangeable head
- External probe (where relevant)
- USB-C cable

**For kinetic characters:**
- Actuator already installed and electrically connected
- Customer attaches approved frond or flower head

---

## 5. The Accessory Marketplace

### Initial Catalogue

| Accessory | Compatibility | Purpose |
|-----------|---------------|---------|
| Seasonal mushroom caps | Sporebert, approved Garden Socket | Cosmetic collection |
| Expressions and frog hats | Mosswick | Character customisation |
| Replacement soil probes | Compatible SENSE revisions | Maintenance and replacement |
| Alternative fern fronds | Approved Fern actuator revision | Different physical movements |
| Flower-head collection | Approved Petals mechanism | Alternative flower designs |
| Decorative stands and pot clips | Compatible bases | Different display locations |
| Speaker or sensor upgrades | Only supported electronics revisions | Functional upgrades |

### Each Accessory Needs

- CAD file
- Material specification
- Compatible socket revisions
- Assembly instructions
- Estimated manufacturing cost
- Test evidence

---

## 6. The MCP Tools This Requires

### Design MCP

- Accessory discovery
- Assembly validation
- Customise head
- Validate attachment geometry
- Calculate additional cost
- Generate assembly instructions

### Device MCP

- Recognise installed hardware
- Distinguish cosmetic vs functional changes
- Verify accessory and power requirements
- Enforce torque, travel and speed limits for moving parts

### Product Manifest Must Distinguish

1. Purchased hardware
2. Installed accessories
3. Selected appearance
4. Configured personality
5. Currently permitted agent actions

**These are five different things.**

---

## 7. The Next Development Checkpoint

### Step 1: Define Garden Socket V1

- Common electronic-core envelope
- Actual CAD, not assumed ESP32 dimensions
- Frozen after mechanical testing

### Step 2: Create Sporebert Reference

- Base unit
- Three interchangeable cap designs
- Proper parametric geometry

### Step 3: Implement Accessory Registry

- Compatibility rules
- Studio previews
- Versioned manifests

### Step 4: Add Virtual Assembly Validation

- Collision checks
- Mounting interface alignment
- Material-specific clearances

### Step 5: Simulate Customer Assembly

- Assemble Glimling
- Install accessory
- Use permitted MCP abilities

### Step 6: Extend to Other Characters

- Mosswick (Glow)
- Fern (separate actuator coupling)
- Petals (separate actuator coupling)

### Requirements

- Repeated attachment-cycle test before claiming durability
- All manufacturing statuses explicitly provisional
- Supplier review and physical testing before launch

---

## The Vision

```
The product concept is a small, upgradeable creature with
a stable electronic identity and a changing physical appearance.

Customers can:
- Enjoy putting it together
- Replace worn parts
- Collect accessories
- Create their own compatible designs
- Keep the same Glimling as the range grows
```

**This is the future of collectible electronics.**
