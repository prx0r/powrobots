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
