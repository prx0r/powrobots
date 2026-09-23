# POW Garden Familiars — First Consumer Product

Personalised garden creatures that talk to your AI.

---

## Three product tiers

| Version | What customer gets | Price |
|---------|-------------------|-------|
| **Garden Friend** | Personalised creature + plant label + NFC identity + manual watering journal. No battery. | $15-24 |
| **Garden Familiar** | Connected creature with moisture readings + Wi-Fi notifications | $39-49 |
| **Garden Familiar Outdoor+** | Weatherproof, outdoor probe, battery, extra sensing | $59-69 |

---

## The creatures

| Name | Character | Price | Best for |
|------|-----------|-------|----------|
| Sir Hopsalot | Frog | $39 | Tomatoes, vegetables |
| Sporebert | Mushroom | $39 | Herbs, houseplants |
| Boo Bloom | Ghost | $35 | Gifting |
| Dewdrop | Dragon | $39 | Succulents |
| Owlsworth | Owl | $39 | Seed trays |
| Bumble | Bee | $39 | Balcony flowers |
| Shelly | Tortoise | $39 | Succulents |
| Gnomeo | Gnome | $39 | Vegetable beds |

---

## Physical specification

**Above soil:** 55-70mm decorative character
**Below soil:** 80-120mm moisture probe
**Interface:** One button + one LED
**Power:** Replaceable batteries (3xAA proposed)

---

## Components (from our graph)

### Indoor version (Garden Familiar)
| Component | Source | Price |
|-----------|--------|-------|
| ESP32-C3-WROOM-02 | LCSC | $2.44 (100 units) |
| Capacitive Soil Sensor | DFRobot SEN0193 | $5.90 |
| WS2812B LED | Alibaba | $0.30 |
| Push Button | Alibaba | $0.50 |
| 3xAA Battery Holder | Alibaba | $0.80 |
| USB-C (charging) | Alibaba | $1.00 |
| PCB Assembly | JLCPCB | $8.18 setup |

### Outdoor version (Garden Familiar Outdoor+)
| Component | Source | Price |
|-----------|--------|-------|
| All indoor components | — | above |
| DFRobot SEN0308 outdoor probe | DFRobot | $14.90 |
| ASA enclosure | JLC3DP | quote |
| IP65 gasket | — | TBD |

---

## Waterproofing approach

**Two-piece design:**
1. **Sealed electronics capsule** — IP65 rated, elastomer gasket, weatherproof cable exit
2. **Decorative character shell** — UV-resistant ASA, holes allowed, sheds water away from capsule

**The shell is not the waterproof barrier.** The capsule inside is.

---

## Manufacturing

| Process | Provider | Cost |
|---------|----------|------|
| PCB assembly | JLCPCB | $8.18 setup + per-unit |
| Enclosure (indoor) | JLC3DP SLA/MJF | quote by design |
| Enclosure (outdoor) | JLC3DP ASA | quote by design |
| Final assembly | Manual | included in COGS |

---

## What our graph provides

| Data | Status |
|------|--------|
| ESP32-C3 component | In graph ($2.44 LCSC) |
| Soil moisture sensor | In graph ($5.90 DFRobot) |
| LED | In graph ($0.30 Alibaba) |
| Button | In graph ($0.50 Alibaba) |
| Battery holder | In graph ($0.80 Alibaba) |
| Outdoor probe | In graph ($14.90 DFRobot) |
| PCB assembly | In graph (JLCPCB $8.18) |
| Enclosure | In graph (JLC3DP) |
| **Total indoor BOM** | **~$14-20** |
| **Total outdoor BOM** | **~$29-35** |
