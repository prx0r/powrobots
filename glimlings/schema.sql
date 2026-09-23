-- Glimlings Database Schema
-- For glimlings.app frontend

-- Products (characters and bundles)
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    character_type TEXT,  -- mushroom, frog, ghost, cloud
    category TEXT,  -- desk, garden, night, weather
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Materials (shell options)
CREATE TABLE materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    finish TEXT,  -- matte, smooth, coloured, translucent
    cost_gbp DECIMAL,
    print_time_hours INTEGER,
    notes TEXT
);

-- Product variants (product + material combinations)
CREATE TABLE product_variants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER REFERENCES products(id),
    material_id INTEGER REFERENCES materials(id),
    price_gbp DECIMAL,
    price_usd DECIMAL,
    price_eur DECIMAL,
    price_aud DECIMAL,
    in_stock BOOLEAN DEFAULT 1
);

-- Customisations (colour, name, expression)
CREATE TABLE customisations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER REFERENCES products(id),
    option_type TEXT,  -- colour, name, expression
    option_name TEXT,
    option_value TEXT,
    additional_cost_gbp DECIMAL DEFAULT 0
);

-- Hardware (compatible electronics)
CREATE TABLE hardware (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    manufacturer TEXT,
    chip TEXT,
    dimensions TEXT,
    features TEXT,
    buy_url_uk TEXT,
    buy_url_us TEXT,
    buy_url_eu TEXT,
    buy_url_au TEXT,
    price_uk_gbp DECIMAL,
    price_us_usd DECIMAL,
    price_eu_eur DECIMAL,
    price_au_aud DECIMAL
);

-- Countries (sales regions)
CREATE TABLE countries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    currency TEXT,
    radio_frequency TEXT,
    plug_type TEXT,
    compliance TEXT,
    shipping_cost_gbp DECIMAL,
    etsy_fees_percent DECIMAL,
    domain TEXT
);

-- Orders
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_email TEXT,
    country_code TEXT REFERENCES countries(code),
    status TEXT DEFAULT 'pending',
    product_variant_id INTEGER REFERENCES product_variants(id),
    customisation_json TEXT,
    total_gbp DECIMAL,
    total_local DECIMAL,
    currency TEXT,
    shipping_address TEXT,
    tracking_number TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    shipped_at TIMESTAMP
);

-- Firmware versions
CREATE TABLE firmware (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hardware_id INTEGER REFERENCES hardware(id),
    version TEXT,
    changelog TEXT,
    download_url TEXT,
    compatible_agents TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- MCP integrations
CREATE TABLE mcp_integrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_name TEXT,
    agent_type TEXT,
    integration_method TEXT,
    status TEXT,
    documentation_url TEXT,
    notes TEXT
);

-- Inventory
CREATE TABLE inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_variant_id INTEGER REFERENCES product_variants(id),
    country_code TEXT,
    quantity_available INTEGER DEFAULT 0,
    quantity_reserved INTEGER DEFAULT 0,
    last_synced_at TIMESTAMP
);

-- Seed data: Products
INSERT INTO products (slug, name, character_type, category) VALUES
('sporebert', 'Sporebert', 'mushroom', 'desk'),
('mosswick', 'Mosswick', 'frog', 'garden'),
('boo-bloom', 'Boo Bloom', 'ghost', 'night'),
('nimbus', 'Nimbus', 'cloud', 'weather');

-- Seed data: Materials
INSERT INTO materials (slug, name, finish, cost_gbp) VALUES
('mjf-nylon', 'Standard Matte', 'matte', 2.00),
('sla-resin', 'Premium Smooth', 'smooth', 3.00),
('sla-coloured', 'Deluxe Full Colour', 'coloured', 5.00),
('sla-translucent', 'Special Glow-Through', 'translucent', 4.00);

-- Seed data: Hardware
INSERT INTO hardware (slug, name, manufacturer, chip, dimensions, price_uk_gbp, price_us_usd) VALUES
('atom-voice', 'M5Stack Atom Voice', 'M5Stack', 'ESP32', '24x24x17mm', 13.00, 13.50),
('atom-voices3r', 'M5Stack Atom VoiceS3R', 'M5Stack', 'ESP32-S3', '24x24x17mm', 13.90, 14.50);

-- Seed data: Countries
INSERT INTO countries (code, name, currency, radio_frequency, plug_type, compliance, shipping_cost_gbp, domain) VALUES
('GB', 'United Kingdom', 'GBP', '868MHz', 'Type G', 'UKCA, PSTI', 3.50, 'uk.glimlings.app'),
('US', 'United States', 'USD', '915MHz', 'Type A/B', 'FCC', 8.00, 'us.glimlings.app'),
('DE', 'Germany', 'EUR', '868MHz', 'Type C/F', 'CE, RoHS', 6.00, 'eu.glimlings.app'),
('AU', 'Australia', 'AUD', '433MHz', 'Type I', 'RCM', 12.00, 'au.glimlings.app');

-- Seed data: MCP Integrations
INSERT INTO mcp_integrations (agent_name, agent_type, integration_method, status) VALUES
('muse', 'ai-agent', 'mcp', 'planned'),
('chatgpt', 'ai-agent', 'mcp', 'planned'),
('home-assistant', 'smart-home', 'mcp', 'verified');
