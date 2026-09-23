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

-- Compatible sensors
CREATE TABLE sensors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    type TEXT,  -- plant, leak, environment, rain, water, co2, motion, sound, camera
    connection TEXT,  -- Bluetooth, 868MHz + Gateway, I2C, GPIO, Analog
    features TEXT,
    price_uk_gbp DECIMAL,
    price_us_usd DECIMAL,
    waterproof BOOLEAN DEFAULT 0,
    compatibility TEXT  -- POW Tested, Bridge Required, Community
);

-- Seed data: Sensors
INSERT INTO sensors (slug, name, type, connection, features, price_uk_gbp, price_us_usd, waterproof, compatibility) VALUES
-- Plant sensors
('hhcc-flower-care', 'HHCC Flower Care', 'plant', 'Bluetooth', 'moisture, temp, light, conductivity', 14.99, 17.99, 0, 'POW Tested'),
('miflora', 'MiFlora', 'plant', 'Bluetooth', 'moisture, temp, light', 12.99, 15.99, 0, 'POW Tested'),
('ecowitt-wh51', 'Ecowitt WH51', 'plant', '868MHz + Gateway', 'moisture', 14.50, 17.99, 1, 'Bridge Required'),
('ecowitt-wh52', 'Ecowitt WH52', 'plant', '868MHz + Gateway', 'moisture, temp, EC', 22.50, 27.99, 1, 'Bridge Required'),
-- Leak detection
('ecowitt-wh55', 'Ecowitt WH55', 'leak', '868MHz + Gateway', 'water leak detection', 12.99, 15.99, 0, 'Bridge Required'),
-- Environment
('dfrobot-sen0501', 'DFRobot SEN0501', 'environment', 'I2C/GPIO', 'temp, humidity, pressure, light, UV', 24.00, 29.90, 0, 'Community'),
-- Rain
('dfrobot-sen0575', 'DFRobot SEN0575', 'rain', 'Analog', 'rainfall', 25.00, 29.90, 1, 'Community'),
-- Water level
('seeed-grove-water-level', 'Seeed Grove Water Level', 'water', 'Analog', 'water level 0-10cm', 6.50, 7.99, 1, 'Community'),
-- CO2
('seeed-grove-scd41', 'Seeed Grove SCD41', 'co2', 'I2C', 'CO2, temp, humidity', 42.00, 52.90, 0, 'Community'),
-- Motion
('seeed-grove-pir', 'Seeed Grove PIR', 'motion', 'GPIO', 'motion detection', 7.00, 8.70, 0, 'Community'),
-- Sound
('dfrobot-sound-sensor', 'DFRobot Sound Sensor', 'sound', 'Analog', 'ambient sound level', 3.00, 3.50, 0, 'Community'),
-- Camera
('seeed-grove-vision-ai', 'Seeed Grove Vision AI', 'camera', 'I2C', 'image capture, basic AI', 35.00, 42.00, 0, 'Community');

-- Seed data: MCP Integrations
INSERT INTO mcp_integrations (agent_name, agent_type, integration_method, status) VALUES
('muse', 'ai-agent', 'mcp', 'planned'),
('chatgpt', 'ai-agent', 'mcp', 'planned'),
('home-assistant', 'smart-home', 'mcp', 'verified');
