# POW Glimlings — Review of the Latest Push

## The Central Idea

One product configuration system powers both the consumer customiser and the MCP tools. A customer shouldn't need to understand SENSE, ACT, TALK or PCB revisions. They should see a character, discover what it can do, choose its appearance and behaviour, and optionally connect it to an AI agent.

---

## The Experience to Build

```
glimlings.app — Customise your Glimling

# Meet Sporebert

Appearance: Purple mushroom, custom name, cap shape, glow colour.
Abilities: Monitor plant moisture, measure light and temperature, send watering alerts.
Personality: Quiet forest guardian, cheerful helper or mischievous goblin.
Voice: Choose a voice only when the product includes audio hardware.

The customer-facing design studio configures a product.
MCP exposes that product's capabilities to an AI agent.
Neither maintains an independent definition.
```

---

## What the Latest Push Gets Wrong

### Technical Blockers

1. **OpenSCAD templates** — Six of eight still contain placeholders (`WIDTH`, `ENGINE_TYPE`). Two developed templates are rectangular, not character designs. Python generator doesn't invoke new templates.

2. **Firmware** — Sends events to placeholder server, doesn't implement device MCP. References invalid ESP32-S3 pins (GPIO22-25 are excluded on S3).

3. **MCP specification** — Omits REMEMBER entirely, doesn't define motor-control tools for Fern or Petals.

4. **Supplier verification** — "78% ready" is self-assessed, not tested.

### Architecture Issue

The design studio, firmware, MCP tools and consumer app are treated as related features. **They need to be four interfaces to the same underlying product definition.**

---

## The Missing Layer: One Definition of Every Glimling

### Sporebert — Hardware Revision S1

| Layer | Definition |
|-------|------------|
| **Hardware** | SENSE + RGB LED + external soil probe |
| **Consumer studio** | Name, cap shape, colour, expression, glow behaviour, plant profile |
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
- Cloudflare Workers + Streamable HTTP (not SSE)
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

## The Key Insight: Moods Are Software

**Moods are entirely software-based.**

- Hardware stays the same
- Software changes the mood
- Same physical device, different personality
- No manufacturing changes needed

### This Makes Snap-Fit Design Functional

```
SNAP-ON HEADS:
  - Same electronics base
  - Different character shells
  - Snap on/off easily
  - Collect them all

COLLECTIONS:
  - Starter pack (1 base + 2 heads)
  - Expansion heads (£10-15 each)
  - Limited editions
  - Seasonal specials

THE INSIGHT:
  Cheap snap-fit design → Functional because:
  1. Swappable heads = collectibility
  2. Software moods = personality
  3. One base = many characters
  4. Low cost = impulse buy
```

### The Product Line

```
BASE UNIT (£34.99):
  - ESP32-S3
  - Soil sensor
  - LED
  - USB-C
  - 1 head included

EXPANSION HEADS (£10-15 each):
  - Mushroom head
  - Frog head
  - Ghost head
  - Fern head
  - Flower head
  - Cloud head
  - Tree head
  - Stone head

COLLECTOR SETS:
  - Starter (1 base + 2 heads): £49.99
  - Garden (1 base + 4 heads): £69.99
  - Complete (1 base + 8 heads): £99.99
```

---

## Why This Works

### For Customers

- **Low entry price** — £34.99 for base unit
- **Collectibility** — Cheap heads to collect
- **Personalisation** — Software moods, hardware appearance
- **Giftability** — Expansion heads as gifts
- **Fun** — Snap on new heads, change personality

### For POW

- **Low manufacturing cost** — One base, many heads
- **High margin** — Heads cost £2-3, sell for £10-15
- **Repeat purchases** — Customers buy more heads
- **Viral potential** — Collectors share collections
- **MCP integration** — Software changes, not hardware

### The Economics

```
BASE UNIT:
  Cost: £15-20
  Retail: £34.99
  Margin: 43-57%

EXPANSION HEAD:
  Cost: £2-3
  Retail: £10-15
  Margin: 70-80%

COLLECTOR SET:
  Cost: £25-35
  Retail: £69.99
  Margin: 50-63%
```

---

## The Vision

```
CUSTOMER BUYS:
  Base unit + 2 heads (£49.99)

CUSTOMER USES:
  - Snaps on mushroom head
  - Names it Sporebert
  - Chooses "playful" mood
  - Connects to Muse

CUSTOMER COLLECTS:
  - Buys frog head (£12.99)
  - Snaps it on
  - Chooses "curious" mood
  - New personality, same base

CUSTOMER GIFTS:
  - Buys ghost head for friend
  - Friend snaps it on their base
  - instant gift, no new electronics

THIS IS THE FUTURE.
Cheap snap-fit design + software moods = functional collectibility.
```

---

## Next Steps

1. **Design base unit** — Standard electronics, snap-fit interface
2. **Design first 3 heads** — Mushroom, Frog, Ghost
3. **Build firmware** — Mood system, MCP server
4. **Build glimlings.app** — Customisation, personality, AI connection
5. **Launch starter pack** — Base + 2 heads
6. **Release expansion heads** — Monthly new designs
7. **Build collector community** — Share collections, trade heads

**The snap-fit design isn't a limitation. It's the feature.**
