# Elderly Companion Engine

## Engine: COMPANION

A new engine type for elderly care products. Provides health monitoring, medication reminders, social connection, and emergency assistance.

### Core Capabilities

| Capability | Description |
|-----------|-------------|
| **Health Monitoring** | Connects to wearables, tracks vitals, detects anomalies |
| **Medication Reminders** | Audio + visual reminders, tracks compliance |
| **Social Connection** | One-button video calls, family updates, daily check-ins |
| **Emergency Assistance** | Fall detection, emergency contacts, location sharing |

### Key Components

| Component | MPN | Price | Purpose |
|-----------|-----|-------|---------|
| ESP32-S3 | ESP32-S3-WROOM-1 | £3.50 | Main controller |
| 7" Touchscreen | Waveshare 7" HDMI | £25.00 | Display + interface |
| Speaker | MAX98357A + 3W speaker | £3.00 | Audio output |
| Microphone | INMP441 | £2.00 | Voice input |
| NFC Reader | PN532 | £5.00 | Medication tracking |
| GPS Module | NEO-6M | £8.00 | Location sharing |
| Accelerometer | MPU-6050 | £1.50 | Fall detection |
| Camera | OV2640 | £5.00 | Video calls |
| Battery | 18650 Li-ion | £4.00 | Backup power |
| Enclosure | 3D printed | £5.00 | Custom housing |

**Total COGS: £62.00**
**Target Price: £149.99**
**Margin: 59%**

### Product Variants

| Variant | Name | Character | Price |
|---------|------|-----------|-------|
|桌面伴侣 | Mab | Wise owl | £149.99 |
| 墙壁伴侣 | Nimbus | Cloud guardian | £129.99 |
| 便携伴侣 | Pickles | Loyal dog | £169.99 |
| 床头伴侣 | Boo Bloom | Night light | £139.99 |

### Integration Points

| System | MCP Tool | Purpose |
|--------|----------|---------|
| Home Assistant | `ha_get_state` | Smart home control |
| Open Wearables | `ow_get_vitals` | Health data |
| Family App | `companion_get_updates` | Family notifications |
| Emergency Services | `companion_emergency` | Emergency alerts |

### Daily Routine

```
07:00 - Good morning message + weather
08:00 - Medication reminder #1
09:00 - Daily check-in call with family
12:00 - Lunch reminder + vitals check
15:00 - Afternoon activity suggestion
18:00 - Dinner reminder + medication #2
20:00 - Evening family call
22:00 - Bedtime reminder + sleep tracking
```

### Safety Features

- **Fall Detection**: Accelerometer detects sudden movements
- **Emergency Button**: One-press connects to emergency contacts
- **Location Sharing**: GPS shares location with family
- **Medication Tracking**: NFC tags on medication boxes
- **Daily Check-ins**: Missed check-ins trigger family alerts

### Manufacturing

- **PCB**: JLCPCB (2-layer, 1.6mm)
- **Enclosure**: JLC3DP (PLA, white/blue)
- **Assembly**: Manual (small components)
- **Testing**: 24-hour burn-in test

### Market Opportunity

- **UK elderly population**: 12.4 million (18% of population)
- **Loneliness statistics**: 2.4 million elderly people suffer from loneliness
- **Care home market**: £15.9 billion annually
- **Telehealth market**: £3.2 billion (growing 15% annually)

### Competitive Advantage

1. **AI-powered**: Muse can check in daily, detect mood changes
2. **Personalised**: Each companion has unique character and personality
3. **Connected**: Integrates with existing smart home systems
4. **Affordable**: 60% cheaper than commercial elderly monitoring systems
5. **Manufacturable**: Uses existing POW manufacturing pipeline

### Next Steps

1. Prototype MVP (ESP32-S3 + touchscreen + speaker)
2. Test with 5 elderly users for 2 weeks
3. Iterate based on feedback
4. Launch beta with 100 units
5. Scale to 1000 units per month

---

**This is the highest-impact product.** It solves a real problem (loneliness), has a clear customer (care homes, families), and connects to existing MCP infrastructure (Home Assistant, wearables).
