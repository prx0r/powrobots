"""
POW Plant Agent — ESP32-S3 Firmware

Monitors soil moisture, light, temperature.
Connects to POW MCP for Muse integration.
Sends alerts when plant needs water.

Hardware:
  - ESP32-S3
  - Capacitive soil moisture sensor (GPIO 34)
  - BH1750 light sensor (I2C)
  - DHT22 temp/humidity (GPIO 4)
  - WS2812B RGB LED (GPIO 5)
  - 5V relay for water pump (GPIO 18)

Wiring:
  Soil sensor:  VCC→3.3V, GND→GND, AOUT→GPIO34
  BH1750:       VCC→3.3V, GND→GND, SDA→GPIO21, SCL→GPIO22
  DHT22:        VCC→3.3V, GND→GND, DATA→GPIO4
  RGB LED:      VCC→5V, GND→GND, DIN→GPIO5
  Relay:        VCC→5V, GND→GND, IN→GPIO18
"""

import json
import time
import network
import uasyncio as asyncio
from machine import Pin, ADC, I2C
from neopixel import NeoPixel

# Configuration
WIFI_SSID = "YOUR_WIFI"
WIFI_PASS = "YOUR_PASSWORD"
MCP_ENDPOINT = "http://YOUR_POW_SERVER:8080"
DEVICE_ID = "plant-agent-001"
DEVICE_NAME = "Gerald"

# Pins
SOIL_PIN = 34
DHT_PIN = 4
LED_PIN = 5
RELAY_PIN = 18
I2C_SDA = 21
I2C_SCL = 22

# Thresholds
MOISTURE_LOW = 30
MOISTURE_CRITICAL = 20
LIGHT_LOW = 100

# Initialize hardware
soil_adc = ADC(Pin(SOIL_PIN))
soil_adc.atten(ADC.ATTN_11DB)
led = NeoPixel(Pin(LED_PIN, Pin.OUT), 1)
relay = Pin(RELAY_PIN, Pin.OUT, value=0)
i2c = I2C(0, sda=Pin(I2C_SDA), scl=Pin(I2C_SCL))


def read_soil_moisture():
    """Read soil moisture sensor (0-100, higher = wetter)."""
    raw = soil_adc.read()
    # Map ADC value (0-4095) to percentage (inverted: dry=high, wet=low)
    moisture = max(0, min(100, 100 - (raw / 4095 * 100)))
    return round(moisture, 1)


def read_light():
    """Read ambient light level from BH1750."""
    try:
        i2c.writeto(0x23, bytes([0x10]))  # Start continuous measurement
        time.sleep_ms(180)
        data = i2c.readfrom(0x23, 2)
        lux = (data[0] << 8 | data[1]) / 1.2
        return round(lux, 1)
    except:
        return -1


def set_led(r, g, b):
    """Set RGB LED colour."""
    led[0] = (r, g, b)
    led.write()


def get_plant_status():
    """Get current sensor readings."""
    moisture = read_soil_moisture()
    light = read_light()

    # LED colour based on moisture
    if moisture < MOISTURE_CRITICAL:
        set_led(255, 0, 0)  # Red: critical
    elif moisture < MOISTURE_LOW:
        set_led(255, 165, 0)  # Orange: low
    else:
        set_led(0, 255, 0)  # Green: healthy

    return {
        "device_id": DEVICE_ID,
        "device_name": DEVICE_NAME,
        "moisture": moisture,
        "light": light,
        "timestamp": time.time(),
        "status": "critical" if moisture < MOISTURE_CRITICAL else
                   "low" if moisture < MOISTURE_LOW else "healthy",
    }


def water_plant(duration_ms=2000):
    """Activate water pump for specified duration."""
    relay.value(1)
    set_led(0, 0, 255)  # Blue: watering
    time.sleep_ms(duration_ms)
    relay.value(0)
    set_led(0, 255, 0)  # Green: done


async def connect_wifi():
    """Connect to WiFi."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASS)

    for _ in range(20):
        if wlan.isconnected():
            print(f"Connected: {wlan.ifconfig()[0]}")
            return True
        time.sleep(0.5)

    print("WiFi connection failed")
    return False


async def report_to_mcp(status):
    """Report status to POW MCP server."""
    try:
        import urequests
        response = urequests.post(
            f"{MCP_ENDPOINT}/api/device/status",
            json=status,
            headers={"Content-Type": "application/json"}
        )
        print(f"MCP report: {response.status_code}")
        response.close()
    except Exception as e:
        print(f"MCP error: {e}")


async def main():
    """Main loop."""
    print(f"POW Plant Agent: {DEVICE_NAME}")
    print("=" * 30)

    # Connect WiFi
    if not await connect_wifi():
        print("Running in offline mode")
        while True:
            status = get_plant_status()
            print(f"Moisture: {status['moisture']}% | Light: {status['light']} lux | Status: {status['status']}")
            if status['moisture'] < MOISTURE_LOW:
                water_plant()
            await asyncio.sleep(60)

    # Connected mode — report to MCP
    print("Connected to POW MCP")
    while True:
        status = get_plant_status()
        print(f"Moisture: {status['moisture']}% | Light: {status['light']} lux | Status: {status['status']}")

        # Report to MCP (Muse can query this)
        await report_to_mcp(status)

        # Water if needed
        if status['moisture'] < MOISTURE_LOW:
            print("Watering plant...")
            water_plant()
            # Report watering event
            status['action'] = 'watered'
            await report_to_mcp(status)

        await asyncio.sleep(300)  # Check every 5 minutes


if __name__ == "__main__":
    asyncio.run(main())
