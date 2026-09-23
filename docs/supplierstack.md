# POW Glimlings — canonical supplier routes

The aim is to define a manufacturing route for every engine and product in `prx0r/powrobots`, without ordering anything or making up production costs.

Use JLCPCB for standard assembled electronics, JLC3DP for personalised enclosures, and a separate fulfilment partner for final assembly and dispatch. Exceptions are products needing external probes, motors, cameras or more complex assembly.

Your five original engines are SENSE, REMEMBER, ACT, TALK and SEE, with COMPANION added in the newer specification. They should share components and manufacturing processes wherever possible.

## 1. The common supplier infrastructure

| Stage | Canonical supplier | Alternative |
| --- | --- | --- |
| Electronic components | [LCSC](https://www.lcsc.com/) | [Mouser](https://www.mouser.co.uk/) for unavailable parts |
| Custom PCB and component assembly | [JLCPCB](https://jlcpcb.com/pcb-assembly) | [Seeed Fusion](https://www.seeedstudio.com/pcb-assembly.html) |
| One-off personalised enclosure | [JLC3DP](https://jlc3dp.com/) | [PCBWay](https://www.pcbway.com/) |
| Specialist sensors, modules and robotics parts | [DFRobot](https://www.dfrobot.com/), [Waveshare](https://www.waveshare.com/), [Seeed](https://www.seeedstudio.com/) | [AliExpress](https://www.aliexpress.com/) |
| Complete product assembly | [PCBWay OEM](https://www.pcbway.com/helpcenter/placingorders/How_to_Place_an_OEM_Order_.html) | [Makerfabs](https://www.makerfabs.com/) |
| UK packing and dispatch | UK fulfilment partner, to be selected | In-house initially, if necessary |

JLCPCB has established PCBA pricing and component inventory services, while Seeed accepts one-off prototype PCBA orders. PCBWay documents complete enclosure-to-box assembly, but the price and feasibility of individually personalised orders require project-specific confirmation.

The standard production package for every engine should contain a versioned BOM, Gerbers, pick-and-place files, firmware, enclosure STEP/STL files, assembly instructions and a functional-test procedure.

## 2. Canonical route for each engine

I would standardise around four board families rather than manufacture six unrelated circuit boards. SENSE, REMEMBER and basic ACT can share one ESP32-based PCB, with different components populated for different products.

These are proposed manufacturing specifications based on your repository's BOMs. They are not yet finished, verified PCB designs.

| Engine | Electronics sourcing and assembly | Enclosure and final assembly |
| --- | --- | --- |
| SENSE | LCSC → JLCPCB. ESP32-S3, light and temperature/humidity sensors on the PCB. [DFRobot SEN0193](https://www.dfrobot.com/product-1385.html) for external soil sensing. | JLC3DP character shell, internal snap rails and a keyed connector for the soil probe. |
| REMEMBER | Reuse the SENSE/ACT core PCB, without unnecessary sensors. Use ESP32 flash for basic history; populate a DS3231 RTC only when offline timekeeping is required. | JLC3DP compact shell. PCB snaps into place. |
| ACT | LCSC → JLCPCB. ESP32, RGB LEDs, buzzer and actuator-driving circuitry. [AliExpress](https://www.aliexpress.com/) or specialist suppliers for external servos and pumps. | JLC3DP shell. LEDs and buzzer can remain entirely on the PCB; moving components need secure mounting and connections. |
| TALK | LCSC → JLCPCB. ESP32-S3, MEMS microphone, MAX98357 amplifier and buttons. Source the speaker separately if it cannot mount directly to the board. | JLC3DP acoustic enclosure with speaker mounting, sound openings and an accessible microphone. |
| SEE | [Seeed XIAO ESP32-S3 Sense](https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/) for the initial module-based design. Custom camera PCBA through Seeed Fusion or PCBWay for a later version. | JLC3DP enclosure with camera alignment and an unobstructed field of view. Pan/tilt products require a separate mechanical assembly. |
| COMPANION | Dedicated ESP32-S3 touchscreen/audio platform with optional camera; Seeed Fusion or PCBWay for its eventual PCBA. | JLC3DP premium enclosure; complete assembly, programming and testing through a specialist manufacturer. |

DFRobot documents the SEN0193 as a separately connected three-pin sensor. Its outdoor SEN0308 is a different waterproof probe, not simply a weatherproof version of an ordinary snap-fit PCB. Seeed's current XIAO ESP32-S3 Sense uses an upgraded OV3660 camera on newer units; your design should not assume the older OV2640 will remain available.

For parts not available in JLCPCB's normal library, it provides pre-order, global-sourcing and customer-consigned component options. That avoids automatically introducing a second assembly factory whenever one specialised component is missing.

## 3. Canonical routes for the 12 products in your current handover

Here is the mapping from the repository's product catalogue. Each row names the electronics platform, any product-specific sourcing and the physical assembly route.

| Product | Electronics route | Custom parts and assembly |
| --- | --- | --- |
| Mosswick — Garden Frog | SENSE + ACT core via JLCPCB | DFRobot soil probe, JLC3DP frog enclosure, probe connector and snap-fit core. |
| Sporebert — Garden Mushroom | Same as Mosswick | Same electronics and probe; different JLC3DP mushroom shell. |
| Boo Bloom — Garden Ghost | Same as Mosswick | Same electronics and probe; different JLC3DP ghost shell. |
| Puck — Desk Goblin | ACT/display board via JLCPCB, with OLED, buzzer, LED and controls | JLC3DP enclosure with a display window and snap-fit PCB retention. |
| Mab — Desk Familiar | Same ACT/display platform as Puck | Different shell and firmware configuration, without a different PCB unless its features actually differ. |
| Mab — Sleep Alarm | ACT + TALK board, adding microphone and speaker | JLC3DP bedside enclosure with acoustics, accessible controls and a secure speaker mount. |
| Nimbus — Home Weather | SENSE + display board | Temperature/humidity/light sensors; printed shell with appropriate ventilation and sensor exposure. |
| Chroma — Home Mood | SENSE + LED variant of the common core | Printed translucent diffuser and character shell; no external wiring if LEDs mount directly to the PCB. |
| Postie — Home Parcel | SENSE + TALK board | Printed shell plus a parcel-detection sensor that still needs to be specified. Electronics route defined; complete BOM unresolved. |
| Pickles — Outdoor Pet | SENSE + ACT + TALK | Waterproof connectors, weather-resistant enclosure and dedicated power arrangement. Full mechanical and environmental design unresolved. |
| Wormington — Bookworm | Minimal REMEMBER board plus NFC | JLC3DP bookworm enclosure and NFC antenna. Existing product economics need revision before treating this as commercially ready. |
| Elderly Companion | Dedicated COMPANION hardware via Seeed Fusion or PCBWay | Touchscreen, speaker, optional camera and custom enclosure. Requires its own testing and safety programme; not equivalent to assembling an ordinary decorative Glimling. |

The central manufacturing simplification is that Mosswick, Sporebert and Boo Bloom should be the same product internally. Similarly, Puck and Mab should reuse the same display board where their capabilities match. Each differently shaped enclosure should preserve the standard mounting geometry and electrical interfaces.

## 4. Routes for the additional products in the original engine specification

| Product | Canonical route |
| --- | --- |
| Coffee Goblin | SENSE + REMEMBER core from JLCPCB; separately sourced load cell and load-cell amplifier if actual weight measurement is required; JLC3DP enclosure with a mechanically isolated weighing platform. |
| Sourdough Familiar | SENSE + REMEMBER core; external temperature probe if measuring dough rather than ambient air; JLC3DP printed enclosure. |
| Pet Bowl Sprite | SENSE + SEE, using the camera platform and an external sensing module; JLC3DP camera enclosure. Pet identification and bowl measurement need separate validation. |
| Guitar Guardian | SENSE + REMEMBER core, populated with environmental sensors; JLC3DP case with ventilation. |
| Parcel Owl | Same physical product family as Postie. Resolve the repository's disagreement between SENSE + ACT and SENSE + TALK before freezing its BOM. |
| Laundry Gremlin | REMEMBER + basic ACT core, LEDs and buzzer; JLC3DP enclosure. Additional power-control hardware is needed if it must operate an appliance. |
| Fridge Goblins | SENSE + REMEMBER core with optional NFC; JLC3DP enclosure designed for condensation and cold operating conditions. |
| Seedling Family | Three identical SENSE boards and three printed characters. Treat as a multipack of one verified hardware design. |
| Keys Goblin | REMEMBER + NFC variant, custom shell. NFC can identify tagged keys at close range, but cannot by itself provide remote location tracking. |
| Reading Lamp | SENSE + REMEMBER + ACT core; LED driver and appropriate low-voltage power supply; JLC3DP shell designed for heat dissipation. |
| Tool Familiar | SENSE + REMEMBER core plus NFC; tool tags sourced separately, with one central reader module. |
| 3D Printer Sprite | SEE + temperature monitoring, camera module and printed mounting bracket. Camera and temperature probe must suit the actual installation environment. |
| Friendship Spirits | Two identical ACT cores, two personalised shells and paired firmware identities. Separate power for each unit. |

## 5. Canonical final assembly and delivery

Use two fulfilment routes, selected by assembly complexity and expected demand.

| Route | Supplier chain | Applies to |
| --- | --- | --- |
| China direct | JLCPCB electronics + JLC3DP enclosure → Makerfabs final assembly, test, packaging and dispatch | Individually personalised Glimlings, initially the default route |
| UK stocked | China-made electronics imported in batches → printed shells and UK fulfilment through a kitting-capable partner | Repeatable designs with enough demand to justify holding UK inventory |
| Integrated factory | Makerfabs or PCBWay handles electronics, mechanical parts, final assembly and testing under one manufacturing arrangement | Cameras, motors, pumps and other more complicated products |

Makerfabs publishes both a one-piece manufacturing service and a dropshipping service, covering product assembly, testing, packaging, storage and international dispatch. It still needs to confirm that its workflow supports a different enclosure for every customer.

For the UK-stocked route, ShipBob's kitting service is an example of a provider that can combine prepared components and packaging. Its standard service should not be treated as electronics programming, engineering inspection or custom robot manufacturing.

The main unresolved supplier constraint is personalised, quantity-one final assembly and fulfilment. One-off PCB assembly and enclosure printing are already documented services. The complete per-order chain is not yet commercially verified.

## 6. Make these routes canonical inside POW

`powrobots` should own the engines, product BOMs and manufacturing requirements. `powproducts` should own canonical component identities and compatibility. `powphysical` should own supplier selection, manufacturing routes and landed-cost calculations.

Each product route needs an immutable version containing:

* Exact engine and PCB revisions, quantities and approved alternatives.

* Component supplier identifiers, manufacturer part numbers and purchasing URLs.

* Enclosure material, CAD revision, manufacturing supplier and mounting interface.

* Assembly operations, required tools, expected labour, test procedure and fulfilment destination.

* Minimum order, verified quoted cost, shipping, import charges, last verification date and any unresolved constraints.

The current `powphysical` implementation contains LCSC, M5Stack and Waveshare adapters. JLCPCB, JLC3DP, Makerfabs and the other manufacturing services above are not yet implemented as working procurement integrations. These routes therefore belong in a versioned supplier registry first, not in a system that pretends it can automatically purchase finished products.

Keep three distinct statuses: proposed, when the component and supplier route is technically specified; supplier-confirmed, when the exact configuration and quantity are accepted; and production-verified, when an actual manufactured unit passes its specified tests. Your engines and products now have proposed routes, with explicit gaps rather than invented prices or assembly guarantees.
