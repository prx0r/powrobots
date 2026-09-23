# The Razor and Blades Model

## The Concept

**Base unit = Razor (expensive, buy once)**
**Heads = Blades (cheap, buy repeatedly)**

```
Customer buys base unit ONCE (£34.99)
Then buys heads forever (£10.99-19.99 each)

The expensive hardware is REUSABLE.
The cheap parts are CONSUMABLE/COLLECTIBLE.
```

---

## The Standardised Interface

### Connector Type: Snap-fit with electrical pass-through

| Component | Provides |
|-----------|----------|
| **Base unit** | Mechanical mounting, electrical connection, light transfer, sensor access |
| **Head** | Mechanical receiving, electrical contact, light input, optional module socket |

### Interface Features (10 connection points)

| Feature | Count | Purpose |
|---------|-------|---------|
| Snap clips | 4 | Mechanical attachment |
| Pogo pins | 3 | Electrical (VCC, GND, DATA) |
| Light pipe | 1 | Optical light transfer |
| Alignment pins | 2 | Prevent wrong orientation |
| Module socket | 1 | Optional expansion |

---

## Electrical Connection

### Pogo Pin Layout

```
    ┌─────────────────┐
    │   ○ VCC (3.3V)  │
    │                 │
    │   ○ GND         │
    │                 │
    │   ○ DATA (I2C)  │
    └─────────────────┘
```

### Why Pogo Pins

- No plugs to align
- Self-centering
- Reliable contact
- Cheap to manufacture
- Rated for 100,000+ cycles

### Electrical Protocol

| Pin | Function |
|-----|----------|
| VCC | 3.3V power to head |
| GND | Ground |
| DATA | I2C communication (SDA/SCL) |

**Head tells base:**
- "I am a mushroom"
- "I have NFC reader"
- "I have motion sensor"
- "I need these LED patterns"

**Base tells head:**
- "Here is sensor data"
- "Change LED to this colour"
- "Activate this feature"

---

## Mechanical Connection

### Snap-Fit Layout

```
    ┌─────────────────┐
    │  ┌───┐   ┌───┐  │
    │  │ 1 │   │ 2 │  │  ← Top clips
    │  └───┘   └───┘  │
    │                 │
    │  (  interface  )│
    │                 │
    │  ┌───┐   ┌───┐  │
    │  │ 3 │   │ 4 │  │  ← Bottom clips
    │  └───┘   └───┘  │
    └─────────────────┘
```

### Clip Design

- Cantilever snap (flex, then lock)
- 2mm engagement depth
- 0.5mm deflection
- Rated for 1000+ insertions

### Alignment Pins

- Prevent wrong orientation
- Self-centering
- 2mm diameter, 3mm length

---

## Head Types

### Basic Head

| Parameter | Value |
|-----------|-------|
| Description | Just a character shell |
| Electronics | None |
| Cost | £1.50-2.00 |
| Retail | £10.99 |
| Examples | Pebble, Simple mushroom |

### Glow Head

| Parameter | Value |
|-----------|-------|
| Description | Character with light diffuser |
| Electronics | Light pipe only |
| Cost | £2.00-3.00 |
| Retail | £12.99 |
| Examples | Sporebert, Mosswick, Boo Bloom |

### Sensor Head

| Parameter | Value |
|-----------|-------|
| Description | Character with extra sensor |
| Electronics | NFC, motion, touch, etc. |
| Cost | £3.00-5.00 |
| Retail | £14.99-17.99 |
| Examples | Rootkin (NFC), Boo Bloom (motion) |

### Motion Head

| Parameter | Value |
|-----------|-------|
| Description | Character with moving parts |
| Electronics | Servo or cam mechanism |
| Cost | £4.00-6.00 |
| Retail | £17.99-19.99 |
| Examples | Fern, Petals |

---

## The Economics

### Base Unit (Buy Once)

| Item | Value |
|------|-------|
| Cost | £16.10 |
| Retail | £34.99 |
| Margin | 54% |

### Heads (Buy Forever)

| Type | Cost | Retail | Margin |
|------|------|--------|--------|
| Basic | £1.50 | £10.99 | 85% |
| Glow | £2.00 | £12.99 | 85% |
| Sensor | £3.00 | £14.99 | 80% |
| Motion | £4.00 | £19.99 | 80% |

### Customer Lifetime Value

```
Base unit: £34.99 (one-time)
Heads: £10.99 × 8 = £87.92 (collect all)
Total: £122.91

Or: £10.99 × 12 months = £131.88/year (subscription model)
```

---

## Why This Works

### 1. One-Time Purchase

- Buy base unit once
- Reuse forever
- No planned obsolescence

### 2. Recurring Revenue

- Buy heads repeatedly
- Collect them all
- Seasonal limited editions

### 3. Low Marginal Cost

- Heads cost £1.50-4.00
- Sell for £10.99-19.99
- 80-85% margin on heads

### 4. Upgradeable

- Start with basic head
- Add sensor head later
- Add motion head later
- Same base, new features

### 5. Collectible

- 8 characters to collect
- Limited editions
- Trade with friends
- Social media content

### 6. Giftable

- Buy head as gift
- No new electronics needed
- Just snap on new character
- Perfect for birthdays

---

## Manufacturing

### Base Unit

| Item | Source | Cost |
|------|--------|------|
| ESP32-S3 DevKit | AliExpress | £5.50 |
| Soil sensor connector | AliExpress | £1.00 |
| RGB LED | AliExpress | £0.30 |
| USB-C breakout | AliExpress | £0.80 |
| Pogo pins (3x) | AliExpress | £0.30 |
| PCB (custom) | JLCPCB | £5.00 |
| Enclosure (base) | JLC3DP | £3.00 |
| **Total** | | **£16.10** |

### Expansion Head

| Item | Source | Cost |
|------|--------|------|
| Character shell | JLC3DP | £1.50-4.00 |
| Light pipe (if needed) | JLC3DP | £0.50 |
| Pogo pads (3x) | AliExpress | £0.10 |
| Optional module | AliExpress | £0.00-5.00 |
| **Total** | | **£1.50-9.00** |

---

## The Vision

```
CUSTOMER BUYS:
  Starter pack (£49.99)
  1 base + 2 heads

CUSTOMER COLLECTS:
  - Buys ghost head (£12.99)
  - Snaps it on
  - New personality, same base

CUSTOMER GIFTS:
  - Buys tree head for friend
  - Friend snaps it on their base
  - Instant gift, no new electronics

CUSTOMER UPGRADES:
  - Buys NFC head (£14.99)
  - Adds plant tracking
  - Same base, new features

THIS IS THE FUTURE.
One-time hardware purchase + recurring collectible revenue.
```
