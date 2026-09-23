# Glimlings.app — The Full Product Vision

## The Ecosystem

```
PHYSICAL PRODUCT (Glimling)
    ↓
DIGITAL COMPANION (glimlings.app)
    ↓
AI AGENT (Muse integration)
    ↓
MARKETPLACE (accessories, customisation)
    ↓
SOCIAL (gifting, sharing, community)
```

## The Customer Journey

1. **BUY** — Customer buys Glimling (Etsy/website)
2. **UNBOX** — Receive physical product
3. **SETUP** — Go to glimlings.app, connect to WiFi
4. **PAIR** — Connect to Muse/ChatGPT
5. **CUSTOMISE** — Choose features, enable MCP tools
6. **OWN** — Register ownership, get digital identity
7. **UPGRADE** — Buy accessories, unlock features
8. **GIFT** — Design one for a friend
9. **COLLECT** — Build a family of Glimlings

---

## glimlings.app Features

### Setup
- Connect Glimling to WiFi
- Register device to account
- Choose character and name
- Set initial preferences

### Ownership
- Digital certificate of ownership
- NFT-style collectibility (optional)
- Device history and milestones
- Transfer ownership to new owner

### Customisation
- Choose which MCP tools to enable
- Set alert preferences
- Customise LED behaviour
- Upload custom faces/animations

### Marketplace
- Buy accessories (sensors, enclosures)
- Unlock premium features
- Design custom enclosures
- Buy gifts for friends

### Social
- Share Glimling photos
- Gift a Glimling to someone
- Join Glimling community
- Trade/sell Glimlings

### AI Integration
- Connect to Muse
- Connect to ChatGPT
- Choose which AI agent
- Set AI personality

---

## Firmware: Enable/Disable MCP Features

**YES — this is easy on ESP32-S3.**

The firmware is modular. Features can be enabled/disabled via configuration stored in flash memory.

### Configuration File (Stored in Flash)

```json
{
  "wifi": {"ssid": "MyWiFi", "password": "..."},
  "mcp": {
    "enabled": true,
    "port": 8080,
    "tools": ["get_moisture", "get_light", "set_led"]
  },
  "features": {
    "led": true,
    "display": false,
    "buzzer": false,
    "camera": false,
    "encoder": false
  },
  "alerts": {
    "low_moisture": true,
    "low_light": false,
    "temperature_extreme": true
  },
  "ai": {
    "agent": "muse",
    "personality": "friendly",
    "check_interval": 300
  }
}
```

### Customer Chooses at Setup

1. Which sensors to enable
2. Which alerts to receive
3. Which AI agent to connect
4. Which MCP tools to expose
5. Which features to activate

### Firmware Responds

- Only loads enabled modules
- Only exposes enabled tools
- Only sends enabled alerts
- Saves battery by disabling unused features

---

## Freak Town-Style Ownership

### Digital Identity
- Each Glimling has unique ID
- Registered to owner's account
- Digital certificate of ownership
- Can transfer ownership
- Can sell/trade

### Collectibility
- Limited edition characters
- Rare colour variants
- Special event Glimlings
- Collector badges

### NFT-Style (Optional)
- Blockchain verification
- Provable ownership
- Transferable identity
- NOT required for basic use

---

## Accessories & Upgrades

| Accessory | Description | Price |
|-----------|-------------|-------|
| Extra Sensors | Soil probe, temp sensor, light sensor | £5-15 |
| Enclosures | Different character shells | £10-20 |
| Stands | Desk stand, wall mount, garden stake | £5-10 |
| Batteries | Portable power bank | £15-25 |
| Camera Module | Add vision to any Glimling | £20-30 |
| Speaker Module | Add voice to any Glimling | £15-25 |
| Premium Firmware | Advanced AI features | £5-10/month |

---

## Gifting & Social

### Gift a Glimling

1. Go to glimlings.app/gift
2. Choose character
3. Customise (name, colour, features)
4. Add personal message
5. Pay
6. Recipient receives:
   - Physical Glimling
   - Digital ownership
   - Personal message
   - Setup instructions

### Design for a Friend

1. Go to glimlings.app/design
2. Choose engine (SENSE, ACT, etc.)
3. Design character
4. Preview in 3D
5. Order for friend
6. Friend receives custom Glimling

### Discounts

- First Glimling: Full price
- Second Glimling: 10% off
- Third Glimling: 15% off
- Family pack (4+): 20% off
- Referral: £5 off for both

---

## Revenue Streams

### 1. Hardware Sales
- Glimlings: £44.99-69.99
- Accessories: £5-30
- Enclosures: £10-20

### 2. Subscription (Optional)
- Basic: Free (basic alerts)
- Plus: £4.99/month (advanced AI)
- Pro: £9.99/month (full features)

### 3. Marketplace
- Creator commissions: 10%
- Premium designs: £5-15
- Limited editions: £50-100

### 4. Gifts
- Gift cards: £25-100
- Custom designs: £5-15 extra
- Express shipping: £5

### Monthly Revenue (1000 Users)

| Stream | Revenue |
|--------|---------|
| Hardware | £50,000 |
| Subscriptions | £5,000 |
| Marketplace | £2,000 |
| Gifts | £3,000 |
| **Total** | **£60,000/month** |

---

## The Vision

**Glimlings aren't just products. They're companions.**

- Physical product meets digital experience
- AI-powered, personalised, collectible
- Community-driven, gift-worthy, upgradeable
- MCP-integrated, smart, connected

**This is the future of consumer electronics.**
