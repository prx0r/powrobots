# Glimlings: Cheap, Custom-Designed Physical Companion for AI Agents

## The Reframe

**Glimlings is NOT:**
- An Alexa competitor
- A conventional smart speaker
- A plant monitor

**Glimlings IS:**
- A cheap, custom-designed physical companion for an AI agent
- A little physical character that brings your agent into the room
- Gardening as first optional expansion, not the core product

---

## The First Product: Four Things Exceptionally Well

1. **Look like a creature you've designed yourself**
2. **Glow expressively**
3. **Deliver short spoken messages from your agent**
4. **Let you talk back by pressing a button**

Motion detection and microphone are inexpensive additions. Screen, camera, battery and complicated sensor array can wait.

**Customers aren't paying £50 for a soil sensor. They're paying for a little physical character that brings their agent into the room.**

---

## The Hardware Shortcut

### M5Stack Voice Modules

| Module | Price | What It Offers |
|--------|-------|----------------|
| M5Stack Atom Voice | $13.50 | ESP32, mic, speaker, RGB LED, button, Grove port |
| M5Stack Atom VoiceS3R | $14.50 | ESP32-S3, 8MB PSRAM, mic, speaker |
| M5Stack AtomS3R AI Chatbot Kit | $21.50 | ESP32-S3, mic, speaker, motion sensors |

**Use the Atom Voice inside a POW-designed mushroom shell.** That gives core voice and lighting hardware at a known retail reference price.

The Atom Voice has a ~0.8W speaker — think nearby desk companion that whispers, not a room-filling smart speaker.

---

## Personality Through Behaviour, Not Hardware

| Feature | First-Gen Experience |
|---------|---------------------|
| Ambient lighting | Glows when agent works, changes colour for attention, dims at night |
| Push-to-talk | Hold button, speak, hear agent response |
| Agent notifications | Quietly announces completed tasks, reminders |
| Motion-triggered greetings | Optional PIR sensor notices someone approaching |
| Simple gestures | Tap to acknowledge, mute, change lighting |
| Personalised voice | Choose talkative, playful, or reserved |

**Push-to-talk first, wake-word later.** Always-listening voice competes for ESP32 resources.

**Physical microphone-off switch required.** Clearly visible when mic is disabled.

---

## Garden as First Personality Pack, Not Separate Product

### Three Configurations, Same Character

| Configuration | What Sporebert Does |
|---------------|---------------------|
| Desk companion | Agent notifications, ambient lighting, conversations, reminders |
| Garden companion | Plant sensor readings, dry soil warnings, named plant questions |
| Bedside companion | Quiet lighting, simple alarms, evening routines, reminders |

**This fixes the £50 plant-monitor problem.** Customer doesn't need plants to want one. Garden functionality is an expansion.

**First garden pack: support ONE verified sensor model.** Keep Bluetooth integration separate from voice processing.

---

## POW Studio: Where to Spend Development Effort

Customer selects character, customises shape/colour/expression/lighting/name/behaviour, orders physical creature.

**Technical shortcut:** Electronics and internal mounting interface fixed. AI modifies exterior within validated envelope. Microphone openings, speaker acoustics, airflow, button access remain functional.

**Standard designs at fixed price. Custom designs at separately calculated price.**

**Device works without requiring owner to learn MCP.**

---

## The Muse Integration

**Build in two directions:**
1. Glimlings exposes authenticated MCP tools (`speak`, `set_light`, `get_status`, `acknowledge_alert`) through remote gateway
2. Own voice backend handles push-to-talk using supported speech-processing service

**Don't bet hardware business on undocumented Muse feature.** Customer can use different agent if they prefer.

**Keep basic lighting and preconfigured behaviours free.** Meter expensive cloud voice processing.

---

## Price Realistically

### Glimling Mini — £49.99–£59.99

Target retail range, not confirmed viable production price.

- Original, customisable USB-powered character
- Microphone, speaker, expressive light, button
- Agent connectivity
- Garden pack and motion sensor as optional additions
- No camera, screen, lithium battery, waterproof enclosure

**At small quantities, development boards may make £49.99 financially unattractive after printing, assembly, shipping, VAT, platform fees and returns.**

**Get fully assembled sample cost before fixing price.**

---

## The First Demonstration

> A personalised mushroom on a desk, glowing while an agent works. When the agent finishes, its light changes and it gives a short spoken summary. The owner presses its head, asks a question and hears a reply.

**If that interaction is delightful and reliable, test whether people will pay for the physical character and their own design.**

Then introduce garden pack, motion accessories, third-party sensor marketplace.

**The expensive part to prove isn't whether we can connect another £1 sensor — it's whether people actually want their agent to have a physical presence in their room.**
