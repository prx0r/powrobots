# Glimlings as MCP Servers — The Real Vision

## The Concept

**Each Glimling IS an MCP server. Muse connects to it. Muse reads sensors, controls LEDs, gets status.**

NOT: "Order a Glimling"
BUT: "Talk to your Glimling"

Sporebert isn't just a plant monitor. **Sporebert is a mushroom that Muse can talk to.**

---

## How It Works

```
ESP32-S3 runs:
  1. MicroPython firmware
  2. MCP server (over HTTP/SSE)
  3. Connects to WiFi
  4. Exposes tools to Muse

Muse connects:
  1. Discovers Glimling on network
  2. Calls MCP tools
  3. Reads sensor data
  4. Controls outputs
  5. Responds to user
```

### Example Conversation

```
USER: "Muse, how's my monstera?"
    ↓
MUSE: Calls Sporebert MCP tool "get_moisture"
    ↓
SPOREBERT: Returns {moisture: 35%, status: "dry"}
    ↓
MUSE: "Your monstera is thirsty! Moisture at 35%.
       Want me to remind you to water it?"
    ↓
USER: "Yes"
    ↓
MUSE: "OK, I'll check again in 2 hours."
```

---

## MCP Tools Per Engine

### SENSE Engine

| Tool | Description |
|------|-------------|
| `get_moisture` | Read soil moisture percentage |
| `get_light` | Read light level in lux |
| `get_temperature` | Read temperature in °C |
| `get_humidity` | Read humidity percentage |
| `get_status` | Get all sensor readings |
| `set_led` | Set LED colour (R, G, B) |
| `get_alerts` | Check for alerts (low moisture, etc.) |

### ACT Engine

| Tool | Description |
|------|-------------|
| `get_display` | Get current display content |
| `set_display` | Set display text or face |
| `get_encoder` | Read encoder position |
| `press_button` | Simulate button press |
| `set_led` | Set LED colour (R, G, B) |
| `buzz` | Play buzzer sound |
| `get_expression` | Get current expression |
| `set_expression` | Set expression (happy, sleepy, etc.) |

### TALK Engine

| Tool | Description |
|------|-------------|
| `speak` | Play audio clip |
| `listen` | Record audio from microphone |
| `get_volume` | Get current volume level |
| `set_volume` | Set volume level |
| `get_transcript` | Get last transcribed speech |

### SEE Engine

| Tool | Description |
|------|-------------|
| `capture` | Capture image from camera |
| `detect_faces` | Detect faces in image |
| `detect_objects` | Detect objects in image |
| `get_motion` | Check for motion |
| `set_night_vision` | Enable/disable night vision |

---

## The Technical Challenge

### ESP32-S3 Capabilities

| Capability | Status |
|------------|--------|
| WiFi | ✅ Can connect to network |
| HTTP server | ✅ Can serve MCP |
| MicroPython | ✅ Can run MCP server |
| Memory | ❌ Limited (128KB RAM) |
| Processing | ❌ Limited power |

### The Solution

| Problem | Solution |
|---------|----------|
| Limited memory | Lightweight MCP server |
| Multiple tools | Cache sensor readings |
| Slow response | Respond quickly, one at a time |
| WiFi stability | Auto-reconnect |

---

## Firmware Architecture

```
sporebert/
├── main.py          # Main loop
├── mcp_server.py    # MCP server (lightweight)
├── sensors.py       # Sensor readings
├── led.py           # LED control
├── wifi.py          # WiFi connection
└── config.py        # Configuration
```

### MCP Server

```python
# mcp_server.py - Lightweight MCP server for ESP32

class MCPServer:
    def __init__(self):
        self.tools = {
            "get_moisture": self.get_moisture,
            "get_light": self.get_light,
            "get_temperature": self.get_temperature,
            "set_led": self.set_led,
            "get_status": self.get_status,
        }
    
    def handle_request(self, request):
        method = request.get("method")
        if method == "tools/list":
            return {"tools": list(self.tools.keys())}
        elif method == "tools/call":
            tool = request["params"]["name"]
            args = request["params"].get("arguments", {})
            return self.tools[tool](args)
    
    def get_moisture(self, args):
        # Read from sensor
        moisture = read_soil_sensor()
        return {"moisture": moisture, "unit": "%"}
```

---

## Muse Integration

### How Muse Connects

```
1. Discover Glimling on network (mDNS)
   - Glimling broadcasts: _mcp._tcp.local
   - Muse finds: sporebert.local

2. Connect via HTTP
   - Muse sends: GET http://sporebert.local:8080/mcp
   - Glimling responds with available tools

3. Call MCP tools
   - Muse sends: POST http://sporebert.local:8080/mcp
   - Body: {"method": "tools/call", "params": {"name": "get_moisture"}}

4. Get responses
   - Glimling responds: {"result": {"moisture": 35}}

5. Act on data
   - Muse interprets and responds to user
```

### Example Muse Responses

```
"Your monstera is at 35% moisture.
 Light level is 500 lux.
 Temperature is 22°C.
 I recommend watering it today."

"I noticed your plant hasn't had
 enough light today. Maybe move it
 closer to the window?"

"Good morning! Your monstera is
 healthy. Moisture at 65%, light
 at 800 lux. Have a great day!"

"Alert! Your monstera's moisture
 dropped below 20%. Water it now
 to prevent damage."
```

---

## The Vision

### Current State

```
Customer buys Glimling
    ↓
Glimling sits on desk
    ↓
Customer checks app manually
    ↓
No AI integration
```

### Future State (MCP Integrated)

```
Customer buys Glimling
    ↓
Glimling connects to WiFi
    ↓
Muse discovers Glimling
    ↓
Muse reads sensors automatically
    ↓
Muse proactively alerts user
    ↓
Muse suggests actions
    ↓
Glimling becomes AI companion
```

---

## What Changes

| Aspect | Current | MCP Integrated |
|--------|---------|----------------|
| Interaction | Manual app checks | AI conversations |
| Alerts | User checks manually | Proactive alerts |
| Intelligence | None | AI-powered insights |
| Personalization | Static | Learns user habits |
| Value | Product | Companion |

**This is the difference between a gadget and a companion.**

---

## The Path

### Phase 1: Firmware (Now)

1. Add MCP server to firmware
2. Expose sensor tools
3. Test with local MCP client
4. Verify WiFi stability

### Phase 2: Muse Integration (Next)

1. Connect Muse to Glimling
2. Test tool calls
3. Refine responses
4. Add proactive alerts

### Phase 3: Production (Later)

1. Ship with MCP enabled
2. Auto-discovery on network
3. Seamless Muse connection
4. Ongoing AI improvements

**This is the real product. Not just a sensor. An AI companion.**
