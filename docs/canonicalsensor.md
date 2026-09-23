# POW Glimlings — Canonical Sensor Catalogue

## 1. The complete sensor family

I'd divide the catalogue into six families. Every accessory gets a product ID, exact part number, electrical interface, compatible hub, calibration instructions and a record of which Glimlings can use it.

The supplier prices below are USD benchmarks. "Budget sourcing" means a component category to source and verify on AliExpress, 1688 or Alibaba—not a confirmed price from an approved factory. Named products with published prices provide more defensible reference points.

### A. Plantlings — one node per plant

| Sensor | Function | Chinese sourcing route | Price benchmark |
| --- | --- | --- | --- |
| Capacitive soil moisture | Tracks drying and watering | Generic modules via AliExpress/1688; DFRobot SEN0193 as reference | $5.90 branded |
| Waterproof soil moisture | Outdoor beds and patio pots | DFRobot SEN0308; OEM equivalent after ingress testing | $14.90 |
| Soil moisture + temperature + EC | Detailed root-zone monitoring | Ecowitt WH52, complete wireless unit | $27.99 |
| Waterproof root temperature | Monitors propagation and soil temperatures | DFRobot DFR0198 / generic DS18B20 | $6.90 branded |
| Air temperature + humidity | Ambient conditions in each growing area | Aosong AHT20 from LCSC | $0.53/IC at 100 |
| Ambient light | Distinguishes bright and shaded locations | BH1750 or VEML7700 via LCSC | Supplier quote required |
| Plant-pot weight | Detects changes in water content and reservoir weight | Generic load cell + HX711 via Alibaba | Supplier quote required |
| Leaf wetness | Tracks prolonged wet foliage | Ecowitt WN35, complete wireless unit | $54.99 |

The AHT20's published 100-unit price is particularly relevant to a custom PCB; unlike a ready-made breakout, it needs correct board layout and assembly. The Ecowitt WH52 is useful as a complete-device benchmark because it already combines three soil measurements with IP66 protection and an AA battery.

### B. Nimbus — weather and greenhouse sensors

| Sensor | What it unlocks | Sourcing reference | Published price |
| --- | --- | --- | --- |
| Temperature, humidity, pressure, light and UV | Compact weather station | DFRobot SEN0501 | $29.90 |
| UV | UV-exposure tracking | DFRobot LTR390 SEN0540 | $7.90 |
| Wind speed | Greenhouse and exposed-garden monitoring | DFRobot SEN0483 | $45 |
| Rainfall | Actual garden rainfall, rather than a forecast | Ecowitt WH40H | $39.99 |
| Temperature and humidity | Separate greenhouse zones | Ecowitt WN31 | $10.99 |
| Rain detection | Detects the onset of rain | DFRobot SEN0545 | $21.90 |
| Multi-parameter weather station | Weather data from one instrument | DFRobot SEN0657 | $249 |

These are reference modules and complete products, not identical types of sensor. The DFRobot SEN0501 already combines five environmental parameters, whereas its ultrasonic weather station is a specialist instrument. A low-cost Nimbus should use a small selection of component-level sensors on a shared PCB, not stack branded breakout boards.

A useful addition would be a properly calibrated PAR sensor for grow lights. Standard light and UV sensors don't directly measure the photosynthetically active radiation gardeners use to evaluate horticultural lighting.

### C. Rootkin — soil science and hydroponics

Specialist instruments

| Sensor | What it measures | Verified Chinese supplier example | Price |
| --- | --- | --- | --- |
| Liquid pH | Acidity of hydroponic solutions | DFRobot SEN0161-V2 | $39.50 |
| Continuous liquid pH | Long-term reservoir monitoring | DFRobot SEN0169-V2 | $64.90 |
| Direct wet-soil pH | Acidity of soft, wet soil | DFRobot SEN0249 | $99 |
| Liquid EC | Total dissolved-ion concentration | DFRobot DFR0300 | $69.90 |
| Soil moisture + temperature | Professional outdoor monitoring | DFRobot SEN0600, IP68 | $29 |
| Soil moisture + temperature + EC | Root-zone trends | DFRobot SEN0601, IP68 | $39 |
| Soil moisture + temperature + pH + EC | Advanced growing environment | DFRobot SEN0604, IP68 | $69 |
| Dissolved oxygen | Hydroponics and aquaponics | DFRobot SEN0237-A | $169 |

For these products, the probe and calibration regime are as important as the electronics. The $39.50 laboratory pH kit is not recommended by its manufacturer for prolonged immersion; its industrial models are designed for continuous monitoring. The dissolved-oxygen kit also requires consumable membrane caps and electrolyte maintenance.

I would avoid putting cheap generic "NPK sensors" in the mainstream range until their readings have been compared against an appropriate laboratory reference. Measuring conductivity is not the same as measuring the concentration of each individual nutrient.

### D. Waterlings — watering and reservoir management

| Accessory | Component to source | Chinese supplier reference | Published price |
| --- | --- | --- | --- |
| Leak Goblin | Water-contact detector | Ecowitt WH55, complete wireless alarm | $15.99 |
| Watering Frog | Low-volume peristaltic pump | DFRobot DFR0523 | $24 |
| Reservoir Guardian | Float switch or water-level sensor | Generic OEM through 1688/Alibaba | Quote required |
| Tank Scale | Load cell and HX711 | Generic OEM through LCSC/Alibaba | Quote required |
| Irrigation Station | Hose-connected water timer with flow meter | Ecowitt WFC01 | From $59.99 |
| Drip Zone | Normally closed valve and suitable controller | Industrial irrigation OEM | Quote required |
| Pump Health | Current sensor and reservoir-level monitoring | Generic component-level parts from LCSC | Quote required |

The WH55 and WFC01 are finished-product benchmarks rather than modules ready to drop into a custom PCB. Ecowitt's water timer includes water-temperature and flow measurement. Its leak detector, importantly, is only IP44; it is intended to detect water, not remain exposed to unrestricted outdoor rain.

DFRobot's peristaltic pump is a useful reference for a small-pot watering station, but it requires an external power supply and has substantially different electrical requirements from a sleeping battery-powered sensor.

The hub's job is to decide whether a plant needs attention. The watering station's own controller must enforce maximum dispensing time, flow or dose limits, and safe shutdown independently of cloud connectivity.

### E. Lookouts — cameras, movement and wildlife

| Sensor or module | Proposed Glimling use | Cheapest route to investigate |
| --- | --- | --- |
| PIR movement | Detect movement near a garden bed | Generic PIR modules through 1688/AliExpress |
| Microwave radar | Detect movement where appropriate | LD2410-family modules via Hi-Link distributors |
| Camera | Daily photographs, growth time-lapses | Seeed XIAO ESP32-S3 Sense or OEM camera board |
| Time-of-flight distance | Detect nearby objects or measure small distances | VL53L0X modules via LCSC/Seeed |
| Magnetic reed switch | Detect opening of greenhouse doors and lids | LCSC |
| Accelerometer | Detect movement or disturbance of a plant pot | LIS3DH or similar from LCSC |
| Sound-level sensing | Monitor ambient garden noise | Microphone module from LCSC |
| Load sensing | Detect whether a mechanism has stalled or been obstructed | Current sensing appropriate to its motor |

For budget sourcing, PIR and reed switches are simpler starting points than camera-equipped nodes. Seeed lists a Grove PIR module at $8.70 and a VL53L0X distance module at $7.90; their underlying components or OEM modules may be cheaper in quantity.

I would not promise reliable pest or plant-disease identification in this family until those specific models have been evaluated. The camera itself is only the image-acquisition component.

### F. Greenhouse specialists

This family is where you can expand beyond gifts into monitoring systems for keen gardeners and small growers.

| Accessory | Sourcing reference | Published price |
| --- | --- | --- |
| CO₂ monitor | Seeed Grove SCD41 | $52.90 |
| VOC / air-quality monitor | DFRobot BME688 breakout | $12.90 |
| Particulate pollution | Ecowitt WH43, finished sensor | $36.99 |
| Leaf-wetness monitor | Ecowitt WN35 | $54.99 |
| Multi-parameter soil probe | DFRobot SEN0604 | $69 |
| Dissolved-oxygen kit | DFRobot SEN0237-A | $169 |

There are two important measurement distinctions. SCD41 directly measures CO₂ using photoacoustic NDIR technology; a VOC-based equivalent-CO₂ estimate is not interchangeable with that measurement. And a greenhouse CO₂ sensor is more suitable for a powered environmental-monitoring station than an inexpensive sleeping plant node.

## 2. Where to source the cheapest hardware

Use a different procurement route depending on whether POW is buying one development module, manufacturing 100 units or buying a finished waterproof sensor.

| Supplier | Role in POW | What to source |
| --- | --- | --- |
| [1688](https://www.1688.com/) | Chinese domestic wholesale; promising for commodity hardware | Generic probes, housings, cables, battery holders, pumps, float switches |
| [Alibaba](https://www.alibaba.com/) | OEM and factory quotations | Assembled sensor nodes, weatherproof enclosures, customised cables, bulk components |
| [AliExpress](https://www.aliexpress.com/) | Small-quantity development | ESP32 boards, prototype sensors and one-off accessories |
| [LCSC](https://www.lcsc.com/) | Traceable production electronics | Exact sensor ICs, ESP32 modules, voltage regulators, connectors |
| [JLCPCB](https://jlcpcb.com/) | Custom PCB assembly | Complete electronics boards with compatible LCSC components |
| [DFRobot](https://www.dfrobot.com/) | Documented specialist reference modules | Water-resistant probes, pH, EC, pumps and specialist instruments |
| [Ecowitt](https://shop.ecowitt.com/) | Existing finished wireless sensor ecosystem | Outdoor sensors, rain gauges, watering timers and gateways |

For a concrete price comparison, one Alibaba SuperMini listing advertises $1.04–$1.73 depending on variant, while another quotes $1.50 at 100 units. LCSC has advertised the bare ESP32-C3 chip at approximately $1.26 at 100 units. These are different products, so the lower chip price doesn't establish a lower finished-board cost.

The relevant production comparison is a complete custom PCB against the entire SuperMini-based assembly, including its additional charging, regulation and wiring requirements.

JLCPCB's September 9, 2026 pricing lists separate charges for setup, stencil, components, assembly and certain inspection operations. As one reference, its Economic PCBA setup charge is $8.18 and stencil charge is $1.53. These are order-level charges, not costs to assign independently to every sensor.

For the cheapest-supplier database, store both the advertised price and the actual quantity-specific offer. An unverified Alibaba listing must never overwrite a recent executable supplier quotation.

## 3. Correct the £7.15 sensor-node specification

Your current node is a plausible prototype BOM, but I would separate it into two hardware designs.

### Indoor Plantling V1

Low-cost reference design

| Component | Canonical sourcing route |
| --- | --- |
| Microcontroller | ESP32-C3 SuperMini for development; approved ESP32-C3 module or chip for production |
| Soil sensing | Replaceable capacitive probe with exact recorded manufacturer and revision |
| Power | Low-leakage regulator, battery measurement and a tested battery configuration |
| Wireless | ESP-NOW or another explicitly supported low-power protocol |
| Enclosure | Injection-mouldable or printable indoor housing with accessible battery compartment |
| Identity | Factory-generated unique ID and QR pairing label |

A removable AA-battery configuration is worth comparing against the proposed 18650 and TP4056 arrangement. It eliminates charging hardware and avoids requiring customers to handle rechargeable lithium-ion cells, although battery size, runtime and operating voltage must be considered together.

Don't infer battery life from the ESP32-C3's chip-level deep-sleep specification. Espressif documents approximately 4.8 µA for an optimised deep-sleep configuration, but development-board regulators, indicator LEDs and connected sensors can materially increase actual consumption.

### Outdoor Plantling V1

Ingress testing required

Use the same firmware and plant-registration system, but change the enclosure, battery arrangement, antenna placement and soil probe as necessary.

Essential mechanical rules

The electronics housing has a target of IP66 or better, the soil probe has its own documented environmental rating, and the cable entry must be independently sealed. A customer should be able to replace a probe without opening the electronics capsule.

A removable decorative cover must not form part of the waterproof seal.

For reference, Ecowitt's WH52 demonstrates a commercially available IP66 design using one AA battery. The manufacturer specifies a minimum 12-month battery life, but POW should independently test its own electronics and duty cycle rather than inherit that claim.

## 4. The sensor network's software specification

All sensors should report into a single garden, regardless of the physical Glimling that displays their readings.

```
Garden: Tom's Garden
|
|-- Sporebert: indoor character + gateway
|
|-- Plantling 001 -> Monty the Monstera
|      moisture
|      battery
|      calibration
|
|-- Plantling 002 -> Gerald the Tomato
|      moisture
|      root temperature
|
|-- Plantling 003 -> Basil
|      moisture
|
|-- Nimbus -> shared room or greenhouse weather
|
|-- Mosswick Watering Station
|      assigned plant: Basil
|      reservoir level
|      watering history
|
`-- Boo Bloom Camera
       assigned area: greenhouse
       photographs and time-lapses
```

Plant identity, sensor identity and physical location must be separate records. Replacing a faulty probe shouldn't destroy Gerald's historical readings. Moving a sensor from Basil to Monty should create a new assignment period rather than rewrite the old measurements.

Every measurement should record its units, calibration revision, time, data source and quality status. Moisture percentages from two different uncalibrated probe models should not automatically be treated as equivalent.

For wireless transport, inexpensive ESP32-C3 nodes using ESP-NOW are a reasonable development route. But an outdoor network must be tested through brick walls, wet foliage and at different distances. A separate long-range radio option may eventually be needed; simply adding a bigger battery will not solve poor reception.

## 5. The canonical catalogue I'd build first

From this research, the useful distinction is between accessories POW can develop from inexpensive component-level electronics and those it should initially integrate or benchmark against existing complete Chinese products.

### First catalogue checkpoint

| Product | Initial implementation | Commercial purpose |
| --- | --- | --- |
| Indoor Plantling | Custom low-cost node | Affordable additional sensors |
| Outdoor Plantling | Tested sealed node or compatible OEM sensor | Weather-resistant garden monitoring |
| Nimbus Weather | Shared environmental PCB | Weather and greenhouse accessory |
| Rain Sprite | Compatible finished gauge initially | Garden rainfall history |
| Leak Goblin | Dedicated leak sensor | Watering-system protection |
| Mosswick Watering | Separate powered controller | Automated care and useful outcome data |
| Boo Bloom Vision | Camera module and approved enclosure | Photographs and plant-growth history |
| Rootkin Hydro | Established specialist probes | Higher-value enthusiast product |

The immediate instruction for `powproducts` and `powphysical` is to make every catalogue item resolve to a canonical manufacturer part number, multiple supplier offers, quantity-price breaks, shipping region, compatible electronics revision and verification status. Finished Ecowitt devices should be recorded as third-party devices requiring the relevant gateway adapter, not automatically as parts compatible with a POW ESP-NOW network.

The commercial opportunity is a cheap standard sensor that creates demand for a large family of optional abilities. The important advantage won't come from undercutting every Chinese sensor manufacturer. It will come from giving inexpensive, otherwise unrelated hardware a common plant identity, history, delightful physical character and useful AI interface.
