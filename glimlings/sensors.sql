-- Compatible Sensors for Glimlings
-- From canonical documentation

-- Plant Sensors
INSERT INTO sensors (slug, name, type, connection, features, price_uk_gbp, price_us_usd, waterproof, compatibility) VALUES
('hhcc-flower-care', 'HHCC Flower Care', 'plant', 'Bluetooth', 'moisture, temp, light, conductivity', 14.99, 17.99, 0, 'POW Tested'),
('miflora', 'MiFlora', 'plant', 'Bluetooth', 'moisture, temp, light', 12.99, 15.99, 0, 'POW Tested'),
('ecowitt-wh51', 'Ecowitt WH51', 'plant', '868MHz + Gateway', 'moisture', 14.50, 17.99, 1, 'Bridge Required'),
('ecowitt-wh52', 'Ecowitt WH52', 'plant', '868MHz + Gateway', 'moisture, temp, EC', 22.50, 27.99, 1, 'Bridge Required');

-- Leak Detection
INSERT INTO sensors (slug, name, type, connection, features, price_uk_gbp, price_us_usd, waterproof, compatibility) VALUES
('ecowitt-wh55', 'Ecowitt WH55', 'leak', '868MHz + Gateway', 'water leak detection', 12.99, 15.99, 0, 'Bridge Required');

-- Environment
INSERT INTO sensors (slug, name, type, connection, features, price_uk_gbp, price_us_usd, waterproof, compatibility) VALUES
('dfrobot-sen0501', 'DFRobot SEN0501', 'environment', 'I2C/GPIO', 'temp, humidity, pressure, light, UV', 24.00, 29.90, 0, 'Community');

-- Rain
INSERT INTO sensors (slug, name, type, connection, features, price_uk_gbp, price_us_usd, waterproof, compatibility) VALUES
('dfrobot-sen0575', 'DFRobot SEN0575', 'rain', 'Analog', 'rainfall', 25.00, 29.90, 1, 'Community');

-- Water Level
INSERT INTO sensors (slug, name, type, connection, features, price_uk_gbp, price_us_usd, waterproof, compatibility) VALUES
('seeed-grove-water-level', 'Seeed Grove Water Level', 'water', 'Analog', 'water level 0-10cm', 6.50, 7.99, 1, 'Community');

-- CO2
INSERT INTO sensors (slug, name, type, connection, features, price_uk_gbp, price_us_usd, waterproof, compatibility) VALUES
('seeed-grove-scd41', 'Seeed Grove SCD41', 'co2', 'I2C', 'CO2, temp, humidity', 42.00, 52.90, 0, 'Community');

-- Motion
INSERT INTO sensors (slug, name, type, connection, features, price_uk_gbp, price_us_usd, waterproof, compatibility) VALUES
('seeed-grove-pir', 'Seeed Grove PIR', 'motion', 'GPIO', 'motion detection', 7.00, 8.70, 0, 'Community');

-- Sound
INSERT INTO sensors (slug, name, type, connection, features, price_uk_gbp, price_us_usd, waterproof, compatibility) VALUES
('dfrobot-sound-sensor', 'DFRobot Sound Sensor', 'sound', 'Analog', 'ambient sound level', 3.00, 3.50, 0, 'Community');

-- Camera
INSERT INTO sensors (slug, name, type, connection, features, price_uk_gbp, price_us_usd, waterproof, compatibility) VALUES
('seeed-grove-vision-ai', 'Seeed Grove Vision AI', 'camera', 'I2C', 'image capture, basic AI', 35.00, 42.00, 0, 'Community');
