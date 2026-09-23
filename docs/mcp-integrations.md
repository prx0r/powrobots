# MCP Integrations for Elderly Companion

## Home Assistant MCP

### Overview
Home Assistant has native MCP support (since 2026.6.0) and multiple community MCP servers:

| Server | Stars | Features | Link |
|--------|-------|----------|------|
| **ha-mcp** | 100+ | 87+ tools, in-process server, webhook support | https://github.com/homeassistant-ai/ha-mcp |
| **homeassistant-mcp** | 103 | 40 tools, BM25 search, entity/area/device access | https://github.com/robbrad/homeassistant-mcp |
| **homeassistant-mcp-server** | 1 | REST + WebSocket, 70+ tools, HACS support | https://github.com/maximeallanic/homeassistant-mcp |
| **mcp-homeassistant** | - | PyPI package, simple REST API | https://pypi.org/project/mcp-homeassistant |

### Integration Architecture

```
Elderly Companion (ESP32-S3)
    ↓ BLE/WiFi
Home Assistant
    ↓ MCP Server
AI Agent (Muse/ChatGPT)
    ↓ Tools
- ha_get_state (lights, thermostat, locks)
- ha_call_service (turn on/off devices)
- ha_get_history (activity patterns)
- ha_fire_event (custom events)
```

### Key Tools for Elderly Care

| Tool | Purpose |
|------|---------|
| `ha_get_state` | Check room temperature, light levels, door status |
| `ha_call_service` | Turn on lights, adjust thermostat, lock doors |
| `ha_get_history` | Track daily activity patterns, detect anomalies |
| `ha_fire_event` | Trigger emergency alerts, send notifications |
| `ha_get_logbook` | Review recent events, troubleshoot issues |

---

## Open Wearables MCP

### Overview
Open Wearables is a self-hosted platform for wearable health data with native MCP support:

| Feature | Description |
|---------|-------------|
| **Unified API** | One API for 300+ devices (Apple Health, Garmin, WHOOP, Oura) |
| **Health Scores** | Open algorithms for Sleep Score, Resilience Score |
| **MCP Server** | FastMCP-based, connects to Claude Desktop/Cursor |
| **Self-hosted** | MIT license, deploy on your own infrastructure |

### Available MCP Tools

| Tool | Purpose |
|------|---------|
| `get_users` | Discover users accessible via API key |
| `get_daily_activity` | Steps, calories, heart rate, intensity minutes |
| `get_sleep_summary` | Sleep duration, quality, patterns |
| `get_workouts` | Exercise sessions, duration, intensity |
| `get_granular_samples` | Weight, SpO2, HRV, intraday heart rate |
| `get_health_scores` | Sleep score, resilience score |
| `get_menstrual_cycles` | Cycle tracking (optional) |

### Integration Architecture

```
Wearable Device (Apple Watch, Garmin, Fitbit)
    ↓ OAuth Sync
Open Wearables (self-hosted)
    ↓ MCP Server
AI Agent (Muse/ChatGPT)
    ↓ Tools
- get_daily_activity (steps, heart rate)
- get_sleep_summary (sleep quality)
- get_health_scores (sleep + resilience)
- get_workouts (exercise tracking)
```

---

## Patientary MCP (Healthcare)

### Overview
Patientary provides healthcare data via MCP for clinical applications:

| Tool | Purpose |
|------|---------|
| `lookup_npi` | Find healthcare providers by NPI |
| `search_providers` | Search providers by name, specialty, location |
| `lookup_icd10` | Look up ICD-10 diagnosis codes |
| `search_icd10` | Search diagnoses by description |
| `validate_codes` | Batch-validate NPIs and ICD-10 codes |
| `lookup_taxonomy` | Look up provider taxonomy codes |

### Use Case for Elderly Companion

```python
# When companion detects health anomaly
def handle_health_alert(companion_id, anomaly_type):
    # Look up ICD-10 code for anomaly
    icd10_code = patientary.lookup_icd10(anomaly_type)
    
    # Find nearby doctor
    providers = patientary.search_providers(
        taxonomy="family medicine",
        location="London, UK"
    )
    
    # Notify family with diagnosis info
    notify_family(companion_id, icd10_code, providers)
```

---

## Butlr MCP (Occupancy Sensing)

### Overview
Butlr provides occupancy sensing via MCP for space utilization:

| Tool | Purpose |
|------|---------|
| `find_spaces` | Find available rooms/capacity |
| `monitor_occupancy` | Real-time space utilization |
| `analyze_trends` | Historical occupancy patterns |
| `search_portfolio` | Find rooms across buildings |
| `check_sensor_health` | Monitor sensor status |
| `track_traffic` | Foot traffic analysis |

### Use Case for Elderly Care

```
# Monitor elderly person's movement patterns
1. Track daily room usage (kitchen, bedroom, bathroom)
2. Detect anomalies (e.g., spending unusual time in bathroom)
3. Alert family if patterns suggest health issues
4. Optimize home environment based on movement data
```

---

## ESPHome MCP

### Overview
ESPHome has an MCP server for direct device control:

### Use Case for Elderly Companion

```yaml
# ESPHome configuration for companion device
esphome:
  name: elderly-companion
  
sensor:
  - platform: mpu6050
    name: "Accelerometer"
    acceleration:
      name: "Acceleration"
    gyroscope:
      name: "Gyroscope"
  
  - platform: template
    name: "Fall Detection"
    lambda: |-
      // Fall detection algorithm
      if (id(acceleration).state > 3.0) {
        return 1;  // Fall detected
      }
      return 0;
```

---

## Integration Matrix

| System | MCP Server | Transport | Auth | Tools |
|--------|-----------|-----------|------|-------|
| Home Assistant | ha-mcp | HTTP/SSE/Webhook | Token | 87+ |
| Open Wearables | open-wearables | stdio | API Key | 10+ |
| Patientary | patientary | HTTP | API Key | 6 |
| Butlr | butlr-mcp | HTTP | API Key | 6 |
| ESPHome | esphome-mcp | stdio | None | Device-specific |

---

## Recommended Integration Stack

### For Elderly Companion MVP

1. **Home Assistant** — Smart home control (lights, thermostat, locks)
2. **Open Wearables** — Health data (activity, sleep, vitals)
3. **Custom MCP** — Companion-specific tools (medication reminders, emergency alerts)

### For Production Deployment

1. **Home Assistant** — Smart home control
2. **Open Wearables** — Health data
3. **Patientary** — Clinical data (ICD-10 codes, provider lookup)
4. **Butlr** — Occupancy sensing (movement patterns)
5. **Custom MCP** — Companion-specific tools

---

## Next Steps

1. **Deploy Open Wearables** — Self-hosted health data platform
2. **Configure Home Assistant** — Connect smart home devices
3. **Build Custom MCP** — Medication reminders, emergency alerts
4. **Test Integration** — End-to-end flow with real users
5. **Scale Deployment** — Roll out to care homes
