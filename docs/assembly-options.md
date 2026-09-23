# Glimlings Assembly Options

## The Four Options

| Option | Price | Margin | Customer Effort | Best For |
|--------|-------|--------|-----------------|----------|
| **A. DIY Kit** | £29.99 | 30% | 5 min, snap parts | Budget customers, education |
| **B. Snap-Fit Kit** | £39.99 | 29% | 1 min, snap module | **Recommended start** |
| **C. Factory Assembled** | £59.99 | 25% | 10 sec, unbox | Convenience customers |
| **D. Custom PCB** | £79.99 | 21% | 10 sec, unbox | Premium customers |

---

## Option A: DIY Kit (£29.99)

### What Customer Receives
- ESP32-S3 DevKit board (pre-flashed with firmware)
- OLED display module
- Buzzer module
- LED module
- USB-C cable
- 3D printed enclosure (2 pieces: base + lid)
- Instruction card with QR code

### What Customer Does
1. Plug OLED into ESP32 (4 pins)
2. Plug buzzer into ESP32 (2 pins)
3. Plug LED into ESP32 (3 pins)
4. Put ESP32 in enclosure base
5. Snap lid on
6. Plug in USB-C power
7. Done!

### Time: 5 minutes
### Tools: None
### Skill: Can read instruction card

### Cost Breakdown
| Item | Cost |
|------|------|
| Parts (dev board + sensors) | £12.50 |
| Enclosure (3D printed) | £2.00 |
| Assembly labour | £0.00 |
| Packaging | £3.00 |
| Shipping to customer | £3.50 |
| **Total** | **£21.00** |
| **Retail** | **£29.99** |
| **Margin** | **30%** |

---

## Option B: Snap-Fit Kit (£39.99) ← RECOMMENDED

### What Customer Receives
- Pre-wired electronics module (ESP32 + all components connected)
- 3D printed enclosure (2 pieces: base + lid)
- USB-C cable
- Instruction card

### What Customer Does
1. Put module in enclosure base
2. Snap lid on
3. Plug in USB-C power
4. Done!

### Time: 1 minute
### Tools: None
### Skill: Can hold object

### Cost Breakdown
| Item | Cost |
|------|------|
| Parts (dev board + sensors) | £15.00 |
| Enclosure (3D printed) | £2.00 |
| Assembly labour | £5.00 |
| Packaging | £3.00 |
| Shipping to customer | £3.50 |
| **Total** | **£28.50** |
| **Retail** | **£39.99** |
| **Margin** | **29%** |

### Why This is Best
1. **Easiest for customer** - 1 minute, no tools
2. **Easiest for us** - Pre-assemble modules in batches
3. **Good margin** - 29% at £39.99
4. **Scalable** - Can batch assemble modules
5. **Low risk** - Module is pre-tested

---

## Option C: Factory Assembled (£59.99)

### What Customer Receives
- Finished Glimling (fully assembled)
- USB-C cable
- Instruction card

### What Customer Does
1. Plug in USB-C power
2. Done!

### Time: 10 seconds
### Tools: None
### Skill: Can plug in cable

### Cost Breakdown
| Item | Cost |
|------|------|
| Parts (dev board + sensors) | £15.00 |
| Enclosure (3D printed) | £2.00 |
| Assembly labour | £15.00 |
| Packaging | £3.00 |
| Shipping to customer | £10.00 |
| **Total** | **£45.00** |
| **Retail** | **£59.99** |
| **Margin** | **25%** |

### Requirements
- Makerfabs or similar factory partner
- Minimum order quantities
- Quality control process

---

## Option D: Custom PCB (£79.99)

### What Customer Receives
- Finished Glimling (custom PCB, premium enclosure)
- USB-C cable
- Instruction card
- Character card with name and personality

### What Customer Does
1. Plug in USB-C power
2. Done!

### Time: 10 seconds
### Tools: None
### Skill: Can plug in cable

### Cost Breakdown
| Item | Cost |
|------|------|
| Parts (custom PCB) | £20.00 |
| Enclosure (3D printed) | £5.00 |
| Assembly labour | £25.00 |
| Packaging | £3.00 |
| Shipping to customer | £10.00 |
| **Total** | **£63.00** |
| **Retail** | **£79.99** |
| **Margin** | **21%** |

### Requirements
- Custom PCB design (HeyPCB or KiCad)
- Factory assembly
- Higher NRE costs

---

## Recommendation

### Start With: Option B (Snap-Fit Kit)

**Why:**
1. **Easiest to build** - No custom PCB, no factory partner
2. **Easiest for customer** - 1 minute assembly
3. **Good margin** - 29% at £39.99
4. **Scalable** - Can batch assemble modules
5. **Test the market** - See if people buy before investing in factory

### How to Build

**Batch assemble modules:**
1. Order 10-20 ESP32-S3 DevKits from AliExpress (£5.50 each)
2. Order 10-20 OLED displays from AliExpress (£3.00 each)
3. Order 10-20 buzzers from AliExpress (£0.20 each)
4. Order 10-20 LEDs from AliExpress (£0.30 each)
5. Solder wires to connect components (30 min per module)
6. Flash firmware to each ESP32 (5 min each)
7. Test each module (5 min each)

**Total time for 10 modules: 8-10 hours**
**Total cost for 10 modules: £150-200**

### Then Scale To: Option C (Factory Assembled)

Once you have 50+ orders, contact Makerfabs:
1. Send them the module design
2. They assemble in bulk
3. Lower per-unit cost
4. Higher margin

### Eventually: Option D (Custom PCB)

Once you have 100+ orders per month:
1. Design custom PCB (HeyPCB or KiCad)
2. Factory assembles everything
3. Premium product
4. Highest margin

---

## The Path

```
START: Option B (Snap-Fit Kit)
  ↓ Test market, get 50 orders
SCALE: Option C (Factory Assembled)
  ↓ Get 100+ orders per month
PREMIUM: Option D (Custom PCB)
  ↓ Premium product line
```

**Start with Option B. It's the easiest to build and test.**
