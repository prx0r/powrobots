# MCP Integration — How It Works

## The Vision

Customer describes what they want → MCP validates, quotes, orders → Product ships

## The Three Integration Levels

### Level 1: Etsy (Manual) — START HERE

| Parameter | Value |
|-----------|-------|
| Description | List on Etsy, manually fulfill orders |
| Tech | Etsy listing + manual assembly |
| MCP | No MCP needed yet |
| Effort | Low |
| Scale | 10-50 orders/month |
| Cost | £0 (just time) |

### Level 2: Website (Automated) — SCALE HERE

| Parameter | Value |
|-----------|-------|
| Description | Custom website with MCP backend |
| Tech | Cloudflare Worker + MCP + Stripe |
| MCP | Full MCP integration |
| Effort | Medium |
| Scale | 50-500 orders/month |
| Cost | £5/month (Cloudflare) |

### Level 3: AI Agents (MCP) — FUTURE HERE

| Parameter | Value |
|-----------|-------|
| Description | Muse/ChatGPT can design and order |
| Tech | MCP server + AI agent integration |
| MCP | Full MCP + AI tools |
| Effort | High |
| Scale | Unlimited |
| Cost | £5/month + API costs |

---

## Start With Level 1 (Etsy)

### This Week

1. Create Etsy listing for Sporebert
2. Set price at £44.99
3. Write product description
4. Add photos (renders of design)
5. Enable custom orders (colour, name)

### When Order Comes In

1. Customer orders Sporebert (purple, named "Fungus")
2. We receive notification
3. We modify parametric template (colour=purple, name=Fungus)
4. Generate STL
5. Submit to JLC3DP
6. Order ESP32 + sensors from AliExpress
7. Assemble when parts arrive
8. Ship to customer
9. Update Etsy with tracking

**This is the simplest path. No MCP needed yet. Just manual fulfillment.**

---

## Level 2: Website (When Ready to Scale)

### Architecture

```
CUSTOMER (website)
    ↓
DESIGN MCP (Cloudflare Worker)
    ↓
Validates: Design fits constraints
    ↓
QUOTES: Parts + enclosure + shipping
    ↓
TAKES ORDER: Stripe payment
    ↓
ROUTING:
  - Enclosure → JLC3DP
  - Parts → AliExpress
  - Assembly → Us
  - Shipping → Royal Mail
    ↓
TRACKING: Updates customer
```

### Tech Stack

| Component | Technology | Cost |
|-----------|------------|------|
| API | Cloudflare Workers | Free tier |
| Database | Cloudflare D1 | Free tier |
| Storage | Cloudflare R2 | Free tier |
| Payments | Stripe | 2.9% + £0.20 |
| MCP | Effect + Alchemy | Free |

**Total: £5/month + Stripe fees**

---

## Level 3: AI Agents (Future)

### Muse/ChatGPT Integration

```
MUSE: "I want a garden monitor for my monstera"
    ↓
MCP: "Here are 3 options:
  1. Sporebert (£44.99) - mushroom design
  2. Mosswick (£44.99) - frog design
  3. Pebble (£44.99) - stone design"
    ↓
MUSE: "Sporebert, purple, named 'Monstera Mike'"
    ↓
MCP: "Quote: £44.99. Ships in 5-7 days."
    ↓
MUSE: "Approved"
    ↓
MCP: Orders and ships
```

**This is the vision. AI agents can design and order Glimlings.**

---

## MCP Tools Needed

### For Level 1 (Etsy)

No MCP needed. Just manual fulfillment.

### For Level 2 (Website)

| Tool | What It Does |
|------|--------------|
| `validate_design` | Check if design fits constraints |
| `calculate_cost` | Estimate print cost based on volume |
| `get_quote` | Return itemised quote |
| `place_order` | Submit order to suppliers |
| `track_order` | Check order status |

### For Level 3 (AI Agents)

| Tool | What It Does |
|------|--------------|
| `list_products` | Show available Glimlings |
| `customise_product` | Modify colour, name, features |
| `validate_customisation` | Check if customisation fits |
| `get_quote` | Return price for custom design |
| `place_order` | Order custom Glimling |
| `track_order` | Check delivery status |

---

## The Path

```
NOW: Level 1 (Etsy, manual)
  → List Sporebert
  → Get first 10 orders
  → Learn fulfillment process

NEXT: Level 2 (Website, automated)
  → Build Cloudflare Worker
  → Add Stripe payments
  → Automate ordering

FUTURE: Level 3 (AI agents, MCP)
  → Connect Muse/ChatGPT
  → Let AI design and order
  → Scale to unlimited
```

---

## The Simplest Path (Level 1)

1. **List Sporebert on Etsy** — £44.99
2. **Get first order** — Manually fulfill
3. **Learn the process** — Document what works
4. **Iterate** — Improve based on feedback
5. **Scale** — Add website when ready

**Don't build MCP yet. Just sell on Etsy first.**
