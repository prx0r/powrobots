# POW Robotics: quantity-one manufacturing and suppliers

I reviewed [powrobots](https://github.com/prx0r/powrobots), its five electronics engines, assembly plans and supplier inventory, along with [powphysical](https://github.com/prx0r/powphysical).

The opportunity is to manufacture one standard electronics platform and personalise the enclosure, character, sensors and firmware for each customer. That works particularly well for your Plant Sprite, Desk Goblin and other ESP32-based companions.

The critical distinction is that ordering one fully assembled circuit board is not the same as ordering one finished robot. Your current plans sometimes conflate the two. PCB fabrication, component sourcing and 3D printing can already be ordered individually at low cost. Fully assembling the enclosure, wiring, actuators and electronics into a tested product remains the difficult step.

The following suppliers offer confirmed single-unit manufacturing options, rather than requiring you to commit to a production run. I have separated online-order services from manufacturers that require custom arrangements.

## 1. PCB assembly: manufactured electronics

These are the suppliers to connect to your SENSE, ACT, TALK, REMEMBER and SEE engines.

| Supplier | Quantity 1 | Service and ordering |
| --- | --- | --- |
| Seeed Fusion, China | Yes | https://www.seeedstudio.com/pcb-assembly.html — Online ordering, component sourcing and assembly from one board. |
| PCBWay, China | Yes | https://www.pcbway.com/ — PCB assembly for 1–20 prototypes, with a published $29 promotional assembly charge. |
| NextPCB, China | Yes, standard service | https://www.nextpcb.com/pcb-assembly-services — Standard turnkey PCBA supports one board. Its automated Rev 0 service requires 5 or 10. |
| Elecrow, China | Yes | https://www.elecrow.com/pcb-assembly.html — Published one-piece prototype assembly option, with component sourcing and kitting. |
| Makerfabs, China | Yes, manual pricing | https://www.makerfabs.com/pcb-assembly.html — One-piece turnkey PCB prototypes, sourcing, firmware programming and testing. |
| JLCPCB, China | Check order configuration | https://jlcpcb.com/pcb-assembly — Low-cost SMT assembly and integrated parts library. Standard PCB orders commonly start at five bare boards; the PCBA configuration determines assembled quantity. |

The most useful initial tests are Seeed Fusion's one-board checkout and PCBWay's PCB-plus-assembly workflow. Both let you submit actual production files, rather than inventing a hypothetical manufacturing cost.

## 2. One-off enclosures, custom bodies and mechanical parts

Prices below are advertised starting prices, not verified prices for a complete robot enclosure. Shipping is additional unless stated.

| Supplier | Country | What you can order, quantity 1 |
| --- | --- | --- |
| JLC3DP | China | https://jlc3dp.com/ — SLA resin from $0.30, MJF/SLS nylon from $1, full-colour WJP from $1. Online file upload and checkout. |
| PCBWay | China | https://www.pcbway.com/rapid-prototyping/ — Printed enclosures and CNC parts; no minimum order. |
| Unionfab | China | https://www.unionfab.com/services/3d-printing — Industrial 3D printing with instant online pricing and no MOQ. |
| RapidDirect | China | https://www.rapiddirect.com/services/3d-printing/ — Upload CAD files for one-off printed parts. Also handles CNC and other manufacturing processes. |
| JLCCNC | China | https://jlccnc.com/ — One-piece CNC orders, STEP upload and instant pricing. For structural parts and precision mounts. |
| Craftcloud | Global network | https://craftcloud3d.com/en/upload — Compare manufacturing offers internationally, with no minimum order. Useful for checking whether Chinese shipping offsets the manufacturing savings. |
| FacFox | China | https://i.facfox.com/insta3dp/ — One-off printing with instant pricing. Its $30 minimum order value makes it unattractive for a single tiny enclosure. |

For personalised character bodies, start with JLC3DP's SLA or MJF services. Use CNC for brackets, shafts and load-bearing parts that cannot be produced reliably by cheaper printing methods. For full-colour characters, compare WJP against printing a plain body and adding colour separately.

A useful feature of JLC3DP is that PCB and 3D-printing orders can be combined into one parcel. That reduces delivery coordination, although it does not mean they will assemble the parts together.

## 3. Who will assemble the entire robot?

This is the important missing supplier category for POW: a factory that takes your PCB, printed enclosure, motors, sensors and firmware, then delivers a functioning device rather than separate components.

One-unit prototypes are not necessarily available through instant checkout. I have distinguished online ordering from full-product assembly requiring engineering review.

| Manufacturer | One-unit option | What they actually offer |
| --- | --- | --- |
| PCBWay, China | Online submission | Full OEM service, including PCB, mechanical enclosure and box build. Select Box Build Assembly in the PCB ordering interface; final pricing follows file review. |
| Makerfabs, Shenzhen | One-unit PCBA; final assembly reviewed | Electronics, programming and testing. They also document assembling customers' externally manufactured structural parts into finished ESP32 products. |
| PCBark, China | Advertises no MOQ | Full PCBA, enclosure integration, wiring, programming and packaging from prototypes onward. Custom order rather than instant checkout. |

### PCBWay's full-product ordering route

1. Open its PCB quotation form and enable assembly.
2. Select Box Build Assembly: Yes.
3. Upload Gerbers, BOM, pick-and-place file, enclosure CAD and assembly instructions.
4. Submit the order for engineering review and the finished-product quotation.

These are actual complete-product manufacturing services, but published information does not establish a fixed checkout price for one personalised robot. A one-off prototype may carry engineering and setup charges that make it uneconomic as an Etsy order.

One useful alternative from Seeed is to customise an existing, tested device rather than manufacture new electronics. Its programme advertises a one-piece minimum for logo, packaging and supported firmware customisation, but substantial one-time setup charges.

## 4. Cheap electronics and robotics suppliers

For the first prototypes, you need suppliers that let you buy individual components without the minimum quantities imposed by wholesale distributors.

| Supplier | What to buy | Individual orders |
| --- | --- | --- |
| LCSC | ESP32 modules, ICs, passives, connectors and PCB components | Many components from 1; check each SKU. https://www.lcsc.com/ |
| AliExpress | Complete sensor modules, servos, motors, OLEDs, cables and prototype kits | Commonly 1. https://www.aliexpress.com/ |
| M5Stack | Preassembled ESP32 modules, small screens, sensors and plug-in robotics modules | Individual items. https://shop.m5stack.com/ |
| DFRobot | Soil sensors, motor drivers, controllers, robotics kits | Individual retail products. https://www.dfrobot.com/ |
| Waveshare | Camera modules, displays, servos and robot control boards | Individual retail products. https://www.waveshare.com/ |
| RobotDigg | Motors, linear mechanisms, robotic arms, extrusion and mechanical hardware | Retail listings; check minimum per part. https://www.robotdigg.com/ |
| Elecrow | Maker electronics, sensors, display modules and PCB assembly | Offers one-piece PCBA. https://www.elecrow.com/ |
| Seeed Studio | Grove modules, development boards, cables and IoT components | Individual modules, plus a one-board PCBA service. https://www.seeedstudio.com/ |

### Accessing cheaper domestic Chinese prices

Taobao and 1688 are additional sourcing channels. For a foreign buyer, Superbuy can purchase from Chinese sellers, consolidate orders at its warehouse and arrange international delivery. Its standard purchasing service advertises no purchasing fee for Taobao and 1688; domestic and international shipping still apply.

Direct links:
- https://www.taobao.com/
- https://www.1688.com/
- https://www.superbuy.com/en/page/shopping1688/

The distinction is that Taobao commonly serves individual retail purchases, whereas 1688 sellers may impose wholesale minimums. Superbuy cannot override a supplier's MOQ and does not provide professional functional testing of purchased electronics.

For POW, record the original supplier price separately from domestic delivery, consolidation fees, international shipping and landed cost. A component that is cheaper on 1688 can be more expensive when ordered individually and shipped to Britain.
