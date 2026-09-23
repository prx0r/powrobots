# Database Schema for Glimlings Frontend

## Tables

### products
Available characters and bundles.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Auto-increment |
| slug | TEXT UNIQUE | sporebert, mosswick |
| name | TEXT | Sporebert |
| character_type | TEXT | mushroom, frog, ghost, cloud |
| category | TEXT | desk, garden, night, weather |
| description | TEXT | Product description |
| created_at | TIMESTAMP | Creation date |

### materials
Shell material options.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Auto-increment |
| slug | TEXT UNIQUE | mjf-nylon, sla-resin |
| name | TEXT | Standard Matte |
| finish | TEXT | matte, smooth, coloured, translucent |
| cost_gbp | DECIMAL | Our cost |
| print_time_hours | INTEGER | Production time |
| notes | TEXT | Additional info |

### product_variants
Available combinations of product + material.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Auto-increment |
| product_id | INTEGER FK | References products |
| material_id | INTEGER FK | References materials |
| price_gbp | DECIMAL | UK price |
| price_usd | DECIMAL | US price |
| price_eur | DECIMAL | EU price |
| price_aud | DECIMAL | AU price |
| in_stock | BOOLEAN | Availability |

### customisations
Customer customisation options.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Auto-increment |
| product_id | INTEGER FK | References products |
| option_type | TEXT | colour, name, expression |
| option_name | TEXT | "Purple", "Happy" |
| option_value | TEXT | "#8B00FF", "smile" |
| additional_cost_gbp | DECIMAL | Extra cost (default 0) |

### hardware
Compatible electronic modules.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Auto-increment |
| slug | TEXT UNIQUE | atom-voice, atom-voices3r |
| name | TEXT | M5Stack Atom Voice |
| manufacturer | TEXT | M5Stack |
| chip | TEXT | ESP32, ESP32-S3 |
| dimensions | TEXT | 24x24x17mm |
| features | TEXT | mic, speaker, led, button, grove |
| buy_url_uk | TEXT | Link to UK retailer |
| buy_url_us | TEXT | Link to US retailer |
| buy_url_eu | TEXT | Link to EU retailer |
| buy_url_au | TEXT | Link to AU retailer |
| price_uk_gbp | DECIMAL | UK price |
| price_us_usd | DECIMAL | US price |
| price_eu_eur | DECIMAL | EU price |
| price_au_aud | DECIMAL | AU price |

### countries
Supported sales regions.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Auto-increment |
| code | TEXT UNIQUE | GB, US, DE, AU |
| name | TEXT | United Kingdom |
| currency | TEXT | GBP, USD, EUR, AUD |
| radio_frequency | TEXT | 868MHz, 915MHz, 433MHz |
| plug_type | TEXT | Type G, Type A/B, Type C/F, Type I |
| compliance | TEXT | UKCA, FCC, CE, RCM |
| shipping_cost_gbp | DECIMAL | Shipping cost |
| etsy_fees_percent | DECIMAL | Platform fees |
| domain | TEXT | uk.glimlings.app |

### orders
Customer orders.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Auto-increment |
| customer_email | TEXT | Customer email |
| country_code | TEXT FK | References countries |
| status | TEXT | pending, printing, assembling, shipped, delivered |
| product_variant_id | INTEGER FK | References product_variants |
| customisation_json | TEXT | Selected options (JSON) |
| total_gbp | DECIMAL | Total in GBP |
| total_local | DECIMAL | Total in local currency |
| currency | TEXT | GBP, USD, EUR, AUD |
| shipping_address | TEXT | Delivery address |
| tracking_number | TEXT | Shipment tracking |
| created_at | TIMESTAMP | Order date |
| shipped_at | TIMESTAMP | Ship date |

### firmware
Firmware versions for each hardware.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Auto-increment |
| hardware_id | INTEGER FK | References hardware |
| version | TEXT | 1.0.0 |
| changelog | TEXT | Version notes |
| download_url | TEXT | Download link |
| compatible_agents | TEXT | muse, chatgpt, home-assistant |
| created_at | TIMESTAMP | Release date |

### mcp_integrations
Supported AI agent connections.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Auto-increment |
| agent_name | TEXT | muse, chatgpt, home-assistant |
| agent_type | TEXT | ai-agent, smart-home |
| integration_method | TEXT | mcp, webhook, mqtt |
| status | TEXT | verified, beta, planned |
| documentation_url | TEXT | Setup guide |
| notes | TEXT | Additional info |

### inventory
Stock levels at printing partner.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Auto-increment |
| product_variant_id | INTEGER FK | References product_variants |
| country_code | TEXT | GB, US, DE, AU |
| quantity_available | INTEGER | In stock |
| quantity_reserved | INTEGER | Pending orders |
| last_synced_at TIMESTAMP | Last inventory sync |

---

## Key Relationships

```
products ──→ product_variants (one product, many material options)
product_variants ──→ customisations (one variant, many custom options)
products ──→ firmware (one product, many firmware versions)
hardware ──→ firmware (one hardware, many firmware versions)
orders ──→ product_variants (one order, one variant)
orders ──→ countries (one order, one country)
mcp_integrations ──→ firmware (one agent, many firmware versions)
inventory ──→ product_variants (one variant, many countries)
```

---

## Sample Data

### products

| id | slug | name | character_type | category |
|----|------|------|----------------|----------|
| 1 | sporebert | Sporebert | mushroom | desk |
| 2 | mosswick | Mosswick | frog | garden |
| 3 | boo-bloom | Boo Bloom | ghost | night |
| 4 | nimbus | Nimbus | cloud | weather |

### materials

| id | slug | name | finish | cost_gbp |
|----|------|------|--------|----------|
| 1 | mjf-nylon | Standard Matte | matte | 2.00 |
| 2 | sla-resin | Premium Smooth | smooth | 3.00 |
| 3 | sla-coloured | Deluxe Full Colour | coloured | 5.00 |
| 4 | sla-translucent | Special Glow-Through | translucent | 4.00 |

### hardware

| id | slug | name | chip | price_uk_gbp |
|----|------|------|------|--------------|
| 1 | atom-voice | M5Stack Atom Voice | ESP32 | 13.00 |
| 2 | atom-voices3r | M5Stack Atom VoiceS3R | ESP32-S3 | 13.90 |

### countries

| id | code | name | currency | radio | plug | domain |
|----|------|------|----------|-------|------|--------|
| 1 | GB | United Kingdom | GBP | 868MHz | Type G | uk.glimlings.app |
| 2 | US | United States | USD | 915MHz | Type A/B | us.glimlings.app |
| 3 | DE | Germany | EUR | 868MHz | Type C/F | eu.glimlings.app |
| 4 | AU | Australia | AUD | 433MHz | Type I | au.glimlings.app |
