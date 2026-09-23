# POW Glimlings — Canonical Product Definition & Architecture

## The Core Principle

**One product definition, four interfaces.**

The design studio, firmware, MCP tools and consumer app are four interfaces to the same underlying product definition — not four separately maintained systems.

---

## One Canonical Product Manifest

### Sporebert — Hardware Revision S1

| Layer | Definition |
|-------|------------|
| **Hardware** | SENSE + RGB LED + external soil probe |
| **Consumer Studio** | Name, cap shape, colour, expression, glow behaviour, plant profile |
| **Device MCP** | Read moisture and light, get device status, change LED colour, configure alerts |
| **Firmware** | Correct sensor drivers, LED controller, pairing and approved configuration |
| **Manufacturing** | Exact PCB revision, sensor connector, enclosure interface, approved materials |

### Key Rules

- **Personality ≠ hardware capability** — Sarcastic personality works without a speaker
- **Appearance ≠ mechanics** — Can change Fern's colour but not disable curling clearance
- **One definition** — Studio, MCP, firmware, manufacturing all read from same source

---

## Two MCP Interfaces, One Backend

| Interface | What It Does |
|-----------|--------------|
| **Design MCP** | Discover products, inspect customisation, configure character, validate shell, preview behaviour, get quote |
| **Device MCP** | Discover owner's paired Glimlings, read sensors, change expressions, operate actuators, configure alerts |

### Connection Architecture

```
Customer / POW Studio / AI agent
    ↓
Glimlings Cloud API
    ↓
┌─────────────┬─────────────┐
│ Design MCP  │ Device MCP  │
└─────────────┴─────────────┘
    ↓               ↓
Product catalog  Owner permissions
CAD validator    Device registry
POW Physical     Command router
                      ↓
                Secure device API
                      ↓
                Customer's ESP32
```

### Key Distinction

- Designing a hypothetical Sporebert ≠ Access to someone's real Sporebert
- Different permissions for different interfaces
- Cloudflare Workers + Streamable HTTP
- ESP32 doesn't run full MCP — communicates with cloud backend

---

## Three Kinds of Customisation

### 1. Physical Appearance

| Setting | Affects |
|---------|---------|
| Shell shape | Manufacturing files |
| Colour | Manufacturing files |
| Facial expression | Manufacturing files |
| Name | Engraving/printing |

**Changing this regenerates STL.**

### 2. Behaviour

| Setting | Affects |
|---------|---------|
| LED animations | Firmware config |
| Movement style | Firmware config |
| Alert thresholds | Firmware config |
| Quiet hours | Firmware config |
| Speaker volume | Firmware config |

**Changing this updates firmware config.**

### 3. Personality & AI

| Setting | Affects |
|---------|---------|
| Personality (playful/reserved) | App/AI expression |
| Notification phrasing | App/AI expression |
| AI agent permissions | Security settings |
| Voice selection | App/AI settings |

**Changing this updates app/AI settings.**

### Key Rules

- Changing personality ≠ Regenerate STL
- Changing shell ≠ Reset plant history
- Revoking AI permissions ≠ Affect device firmware

---

## Capability Matrix

| Glimling | Customisable | Device Abilities |
|----------|--------------|------------------|
| **Sporebert** | Cap, colour, glow, name, personality | Read soil/environmental sensors; change LED patterns |
| **Fern** | Frond shape, colour, movement personality | Read moisture, curl and unfurl. Requires MOVE actuator |
| **Petals** | Petal shape, flower colour, bloom behaviour | Read moisture, open/close petals, control LEDs |
| **Mosswick** | Frog colour, eyes, croak style | Read moisture, illuminate eyes, play sounds |
| **Boo Bloom** | Ghost silhouette, expression, glow | Control light, react to movement |
| **Nimbus** | Cloud shape, illumination, notification style | Read temp, humidity, pressure |
| **Rootkin** | Tree shape, bark, leaves, personality | Monitor plant, NFC tags, history |
| **Pebble** | Shape, finish, colour, subtle light | Read plant conditions, discreet status |
| **Puck/Mab** | Face, display theme, sounds, character | Display expressions, button/encoder input |
| **SEE products** | Shell, camera presentation, uses | Capture images (camera hardware required) |

### Rules

- Show only options supported by selected product revision
- Camera toggle never appears for devices without camera
- Same rule for speakers, pumps, batteries
- MOVE must be explicit capability module (not ACT)

---

## Documentation Contradictions to Fix

### OpenSCAD Templates
- Six of eight contain placeholders (`WIDTH`, `ENGINE_TYPE`)
- Python generator not integrated with new templates
- Sporebert enclosure (65×60×45mm) exceeds SENSE spec (40mm limit)

### Firmware
- Desk-goblin loop has `UnboundLocalError` potential
- Uses unavailable GPIOs (GPIO22-25 don't exist on ESP32-S3)
- Valid GPIO ranges: 0-21 and 26-48

### MCP
- `glimlings-as-mcp-servers.md` shows simplified handler, not real implementation
- Build real protocol in cloud gateway, not on every microcontroller

### Integration Plan
- `mcp-integration-plan.md` still says "sell on Etsy first"
- Current objective: establish interfaces before manufacturing orders

---

## Implementation Order

### 1. Canonical Product & Capability Registry

Define versioned schemas for:
- Hardware revisions
- Available capabilities
- Supported character variations
- Optional modules
- Required permissions

**One schema package imported by studio and gateway.**

### 2. Sporebert as Reference Product

- Product manifest
- Selectable appearance and personality
- Simulated sensor readings
- LED state and notification behaviour
- Studio displays capabilities from manifest

### 3. Two MCP Interfaces

**Design MCP:**
- Customise draft Sporebert
- Validate configuration
- Inspect manufacturing requirements

**Device MCP:**
- Query simulated owner-paired Sporebert
- Operate simulated device
- Different permissions than Design MCP

### 4. Firmware & Device Identity Contracts

- Versioned messages for capabilities, telemetry, commands
- Validate commands against device hardware + owner permissions
- Build simulator before connecting actual firmware

### 5. Design Pipeline

- Studio generates configuration document
- Preview approved character
- Call existing CAD validator
- Distinguish illustrative preview from verified geometry
- Route pricing through powphysical
- Retain incomplete-quote states

### 6. Expand by Capability

After Sporebert:
1. **Puck** — Test display controls
2. **TALK variant** — Test real voice permissions
3. **Simulated Fern** — Test movement limits

**Each addition reuses same studio and MCP infrastructure.**

---

## Acceptance Test

```
1. Customer customises virtual Sporebert
2. Sees appearance and behaviour change
3. Connects simulated device
4. Authorises AI agent to read moisture and alter glow
5. Another user's agent cannot operate that device
6. Personality change doesn't imply new hardware
7. Unverified enclosure never receives manufacturing approval
```

**Result: Platform where every new Glimling automatically acquires:**
- Customisation interface
- Digital twin
- MCP capabilities permitted by physical hardware
