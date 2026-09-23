# Shell-Only Glimlings: The Simpler Business

## The Core Offer

**"Design a home for your AI agent."**

The customer buys a personalised Glimling shell from Etsy and a compatible M5Stack voice module from whichever supplier offers the best delivered price. The shell arrives ready to clip around the electronics. They install firmware, connect their agent and choose what their Glimling can do.

**This eliminates:** electronics inventory, multi-supplier assembly, device testing, most logistics.

---

## The New Supply Chain

```
Customer designs Glimling in POW Studio
    ↓
Order 1: Etsy shop → Printing partner → Customer
Order 2: Electronics retailer → Customer
    ↓
Customer clips them together
    ↓
Installs firmware, pairs device, chooses personality
```

**No Makerfabs, no electronics inventory, no custom PCB, no factory assembly.**

The catch: customer receives two parcels, potentially on different dates. Acceptable for maker-friendly product, less convenient as gift.

---

## 1. Actual Suppliers

| Supplier | Responsibility | Why |
|----------|----------------|-----|
| M5Stack | Voice modules | Atom Voice $13.50, available individually |
| The Pi Hut | UK electronics option | Atom Voice £13 inc VAT |
| Craftcloud | Global shell manufacturing | No minimum, UK partners, direct shipping |
| JLC3DP | Specialist shells | Translucent resin, SLA, MJF |
| Makr3D | Potential UK Etsy fulfilment | Etsy integration, white-label packing |

**For first 10 orders:** Submit approved files manually to print supplier. No automated manufacturing integrations needed yet.

**Etsy permits** third-party production of original designs, including print-on-demand, with proper disclosure.

---

## 2. Start With One Electronics Module

### M5Stack Atom Voice, C008-C

- 24 × 24 × 17 mm
- Microphone, 0.8W speaker, RGB LED, button, Grove port
- Manufacturer publishes dimensions, interfaces, mounting details

**Design first character around complete, unmodified M5Stack enclosure.** Shell clips around it, preserving speaker, microphone, LED, button, power connector.

**Support other boards through separately validated mounting inserts later.**

---

## 3. Shell-Only Margins

### Illustrative £24.99 Shell

| Item | Amount |
|------|--------|
| Retail price | £24.99 |
| Printed shell | -£6.00 |
| Customer delivery | -£3.75 |
| Packaging | -£0.75 |
| Returns/reprint allowance | -£1.00 |
| Etsy fees (UK) | -£3.10 |
| **Contribution** | **£10.39** |

**~42% contribution before marketing and VAT.**

If VAT-registered and costs are net of recoverable VAT: ~£6.22 contribution.

If actual shell costs £12 instead of £6: economics deteriorate sharply.

**Crucial number: price of printing and delivering one specific shell, not advertised minimum per gram.**

---

## 4. Make Studio Compatible With Existing Hardware

| Customer Selection | Studio Behaviour |
|--------------------|------------------|
| Atom Voice | Display tested compatible characters and features |
| Atom VoiceS3R | Display tested mounting variants and abilities |
| Other modules | Show only validated models; offer experimental mode |
| No electronics yet | Explain required module, show suppliers by region |

**Opens additional market:** People who already own M5Stack or Home Assistant hardware and want attractive enclosure.

**Software matters just as much:** Free setup page that identifies board, installs firmware, configures Wi-Fi, pairs character. Basic lighting and button work without cloud.

---

## 5. First Catalogue

| Offering | Price | Description |
|----------|-------|-------------|
| Standard character | £19.99-24.99 | Approved design, standard material |
| Personalised character | £29.99-39.99 | Custom colour, name, face, features |
| Artist edition | Individually quoted | Complex geometry, detailed painting |
| Digital print file | £4.99-9.99 | Validated file for 3D printer owners |

---

## 6. The Biggest Trade-Off

Shell-only eliminates manufacturing complexity but shifts work onto customer.

- **Hobbyist:** Delighted to buy electronics separately and install firmware
- **Christmas gift buyer:** May not have used an ESP32

**Solution:** Shell-only as first offering, complete gift kit after design/onboarding proven.

---

## Etsy Boundary

- Don't redirect Etsy transactions to own checkout
- Sell shell as complete shell-only purchase
- State electronics not included
- Provide accurate compatibility information
- Independent website maintains broader catalogue

---

## The Vision

**An open library of beautiful, customisable physical bodies for existing AI hardware, with a shared personality and agent software layer.**

This is much closer to the business you're describing. It also provides a natural starting point for POW's longer-term compatibility, manufacturing and supplier intelligence.
