# Actual Supplier: M5Stack, Waveshare, and the Glimling Electronic Heart

## The Fit

M5Stack is a very good fit for Glimlings' first prototypes. It already sells tiny voice-capable computers with a microphone, speaker, button, LED and expansion port. You can buy them individually, put them inside your own character shells and develop the voice integration without first commissioning a custom PCB.

However, test M5Stack alongside one Waveshare board before choosing the production hardware. M5Stack offers an exceptionally compact starting point; Waveshare offers considerably more audio and lighting hardware for a similar component price.

---

## 1. Can You Order Just One? What Does Shipping Cost?

### M5Stack Atom Voice — $13.50 direct

M5Stack's official store lists the C008-C with stock available and no minimum quantity. Dimensions: 24 × 24 × 17 mm.

| Buying Route | Price | Delivery |
|--------------|-------|----------|
| M5Stack direct | $13.50 each | Standard international: 15-20 business days; DHL: 3-5 days |
| The Pi Hut, UK | £13 inc VAT + £3.80 shipping | 1-2 days after dispatch |

The official M5Stack store does not publish a universal shipping price. Destination-specific checkout quote required.

---

## 2. Which Voice Board Should Become the Glimling's Electronic Heart?

| Board | Price | Main Advantage | Limitation |
|-------|-------|----------------|------------|
| M5Stack Atom Voice | $13.50 | Tiny, complete voice unit with RGB LED and Grove port | Older ESP32 without PSRAM |
| M5Stack Atom VoiceS3R | $14.50 | ESP32-S3, 8MB PSRAM, microphone and speaker | No integrated RGB LED; sold out |
| M5Stack AtomS3R AI Chatbot Kit | $21.50 | ESP32-S3 voice kit with additional sensors and screen | Includes unnecessary hardware |
| Waveshare ESP32-S3 Audio Board | $15.99-$17.99 | Dual microphones, seven RGB LEDs, RTC, 8MB PSRAM | Larger board; speaker through separate header |
| Seeed reSpeaker Lite | $30.99 | Dedicated XMOS voice processing, dual microphones | More expensive; speaker is additional |

### Two Boards Worth Testing Side by Side

**M5Stack Atom Voice:** Test how small and charming the Glimling can be. Speaker, microphone, light and button packaged into a very compact unit.

**Waveshare audio board:** Test the more ambitious version with richer lighting, dual microphones, a real-time clock and enough PSRAM for a more capable audio stack.

**Key detail:** The newer M5Stack VoiceS3R drops the original Voice's integrated RGB LED. We'd have to add our own illumination. The older Atom Voice is more immediately complete; the S3R is a more expandable processing platform.

---

## 3. Canonical Supplier List

| Supplier | Role | Quantity-one | Shipping |
|----------|------|--------------|----------|
| M5Stack | Compact voice cores, plug-in sensors | Yes | International: 15-20 days; DHL: 3-5 days |
| The Pi Hut | UK prototypes, replacement M5Stack | Yes | £3.80 UK, 1-2 days |
| Waveshare | Alternative audio boards, displays, cameras | Yes | Worldwide, freight varies |
| Seeed Studio | Higher-quality voice modules, Grove sensors | Yes | $15 postal, 12-45 days |
| LCSC | Components for future custom electronics | Part-dependent | Quote exact quantities |
| JLCPCB | Custom PCB fabrication and assembly | Small batches | 5 boards for $2, ~24hr production |
| JLC3DP | Interchangeable shells, heads, prototypes | Yes | Cost depends on geometry and material |
| PCBWay | Alternative printing, manufacturing comparison | Yes | $25 minimum, some SLA in 1 day |
| Makerfabs | Electronics assembly, programming, testing, fulfilment | One-piece prototypes | ~12 days PCBA, ~15 days small batch |
| AliExpress / 1688 | Commodity components, supplier discovery | Usually | Calculate landed price per seller |

### Three Suppliers to Contact Before Custom Electronics

**M5Stack** — Hardware and potential OEM production
- Ask for 10-, 50-, 100- and 500-unit prices
- Pre-flashing firmware
- Custom LED arrangement support
- Contact: sales@m5stack.com

**Makerfabs** — Single-package fulfilment
- Warehousing, packing, tracked dispatch, seller's brand
- No separate warehousing/dropshipping fee
- Ask: Can it purchase M5Stack boards, receive JLC3DP shells, flash firmware, test, ship?

**JLC3DP** — Custom character manufacturing
- Upload 3 standard shells + personalised design
- Get quotes for 1, 10, 50 copies
- Compare with PCBWay

---

## 4. First Working Glimling Prototype

### Minimal Voice + Character Prototype

| Part | Price |
|------|-------|
| M5Stack Atom Voice, C008-C | $13.50 |
| M5Stack PIR Motion Unit, U004 | $5.50 |
| M5Stack RGB LED Unit, U003 | $3.95 |
| M5Stack ENV III, U001-C | $5.95 (promo) |
| Personalised shell | Quote after design |
| **Total** | **~$29-35 + shell** |

Optional additions:
- Extra RGB unit (Atom Voice has one built-in)
- ENV III for temperature, humidity, pressure sensing
- Waveshare audio board for comparison

**Integration detail:** M5Stack's Grove expansion port is valuable but not unlimited. Connecting several sensors may require a hub. For first prototype, motion lives on Glimling, plant sensors communicate through existing gateways.

---

## 5. The Fulfilment Model

### Prototypes
- Order single boards from M5Stack or The Pi Hut
- Buy shells one at a time from JLC3DP
- No manufacturing commitment needed

### First Customer Orders
- Small inventory of tested electronic cores
- Standard character shells at one fulfilment location
- Print/personalise decorative parts to order
- Custom designs priced from actual quotes

### After Proven Demand
- Request M5Stack OEM pricing
- Compare with custom LCSC/JLCPCB electronics design
- Makerfabs becomes assembly/fulfilment partner

**Main complication:** Consolidation. Sending M5Stack board and printed shell separately is easy; delivering as one assembled, tested, giftable product requires inventory coordination. Get written per-order quotation from Makerfabs before building checkout around it.

---

## 6. The Manufacturing Decision

The compelling thing about M5Stack is that you can sell a unique physical design without immediately designing unique electronics. One proven electronic heart could fit a mushroom, ghost, frog, robot or customer-generated character.

**Avoid putting a retail development board into every production Glimling indefinitely.** You pay for manufacturer's packaging, connectors and distribution. A branded consumer device incorporating a pre-certified board is not automatically approved as a complete product.

**The first major test:** One functional, customised character with good microphone pickup, audible speech, attractive diffuse lighting, accessible controls and reliable connection to agent gateway.

The original Atom Voice offers a very inexpensive way to prove that experience; Waveshare and the S3R family give a useful route toward more capable hardware.
