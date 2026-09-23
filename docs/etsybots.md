# POW Things: give everything you love a digital life

The bigger idea: giving ordinary physical things a digital identity, memory and a way to interact with your AI.

Plants and alarm clocks are two examples. But imagine your Muse knows how much coffee you have left, whether your sourdough starter is ready, when your dog last ate, which book you're reading and whether your favourite guitar is sitting in a room that's too humid.

Even better, the customer can tell Muse: "Design me a little companion for my coffee setup. Make it look like a sleepy frog, and have it remind me to order beans when I'm running low."

POW turns that request into a customisable physical product assembled from tested modules. The same electronics could power hundreds of designs.

Three families: objects that sense the physical world, objects that remember something about it, and objects that let your AI act in it. The interesting products combine at least two.

---

## The three product families

### Family 1: Sense the world
Objects with sensors that bring physical things into digital life.

### Family 2: Remember the world
Objects that track history, routines and states over time.

### Family 3: Act in the world
Objects that let your AI do things — lights, sounds, movement, notifications.

**Best products combine 2-3 families.**

---

## Sixteen products

| # | Product | What enters digital world | What Muse can do | Price |
|---|---------|--------------------------|-----------------|-------|
| 1 | Coffee Goblin | Bean jar weight sensor | "How many coffees left?" | £59-89 |
| 2 | Sourdough Familiar | Starter temp, feeding history | "How's Doughbert doing?" | £59-99 |
| 3 | Pet Bowl Sprite | Bowl weight, feeding history | "Has Pickles eaten?" | £59-89 |
| 4 | Bookworm | NFC book tracker | "What was I reading?" | £15-35 |
| 5 | Guitar Guardian | Case temp/humidity | "How's my guitar?" | £39-69 |
| 6 | Parcel Owl | Letterbox sensor | "Has anything arrived?" | £39-59 |
| 7 | Laundry Gremlin | Cycle tracker | "Did I forget my washing?" | £29-49 |
| 8 | Fridge Goblins | NFC leftover labels | "What do I use up?" | £19-39 |
| 9 | Seedling Family | Multi-plant monitoring | "Which seedling needs help?" | £69-119 |
| 10 | Desk Familiar | Button + focus sessions | "Start my work session" | £49-79 |
| 11 | Keys Goblin | Key stand sensor | "Have I put my keys away?" | £39-59 |
| 12 | Reading Lamp | Reading sessions + light | "Set up bedtime reading" | £59-99 |
| 13 | Tool Familiar | NFC-tagged tools | "Which drill needs servicing?" | £19-59 |
| 14 | 3D Printer Sprite | Print status + consumables | "What's happening with my printer?" | £59-99 |
| 15 | Memory Chest | Physical keepsakes + NFC | "Tell me the story behind this" | £29-59 |
| 16 | Friendship Spirits | Shared signal pair | "Send Sarah's ghost a message" | £79-119/pair |

---

## Four to prototype first

### Coffee Goblin (£59-89)
Weight sensor under jar. Frog character. Muse knows bean quantity, suggests reorder. Shares electronics with pet bowl platform.

### Sourdough Familiar (£59-99)
Temperature + feeding tracker. Muse keeps diary, prepares baking schedules. People already name their starters — natural companion.

### Guitar Guardian (£39-69)
Temp/humidity in instrument case. Muse checks readings, reminds about maintenance. Optional NFC for instrument identification.

### Bookworm (£15-35)
NFC clip-on bookmark. No battery. Tap to open reading journal. Cheapest product, easiest to manufacture, great gift.

---

## The MCP architecture

```
Muse → POW MCP → Secure device service → Devices
         ↓
    pow_list_devices()
    pow_get_plant_readings(device_id)
    pow_set_alarm(device_id, time, personality)
    pow_set_light(device_id, colour, brightness)
    pow_get_device_status(device_id)
```

One MCP server. One device service. All devices authenticate through it.

---

## Three voice levels

| Version | Experience | Complexity |
|---------|-----------|-----------|
| Button | Press → action | Firmware only |
| Push-to-talk | Press + speak → response | Speech recognition + TTS |
| Always-on | Natural conversation with Muse | Full Muse integration |

Start with push-to-talk. Always-on needs approved Muse connector.

---

## What POW does differently

- **Personalised** — character, name, colour, personality
- **Modular** — one electronics platform, many enclosures
- **Connected** — MCP integration with AI assistants
- **Repairable** — standard parts, documented assembly
- **Tested** — every order generates manufacturing data
- **Improving** — outcomes feed back into the graph

**The product is a physical body for your AI agent.**
