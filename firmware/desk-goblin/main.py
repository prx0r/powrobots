"""
POW Desk Goblin — ESP32-S3 Firmware

A physical embodiment of your AI assistant's status.
Reacts to calendar events, deadlines, and task completions.

Hardware:
  ESP32-S3 DevKit     — £8.90
  SSD1306 OLED 0.96"  — £3.00 (I2C)
  Rotary Encoder       — £1.50
  Push Button          — £0.50
  WS2812B RGB LED      — £0.30
  Active Buzzer        — £0.20
  USB-C Cable          — £1.00

Wiring:
  OLED:    SDA→GPIO21 SCL→GPIO22 VCC→3.3V GND→GND
  Encoder: CLK→GPIO25 DT→GPIO26 SW→GPIO27 VCC→3.3V GND→GND
  LED:     DIN→GPIO5 VCC→5V GND→GND
  Buzzer:  VCC→5V GND→GND IN→GPIO18
"""

import json
import time
import network
from machine import Pin, I2C

# ─── Configuration ───
DEVICE_ID = "desk-goblin-001"
DEVICE_NAME = "Grizelda"  # Customer chooses
CHARACTER = "goblin"  # Customer chooses: goblin/mushroom/frog/ghost/robot
LED_COLOUR = (0, 200, 100)  # Customer chooses

WIFI_SSID = "YOUR_WIFI"
WIFI_PASS = "YOUR_PASSWORD"
MCP_URL = "http://YOUR_SERVER:8080/api/event"

# ─── Hardware ───
try:
    from ssd1306 import SSD1306_I2C
    i2c = I2C(0, sda=Pin(21), scl=Pin(22))
    oled = SSD1306_I2C(128, 64, i2c)
    HAS_OLED = True
except:
    HAS_OLED = False

try:
    from neopixel import NeoPixel
    led = NeoPixel(Pin(5, Pin.OUT), 1)
    HAS_LED = True
except:
    HAS_LED = False

encoder_clk = Pin(25, Pin.IN, Pin.PULL_UP)
encoder_dt = Pin(26, Pin.IN, Pin.IN)
encoder_btn = Pin(27, Pin.IN, Pin.PULL_UP)
buzzer = Pin(18, Pin.OUT, value=0)

# ─── State ───
last_encoder = encoder_clk.value()
expression = "happy"  # happy/sleepy/excited/horror/thinking
display_text = "Ready"
notification_count = 0

EXPRESSIONS = {
    "happy":   {"led": (0, 255, 0), "face": ":-)"},
    "sleepy":  {"led": (100, 100, 0), "face": ":-Z"},
    "excited": {"led": (0, 200, 255), "face": ":-D"},
    "horror":  {"led": (255, 0, 0), "face": ":-O"},
    "thinking":{"led": (150, 150, 255), "face": ":-/"},
}


def set_led(r, g, b):
    if HAS_LED:
        led[0] = (r, g, b)
        led.write()


def update_display():
    if not HAS_OLED:
        return
    oled.fill(0)
    expr = EXPRESSIONS.get(expression, EXPRESSIONS["happy"])
    oled.text(expr["face"], 40, 0)
    oled.text(DEVICE_NAME, 10, 20)
    oled.text(display_text[:16], 0, 40)
    if notification_count > 0:
        oled.text(f"*{notification_count} new", 0, 55)
    oled.show()


def read_encoder():
    global last_encoder
    current = encoder_clk.value()
    if current != last_encoder:
        last_encoder = current
        return -1 if encoder_dt.value() != current else 1
    return 0


def send_event(event_type, data):
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
    print(f"POW Desk Goblin: {DEVICE_NAME}")
    connected = await connect_wifi()

    while True:
        # Check encoder
        direction = read_encoder()
        if direction != 0:
            expression = list(EXPRESSIONS.keys())[
                (list(EXPRESSIONS.keys()).index(expression) + direction) % len(EXPRESSIONS)
            ]
            set_led(*EXPRESSIONS[expression]["led"])
            update_display()

        # Check button press
        if encoder_btn.value() == 0:
            notification_count += 1
            buzzer.value(1)
            time.sleep_ms(100)
            buzzer.value(0)
            if connected:
                send_event("button_press", {"count": notification_count})

        # Simulate calendar events (in production, receive from MCP)
        # For demo: cycle expressions every 60 seconds
        if connected:
            send_event("status", {
                "device_id": DEVICE_ID,
                "expression": expression,
                "notifications": notification_count,
            })

        update_display()
        await asyncio.sleep(0.1)


import uasyncio as asyncio
if __name__ == "__main__":
    asyncio.run(main())
