"""
POW Plant Sprite — ESP32-S3 Firmware

A personalised plant companion that monitors soil moisture,
light, and temperature. Reports to POW MCP for Muse integration.

Hardware (from BOM):
  ESP32-S3 DevKit     — £8.90 (Kunkune UK)
  Soil Moisture Sensor — £1.20 (AliExpress)
  BH1750 Light Sensor  — £1.50 (AliExpress)
  DHT22 Temp/Humidity  — £2.00 (AliExpress)
  WS2812B RGB LED      — £0.30 (AliExpress)
  USB-C Cable          — £1.00 (AliExpress)

Wiring:
  Soil:    VCC→3.3V GND→GND AOUT→GPIO34
  BH1750:  VCC→3.3V GND→GND SDA→GPIO21 SCL→GPIO22
  DHT22:   VCC→3.3V GND→GND DATA→GPIO4
  LED:     VCC→5V GND→GND DIN→GPIO5
"""

import json
import time
import network
from machine import Pin, ADC, I2C

# ─── Configuration ( personalised per device) ───
DEVICE_ID = "plant-sprite-001"
DEVICE_NAME = "Gerald"  # Customer chooses this
PLANT_NAME = "Monstera"  # Customer chooses this
LED_COLOUR = (0, 255, 0)  # Customer chooses this
PERSONALITY = "friendly"  # Customer chooses this

WIFI_SSID = "YOUR_WIFI"
WIFI_PASS = "YOUR_PASSWORD"
MCP_URL = "http://YOUR_SERVER:8080/api/event"

# ─── Thresholds ───
MOISTURE_LOW = 30
MOISTURE_CRITICAL = 20
LIGHT_LOW = 100
CHECK_INTERVAL = 300  # 5 minutes

# ─── Hardware ───
soil_adc = ADC(Pin(34))
soil_adc.atten(ADC.ATTN_11DB)

try:
    i2c = I2C(0, sda=Pin(21), scl=Pin(22))
    HAS_LIGHT = True
except:
    HAS_LIGHT = False

led = None
try:
    from neopixel import NeoPixel
    led = NeoPixel(Pin(5, Pin.OUT), 1)
except:
    pass


def read_moisture():
    raw = soil_adc.read()
    return max(0, min(100, 100 - (raw / 4095 * 100)))


def read_light():
    if not HAS_LIGHT:
        return -1
    try:
        i2c.writeto(0x23, bytes([0x10]))
        time.sleep_ms(180)
        data = i2c.readfrom(0x23, 2)
        return round((data[0] << 8 | data[1]) / 1.2, 1)
    except:
        return -1


def set_led(r, g, b):
    if led:
        led[0] = (r, g, b)
        led.write()


def get_status():
    moisture = read_moisture()
    light = read_light()

    if moisture < MOISTURE_CRITICAL:
        set_led(255, 0, 0)
        status = "critical"
    elif moisture < MOISTURE_LOW:
        set_led(255, 165, 0)
        status = "low"
    else:
        set_led(*LED_COLOUR)
        status = "healthy"

    return {
        "device_id": DEVICE_ID,
        "name": DEVICE_NAME,
        "plant": PLANT_NAME,
        "moisture": moisture,
        "light": light,
        "status": status,
        "personality": PERSONALITY,
        "timestamp": time.time(),
    }


def send_event(event_type, data):
    """Send event to POW MCP for Muse consumption."""
    event = {
        "device_id": DEVICE_ID,
        "device_name": DEVICE_NAME,
        "event": event_type,
        "data": data,
        "timestamp": time.time(),
    }
    try:
        import urequests
        resp = urequests.post(MCP_URL, json=event,
                              headers={"Content-Type": "application/json"})
        resp.close()
    except:
        pass


async def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASS)
    for _ in range(20):
        if wlan.isconnected():
            return True
        time.sleep(0.5)
    return False


async def main():
    print(f"POW Plant Sprite: {DEVICE_NAME}")
    connected = await connect_wifi()

    while True:
        status = get_status()
        print(f"{PLANT_NAME}: moisture={status['moisture']}% light={status['light']} lux [{status['status']}]")

        if connected:
            send_event("status", status)

            if status["moisture"] < MOISTURE_LOW:
                send_event("moisture_low", {
                    "moisture": status["moisture"],
                    "plant": PLANT_NAME,
                    "message": f"{PLANT_NAME} is thirsty!" if PERSONALITY == "friendly"
                               else f"{PLANT_NAME} moisture critically low",
                })

        await asyncio.sleep(CHECK_INTERVAL)


import uasyncio as asyncio
if __name__ == "__main__":
    asyncio.run(main())
