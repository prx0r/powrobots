# Glimlings: Product Strategy & Manufacturing Route

## Product Structure

| Option | Role | Price | Why |
|--------|------|-------|-----|
| **A: DIY Kit** | Educational product | £29.99 | Hobbyists only, too many steps for gifts |
| **B: Snap-Fit Kit** | Secondary product, initial pilot | £39.99 | Low assembly, easy to personalise |
| **C: Assembled** | **Main consumer product** | **£59.99** | Ready to use, tested, gift-ready |
| **D: Custom PCB** | Manufacturing method, not a tier | £79.99 | Simplifies assembly, doesn't justify £20 premium |

### Proposed Main Product: £59.99

Personalised, fully assembled Glimling. Your choice of character, colour, name and personality. USB-powered, preconfigured and tested before dispatch.

---

## The Fifth Option: Off-the-Shelf Electronics Module

Before commissioning a custom PCB, use an existing assembled module.

### M5Stack AtomS3R AI Chatbot Kit — $21.50

- ESP32-S3
- 0.85-inch colour display
- Microphone
- Speaker
- Button
- 8 MB PSRAM
- **In stock**

**Source:** https://shop.m5stack.com/products/atoms3r-ai-chatbot-kit-8mb-psram

### M5Stack Atom Voice — $13.50

- ESP32
- Integrated speaker
- Microphone
- RGB LED
- Button
- **No display**

**Source:** https://shop.m5stack.com/products/atom-echo-smart-speaker-dev-kit

### Seeed XIAO + Round Display — ~$26.49

- ESP32-S3 ($8.49)
- 1.28" round touchscreen ($18)
- Pre-soldered, plugs together, no soldering

**Source:** https://www.seeedstudio.com/XIAO-Series-and-accessories.html

### Why This Works

- $21.50 for complete electronics (display, mic, speaker, button)
- Design character enclosure around it
- Flash your own firmware
- No PCB design needed
- Test the product before investing in custom electronics

---

## Two-Stage Manufacturing Route

### Stage 1: First 5–10 Glimlings

**Preassembled electronics + custom printed shell**

1. Use M5Stack module with your own firmware and animated character
2. Design two-piece enclosure that accepts the complete module
3. Leave USB-C port accessible
4. Order one-off shells from JLC3DP
5. Flash, assemble, test, package
6. Sell a handful before taking general orders

**Cost:**
- M5Stack module: $21.50 (~£17)
- Enclosure (JLC3DP): $1-5 (~£2)
- Packaging: £3
- Shipping: £3.50
- **Total: ~£25-28**
- **Retail: £59.99**
- **Margin: ~55%**

### Stage 2: Repeatable Production

**One custom PCB, interchangeable character shells**

1. Commission populated board from JLCPCB
2. One electronics core shared across family of characters
3. Desk Goblins share display-and-audio board
4. Plant Sprites share sensor board
5. Every character doesn't need its own electronics design

**JLCPCB Economic PCBA Pricing:**
- $8.18 order setup
- $1.53 stencil
- Components + assembly fees
- Batch production amortises fixed charges

---

## Fulfilment Partners

| Provider | Application |
|----------|-------------|
| **Makerfabs** | PCB assembly, mechanical parts, testing, packaging, dropshipping |
| **PCBWay** | Full box-build quotation (PCB + BOM + enclosure + assembly) |
| **Slant 3D** | API-driven, made-to-order 3D printing with direct fulfilment |

---

## Real Margin Check

### UK Etsy Fees

| Fee | Amount |
|-----|--------|
| Transaction fee | 6.5% |
| Payment processing | 4% + £0.20 |
| Listing fee | £0.15 |
| **Total fees** | **~11% + £0.35** |

### At £59.99 Retail

| Item | Amount |
|------|--------|
| Retail price | £59.99 |
| Etsy fees (~11%) | -£6.95 |
| **Net revenue** | **£53.04** |
| Manufacturing cost | -£25-28 |
| **Profit** | **£25-28** |
| **Margin** | **~47%** |

### What £25-28 Manufacturing Must Cover

- PCB/electronics module
- Enclosure (3D printed)
- Firmware programming
- Functional testing
- Packaging
- Inbound freight
- Rejects/returns

---

## Compliance Requirements (UK)

| Requirement | What It Means |
|-------------|---------------|
| **Radio equipment** | Wi-Fi enabled device must comply |
| **RoHS** | Restriction of hazardous substances |
| **WEEE** | Waste electrical equipment registration |
| **Connected product security** | May apply to IoT devices |

**Resolve these before taking consumer orders.**

---

## The Milestone

**One finished, USB-powered Desk Goblin using off-the-shelf M5Stack core and your own printed shell.**

Measure:
1. Actual assembly time
2. Actual test time
3. Second enclosure variation
4. Full fulfilment quote

**That tells you whether £59.99 is commercially viable before committing to custom PCB.**

---

## Summary

| Stage | What | Cost | Timeline |
|-------|------|------|----------|
| **Stage 1** | M5Stack + custom shell | ~£25-28 | 1-2 weeks |
| **Stage 2** | Custom PCB + shells | ~£15-20 | 4-6 weeks |
| **Scale** | Factory assembly | ~£10-15 | 8-12 weeks |

**Start with Stage 1. Test demand. Then invest in custom PCB.**
