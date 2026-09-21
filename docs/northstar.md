# POWROBOTS

## Mission

Build `powrobots` as the UK-first physical-economy data garden for robotics.

This is **not** initially:

* a robotics news site
* a stock screener
* a dashboard
* an AI chatbot
* a robot comparison site
* a complicated forecasting model
* a collection of speculative embeddings
* a generic web scraper

Checkpoint 1 / Layer 1 has one purpose:

> Continuously acquire, normalize, identity-resolve and preserve the physical signals needed to reconstruct the UK robotics economy through time.

The eventual question POWRobots should answer is:

> What physical bottleneck in the robotics buildout is tightening or relaxing, how early can we observe it, which organisations are exposed, and has the financial market priced it yet?

The canonical causal path is:

```text
robot adoption
    ↓
robot/cell demand
    ↓
component demand
    ↓
motors / drives / encoders / gearboxes / bearings
controllers / PLCs / industrial PCs
vision / cameras / sensors
memory / storage / compute
power electronics
grippers / EOAT
safety equipment
cables / connectors
    ↓
inventory + lead times + prices
    ↓
installation / integration load
    ↓
maintenance + failures + spares
    ↓
technician / training demand
    ↓
replacement + refurbishment market
    ↓
supplier revenues / margins / capex
    ↓
listed-company consequences
```

POWRobots should measure this graph rather than merely describe it.

---

# 1. Repository boundaries

## `powrobots`

Owns domain-specific robotics knowledge:

```text
robots
robot_models
robot_families
robot_cells
robot_components
bom_relationships
compatibility
applications
integrators
installations
service_providers
repair_events
failure_modes
training
robotics_jobs
robotics_procurement
robotics_grants
robot_trade
robot_used_market
robot_supply_signals
robot_material_dependencies
robot_company_exposure
```

## `powproducts`

Eventually owns generic physical-product primitives:

```text
product
manufacturer
mpn
offer
seller
price
currency
availability
inventory
lead_time
condition
marketplace_listing
product_identity
price_history
```

Do NOT make POWRobots duplicate this abstraction permanently.

For Layer 1 it is acceptable for POWRobots to contain adapters that materialize the same schema locally. Design those tables so they can later move into or import from `powproducts` without migration hell.

## `powrepair`

Eventually owns generic repair/service primitives:

```text
repair_provider
repair_capability
repair_quote
turnaround_time
fault
failure
part_replaced
labour_rate
service_region
```

POWRobots should extend those concepts with robotics-specific ontology.

## `powstocks`

Owns equity prices, L2, RNS, directors, shareholders and market response.

POWRobots should NOT rebuild POWStocks.

It should instead export:

```text
company_id
robotics_exposure
signal
constraint
timestamp
confidence
evidence
```

Then POWStocks can measure the market response.

---

# 2. Core design principle

Every collector MUST preserve:

```text
what did the source say?
when did the source say it?
when did we observe it?
what entity did we believe it referred to?
what transformation did we apply?
what was the confidence?
```

Never overwrite historical observations.

The minimum temporal fields are:

```text
source_published_at
source_updated_at
observed_at
valid_from
valid_to
ingested_at
```

Where fields are unavailable, retain NULL.

`observed_at` is mandatory.

This is fundamental because a disappearing listing, falling inventory count or changed lead time is often more valuable than today's value.

---

# 3. Storage architecture

Use a three-stage data lake.

```text
RAW
 ↓
NORMALIZED
 ↓
DERIVED
```

Recommended:

```text
Cloudflare R2
    raw immutable payloads

Parquet
    normalized append-only observations

DuckDB
    local analytical/query layer

Postgres
    optional later for API/application state
```

Do not require Postgres for Layer 1.

Directory convention:

```text
data/
  raw/
    source=<source>/
      year=YYYY/
        month=MM/
          day=DD/
            ...

  normalized/
    entity_type=<type>/
      year=YYYY/
        month=MM/
          ...

  derived/
    signal=<signal_name>/
      year=YYYY/
        month=MM/
```

Every raw object should have:

```text
source
collector_version
request_id
request_url_hash
retrieved_at
http_status
content_type
sha256
payload
```

Compress large raw payloads.

Do not discard raw responses after parsing.

---

# 4. Universal provenance schema

Create:

```sql
source_observation (
    observation_id,
    source_id,
    collector_version,
    observed_at,
    source_published_at,
    source_updated_at,
    source_record_id,
    source_url_hash,
    raw_object_uri,
    raw_sha256,
    parser_version,
    parse_status,
    metadata_json
)
```

And:

```sql
source_registry (
    source_id,
    name,
    authority,
    category,
    access_method,
    cadence,
    geographic_scope,
    historical_depth,
    requires_auth,
    rate_limit,
    license_notes,
    tos_notes,
    expected_fields,
    reliability_tier,
    enabled
)
```

No collector exists without a `source_registry` entry.

---

# 5. Entity graph

Everything needs stable internal IDs.

Core nodes:

```text
Organisation
Brand
RobotManufacturer
RobotFamily
RobotModel
ComponentManufacturer
Component
ComponentCategory
Distributor
MarketplaceListing
Integrator
ServiceProvider
TrainingProvider
Course
Occupation
Location
Facility
Industry
Application
Material
CommodityCode
PublicContract
Grant
ListedCompany
```

Core edges:

```text
MANUFACTURES
DISTRIBUTES
PART_OF
COMPATIBLE_WITH
USES_COMPONENT
USES_MATERIAL
INTEGRATES
SERVICES
REPAIRS
TRAINS_FOR
LOCATED_AT
DEPLOYED_AT
USED_IN
SUPPLIES
CUSTOMER_OF
SUBSIDIARY_OF
EXPOSED_TO
REPLACES
ALTERNATIVE_TO
```

Every edge should support:

```text
valid_from
valid_to
observed_at
confidence
evidence_observation_id
```

---

# 6. Robot ontology

Do not treat "robot" as one product class.

Create at least:

```text
industrial_arm
cobot
scara
delta
cartesian
amr
agv
humanoid
mobile_manipulator
warehouse_robot
agricultural_robot
construction_robot
medical_robot
inspection_robot
drone_air
drone_ground
drone_marine
autonomous_plant
```

Applications:

```text
welding
palletising
pick_place
machine_tending
assembly
packing
sorting
inspection
painting
dispensing
material_handling
warehouse_transport
agriculture
construction
healthcare
laboratory
nuclear
defence
food_processing
```

---

# 7. Robot model schema

```sql
robot_model (
    robot_model_id,
    manufacturer_id,
    family,
    model,
    aliases,
    robot_type,
    axes,
    payload_kg,
    reach_mm,
    mass_kg,
    repeatability_mm,
    max_speed,
    controller,
    power_requirement,
    ingress_rating,
    mounting_options,
    launch_date,
    discontinued_date,
    status,
    source_confidence
)
```

Preserve original source units plus normalized SI units.

Never infer a specification silently.

---

# 8. BOM / component graph

This is one of POWRobots' most important assets.

Model robot construction at multiple confidence levels.

## Tier A — exact

Specific known component:

```text
ABB IRB ...
USES_COMPONENT
specific encoder MPN
```

## Tier B — family

Known technology family:

```text
robot model
USES_COMPONENT_CATEGORY
absolute encoder
```

## Tier C — inferred architecture

Typical architecture inferred from credible engineering evidence.

Always store:

```text
relationship_confidence
relationship_type
evidence
```

Never present Tier C as an exact BOM.

Core categories:

```text
servo_motor
stepper_motor
motor_drive
servo_drive
encoder_absolute
encoder_incremental
resolver
gearbox_harmonic
gearbox_cycloidal
planetary_gearbox
bearing
linear_rail
ballscrew
controller
PLC
industrial_PC
CPU
GPU
MCU
FPGA
DRAM
NAND
SSD
network_interface
ethercat
profinet
can
camera
depth_camera
lidar
radar
force_torque_sensor
proximity_sensor
safety_scanner
light_curtain
emergency_stop
relay
contactor
power_supply
inverter
battery
BMS
connector
cable
cable_chain
gripper
vacuum_generator
pneumatic_valve
end_effector
welding_equipment
teach_pendant
fan
filter
lubricant
```

---

# 9. ROS/URDF ingestion

Treat ROS as an extraordinarily useful structured robot-model source.

URDF provides machine-readable links/joints and robot geometry.

Build collectors for known maintained repositories including:

```text
Universal Robots
ABB / ROS-Industrial
FANUC
KUKA
Yaskawa/Motoman
Staubli where available
```

Extract:

```text
manufacturer
family
model
links
joints
joint_type
axis
limits
velocity
effort
inertial data
mesh references
transmissions
hardware interfaces
repository
commit SHA
license
```

Store source commit SHA.

Never assume a URDF represents a full physical BOM.

It represents geometry/kinematics and sometimes hardware/transmission information.

A KUKA ROS2 description repository, for example, currently contains model families, meshes, URDF/xacro, joint limits and hardware-interface information. The Universal Robots ROS description currently covers numerous UR and UR-e models.

Create a Git collector that notices:

```text
new robot model
new package
model removed
joint limits changed
new driver
new hardware interface
release frequency
repository activity
```

These changes themselves can become ecosystem signals.

---

# 10. Manufacturer catalogue collectors

Seed manufacturers:

```text
ABB
FANUC
KUKA
Yaskawa / Motoman
Universal Robots
Staubli
Kawasaki
Mitsubishi Electric
Epson
Comau
Omron
Denso
Doosan
Techman
Dobot
Hanwha
Nachi
JAKA
AUBO
Unitree
Agility
Figure
Apptronik
Boston Dynamics
```

UK industrial adoption is the initial priority.

For every manufacturer maintain:

```text
manufacturer.yml
models.yml
collector.yml
```

Capture catalog changes periodically.

Fields:

```text
models available
models introduced
models retired
payload
reach
application
UK availability
UK distributor
support availability
warranty
service plans
training
replacement parts
documentation
```

Prefer APIs/catalog feeds.

Otherwise retrieve public catalogue pages at respectful cadence and preserve change hashes.

---

# 11. Electronic/component distributors

Priority collector:

## Mouser

Use official Search API.

Capture:

```text
manufacturer
manufacturer_part_number
distributor_part_number
description
category
availability
stock
lead_time
lifecycle_status
MOQ
order_multiple
price_breaks
datasheet
replacement_parts
```

The official API currently exposes inventory, pricing, specifications and lead-time-related information.

## DigiKey

Use official Product Information APIs.

Capture equivalent fields.

Use real-time detail calls for tracked parts because keyword-search values can be cached.

Do NOT poll eight million products.

Build an expanding tracked universe:

```text
robot BOM components
+ components found in manuals
+ close substitutes
+ strategically important component categories
```

This makes API quotas manageable.

---

# 12. Parts snapshots

Canonical observation:

```sql
component_market_observation (
    observed_at,
    component_id,
    distributor_id,
    sku,
    currency,
    unit_price_1,
    unit_price_10,
    unit_price_100,
    unit_price_1000,
    stock_qty,
    lead_time_days,
    lifecycle_status,
    minimum_order_qty,
    replacement_component_id,
    source_observation_id
)
```

Derived later:

```text
stock_velocity
price_velocity
lead_time_velocity
cross_distributor_dispersion
stockout_frequency
replacement_frequency
lifecycle_deterioration
```

Do not calculate sophisticated signals until the raw history works.

---

# 13. Used robot and spare-parts market

This is essential.

The secondary market reveals:

```text
installed base
obsolescence
depreciation
liquidation
replacement demand
parts scarcity
repair economics
```

## eBay UK

Use official Browse API.

GB is supported.

Track queries for:

```text
ABB robot
FANUC robot
KUKA robot
Yaskawa robot
Universal Robots
teach pendant
servo amplifier
servo motor
encoder
robot controller
robot gearbox
robot wrist
robot PCB
industrial camera
PLC
safety scanner
```

Store every listing snapshot.

Important limitation:

eBay's Marketplace Insights sales-history API is restricted and not open to new users.

Therefore do NOT pretend that absence = sale.

Infer listing outcome conservatively:

```text
active
ended_unknown
removed_unknown
observed_price_change
relisted_possible
```

Never label `sold` without evidence.

## Machineseeker

Useful discovery source.

It currently exposes a large inventory of used industrial robots with fields including:

```text
manufacturer
model
price where present
year
condition
operating hours
payload
reach
controller
location
```

Do not assume automated collection is permitted.

Create the source adapter behind a feature flag and confirm terms before production scraping.

The source registry needs:

```text
collection_allowed = unknown|yes|no
```

No bypasses.

Other candidate discovery sources:

```text
BidSpotter
Surplex
Exapro
specialist refurbished robot dealers
UK industrial auctioneers
```

Treat as optional until terms are reviewed.

---

# 14. UK robotics trade flows

This is one of the highest-value datasets.

Start with:

```text
HS 847950 = industrial robots
```

Build a version-controlled mapping:

```yaml
commodity_groups:
  finished_robots:
  motors:
  generators:
  gearboxes:
  bearings:
  electronic_control:
  sensors:
  cameras:
  semiconductors:
  memory:
  batteries:
  industrial_computers:
```

Do NOT guess codes.

Resolve them through the official UK Trade Tariff and store:

```text
commodity_code
description
valid_from
valid_to
parent
classification_version
robotics_relevance
robotics_relevance_confidence
```

HMRC publishes detailed UK Overseas Trade Statistics monthly and bulk data going back historically.

Ingest:

```text
month
flow = import/export
commodity_code
partner_country
value_gbp
net_mass
supplementary_quantity where available
```

First-order signals:

```text
UK industrial robot import value
UK industrial robot import units
average implied unit value
imports by source country
China share
Japan share
Germany share
US share
YoY growth
3m acceleration
12m acceleration
```

This may become one of the cleanest empirical measures of UK robotics deployment.

---

# 15. UK government procurement

Ingest both:

```text
Contracts Finder
Find a Tender
```

Use their OCDS outputs.

Search/query categories and text around:

```text
robot
robotics
automation
automated
autonomous
AMR
AGV
cobot
manipulator
machine vision
industrial automation
warehouse automation
surgical robot
inspection robot
drone
unmanned
```

Store the COMPLETE notices and normalized entities.

Schema:

```sql
procurement_notice (
    notice_id,
    ocid,
    stage,
    published_at,
    buyer_id,
    title,
    description,
    cpv_codes,
    value_min,
    value_max,
    currency,
    contract_start,
    contract_end,
    region,
    supplier_id,
    award_value,
    raw_observation_id
)
```

Derived eventually:

```text
robotics procurement £ / month
number of robotics tenders
number of awards
median contract size
buyer concentration
supplier concentration
sector distribution
regional distribution
tender→award conversion
```

Procurement announcements can lead realised installation.

That temporal gap matters.

---

# 16. UKRI / Innovate UK

Ingest:

```text
Gateway to Research API
UKRI opportunities
Innovate UK robotics programmes
robotics adoption hubs
skills projects
advanced manufacturing projects
```

Create:

```sql
grant_project (
    project_id,
    programme,
    title,
    recipient_org_id,
    partners,
    start_date,
    end_date,
    award_gbp,
    location,
    technology_tags,
    industry_tags,
    source
)
```

Map recipients through Companies House where possible.

This gives us:

```text
government subsidy → organisation → robotics capability → geography
```

---

# 17. Companies House

Ingest companies identified through:

```text
integrators
robot suppliers
repair shops
training providers
grant recipients
contract awardees
robotics startups
component suppliers
```

Do NOT crawl every UK company.

Resolve identified organisations.

Capture:

```text
company_number
name
aliases
status
incorporation_date
SIC
registered_location
officers
filing timestamps
charges
accounts metadata
PSC metadata where legally/publicly available
```

Preserve filing events through time.

Important derived signals later:

```text
new integrator formation
robotics company births/deaths
regional clustering
hiring vs accounts growth
grant-backed company survival
supplier consolidation
```

---

# 18. UK integrator graph

Seed from authoritative industry directories.

Automate UK / BARA is particularly useful.

Its product finder currently represents 600+ members and many equipment categories, and its robot-integrator section currently exposes dozens of UK integrators.

Also separately track BARA-certified integrators because certification is audited and time-dependent.

Store:

```sql
integrator (
    organisation_id,
    certification,
    certification_date,
    certification_expiry,
    robot_brands,
    applications,
    industries,
    regions,
    service_capabilities,
    repair_capabilities,
    commissioning,
    programming,
    maintenance,
    training
)
```

Important:

Certification must be a temporal observation.

Do not simply have:

```text
bara_certified = true
```

Use:

```text
valid_from
valid_to
observed_at
```

Potential secondary directory seeds:

```text
GTMA
Automation World UK
manufacturer partner directories
regional Made Smarter supplier lists
```

Use for discovery; resolve organisations against Companies House.

---

# 19. Deployment evidence

Direct UK installation data will be incomplete.

Therefore model `deployment_evidence`, not fictional "installations".

```sql
deployment_evidence (
    evidence_id,
    observed_at,
    organisation_id,
    facility_id,
    robot_manufacturer_id,
    robot_model_id,
    robot_count,
    application,
    evidence_type,
    confidence,
    source
)
```

Evidence can include:

```text
contract award
case study
planning document
company announcement
job posting
integrator case study
manufacturer case study
grant project
tender
annual report
used-equipment disposal
```

Then later infer:

```text
probable_robot_installation
```

only through a separate transformation.

Keep evidence and inference apart.

---

# 20. Labour / skills garden

This is a major POWRobots differentiator.

The current UK Robotics Adoption Programme explicitly recognises a skills shortage around specifying, integrating, operating and maintaining robots.

Collect:

## Apprenticeships

Government Find an Apprenticeship.

Watch terms:

```text
mechatronics
robotics
automation
PLC
maintenance
controls
servo
robot programmer
robot technician
```

The current Level 3 Mechatronics Maintenance Technician standard directly covers electrical, electronic, mechanical, fluid power, PLC, robotics and control systems.

Capture:

```text
employer
training_provider
location
salary
qualification
duration
posting_date
closing_date
skills
robot_brands if named
equipment if named
```

## Skills England

Ingest apprenticeship standards and providers.

## ONS

Historical baselines:

```text
employment by detailed occupation
engineering employment
workforce jobs by industry
producer-price data
```

## Adzuna

Official job-search API exists.

If credentials are obtainable, use it for high-frequency robotics labour demand.

Keywords:

```text
robot engineer
robot technician
automation engineer
controls engineer
PLC engineer
mechatronics technician
maintenance engineer
robot programmer
field service engineer robotics
servo engineer
```

Normalize duplicates aggressively.

Job-board volume ≠ employment.

Treat it as demand pressure.

Derived later:

```text
vacancies_per_region
salary_median
salary_velocity
skills_frequency
brand_frequency
vacancy_duration
employer_concentration
robot_jobs / manufacturing_jobs
```

---

# 21. Repair / maintenance layer

This is not optional.

For every manufacturer/model attempt to model:

```text
service interval
maintenance procedures
common fault
replaceable units
spare availability
spare price
repair provider
support status
controller generation
teach-pendant availability
legacy support
```

Sources:

```text
OEM public manuals
OEM support documentation
integrator service pages
parts distributors
secondary marketplaces
job postings
public case studies
product recalls/safety notices
```

Do not download or republish manuals where licensing forbids it.

Store metadata, extracted facts where permitted, hashes and references.

Core tables:

```sql
failure_mode
maintenance_requirement
repair_capability
spare_part
repair_provider_capability
service_observation
```

Critical signals eventually:

```text
spare_part_scarcity
legacy_robot_support_risk
service_provider_density
technician_pressure
repairability_score
replacement_pressure
```

---

# 22. UK safety / failure evidence

Ingest public OPSS product safety alerts/reports/recalls.

The government feed supports machinery as a category and can be monitored continuously.

Capture:

```text
product
brand
model
category
risk_level
failure_description
measure
recall_date
manufacturer/importer
```

Also track relevant HSE publications and incident datasets when machine-readable data exists.

Do not interpret a generic machinery incident as a robotics incident without evidence.

PUWER is useful as regulatory context because UK work equipment must be kept maintained, safe and inspected, and maintenance must be capable of being performed safely.

This makes maintenance capacity economically meaningful rather than cosmetic.

---

# 23. Producer prices

Ingest relevant ONS Producer Price Index time series.

At minimum:

```text
electrical equipment inputs
imported electrical equipment
machinery/equipment inputs
computer/electronic/electrical products
basic metals/fabricated products/machinery
```

As of September 2026 ONS is publishing monthly series through August 2026, including specific electrical-equipment and machinery input indices.

Use these only as broad cost baselines.

Do NOT substitute them for actual component prices.

---

# 24. Materials — include, but keep bounded

Yes, materials belong in POWRobots.

But NOT as a giant commodities project.

Only include a material if we can establish:

```text
material
 → component category
 → robot subsystem
```

Start with:

```text
copper
aluminium
steel
neodymium
praseodymium
dysprosium
samarium
cobalt
lithium
nickel
graphite
silicon
gallium
germanium
indium
```

Sources:

## British Geological Survey

Use the World Mineral Statistics API/OGC service.

BGS has mineral production statistics going back decades and exposes API access.

## UK Critical Minerals Intelligence Centre

Track assessments and reports.

Do NOT make raw spot commodity trading the scope of Layer 1.

---

# 25. Product hierarchy / BOM dependency

Build this structure:

```text
robot
  ├── mechanical
  │   ├── frame
  │   ├── bearing
  │   ├── gearbox
  │   └── transmission
  │
  ├── actuation
  │   ├── servo_motor
  │   ├── brake
  │   └── drive
  │
  ├── sensing
  │   ├── encoder
  │   ├── force_sensor
  │   ├── proximity
  │   └── vision
  │
  ├── compute
  │   ├── CPU
  │   ├── GPU
  │   ├── MCU
  │   ├── PLC
  │   ├── DRAM
  │   └── storage
  │
  ├── power
  │   ├── PSU
  │   ├── inverter
  │   ├── battery
  │   └── BMS
  │
  ├── safety
  │   ├── safety_controller
  │   ├── scanner
  │   ├── light_curtain
  │   └── E-stop
  │
  └── tooling
      ├── gripper
      ├── vacuum
      ├── welder
      └── custom_EOAT
```

The graph must support both:

```text
specific part
```

and:

```text
generic part category
```

because exact OEM BOMs often will not be public.

---

# 26. Identity resolution

This will make or break the project.

Create canonical IDs rather than joining strings.

Examples:

```text
"Fanuc"
"FANUC"
"Fanuc UK Limited"
"FANUC CORPORATION"
```

must be connected but not necessarily collapsed into the same legal entity.

Likewise:

```text
UR10
UR10e
Universal Robots UR10
Universal Robot UR-10
```

Create aliases.

Use deterministic rules first:

```text
company number
MPN
GTIN
manufacturer + exact model
manufacturer + normalized part number
```

Then fuzzy candidate generation.

Never let an LLM silently merge entities.

All uncertain merges go into:

```text
entity_resolution_candidate
```

with scores/evidence.

---

# 27. Source quality tiers

Assign every source:

```text
A = official government/OEM/API
B = established industry association/distributor
C = marketplace/integrator/company publication
D = third-party directory/news
E = inference
```

A derived fact should retain the quality of its evidence.

---

# 28. History/backfill

Checkpoint 1 is not finished if collectors only start today.

Backfill as much history as legitimately available.

Priority historical datasets:

```text
HMRC robot/component imports
ONS PPIs
ONS employment
Companies House
UKRI projects/grants
government procurement
BGS minerals
apprenticeships where archive is accessible
ROS repository commit history
```

For marketplaces/component inventory where historical state cannot be recreated:

```text
start accumulating NOW
```

That is the garden.

---

# 29. Cadence

Suggested:

```text
component stock/pricing       6h or daily
eBay used market              6h
OEM catalogue                 daily/weekly
robot directories             daily
jobs                           daily
apprenticeships               daily
Contracts Finder              daily
Find a Tender                 daily
Companies House identified    daily
UKRI                          daily
product safety                daily
ROS repositories              daily
HMRC trade                    monthly
ONS PPI                       monthly
BGS minerals                  annual
```

Source cadence should be configurable.

Never hard-code scheduler logic inside collectors.

---

# 30. Collector interface

Every collector should implement approximately:

```python
class Collector:
    source_id: str

    async def discover(self) -> list[SourceRecord]:
        ...

    async def fetch(self, record) -> RawObservation:
        ...

    async def normalize(self, raw) -> list[NormalizedRecord]:
        ...

    async def checkpoint(self) -> CollectorState:
        ...
```

Collectors need:

```text
idempotency
retry
backoff
rate limiting
pagination
resume checkpoints
content hashing
metrics
dead-letter handling
```

---

# 31. Never overwrite source state

If Mouser says:

```text
stock = 512
```

today and:

```text
stock = 29
```

tomorrow, preserve both.

If an integrator disappears from a directory, preserve that too.

Use snapshot tables and change events:

```sql
change_event (
    entity_id,
    field,
    old_value,
    new_value,
    first_observed_at,
    detected_at,
    source_id
)
```

---

# 32. First transformations

Only after ingestion is reliable, implement simple transparent transformations.

## Robot import pulse

```text
current 3m imports /
same 3m last year
```

## Component pressure

Combination of:

```text
stock declining
lead time increasing
price increasing
number of distributors stocking decreasing
```

## Used robot liquidity

```text
active listings
new listings
listing disappearances
median asking price
price cuts
median age
```

## Skills pressure

```text
vacancy count
salary
vacancy duration
apprenticeship openings
training capacity
```

## Integrator pressure

Possible later proxy:

```text
robotics tenders
/
estimated integrator capacity
```

## Repair pressure

```text
spare scarcity
+ technician demand
+ legacy installed base
+ used equipment age
```

These should remain formulas, not magic ML scores.

---

# 33. Future constraint graph

Eventually produce something like:

```text
{
  "constraint": "servo_encoder_supply",
  "as_of": "...",
  "direction": "tightening",
  "evidence": [
     "UK import acceleration",
     "distributor inventory decline",
     "lead-time increase",
     "price increase"
  ],
  "affected_robot_categories": [...],
  "affected_manufacturers": [...],
  "affected_companies": [...],
  "confidence": ...
}
```

But DO NOT build this before Layer 1 data quality exists.

---

# 34. Equity exposure mapping

Create the data structure now but not investment recommendations.

```sql
company_exposure (
    company_id,
    exposure_type,
    robot_entity_id,
    component_category_id,
    revenue_exposure_pct,
    geography,
    evidence,
    confidence,
    valid_from,
    valid_to
)
```

Exposure types:

```text
robot_manufacturer
component_supplier
distributor
integrator
automation_customer
repair_provider
material_supplier
compute_supplier
sensor_supplier
motion_control
industrial_software
```

This allows POWStocks later to ask:

```text
constraint appeared T0
stock reaction began T1
lag = T1 - T0
```

That lag is one of the most important eventual POW measurements.

---

# 35. UK geography

Everything possible should resolve to:

```text
postcode
latitude/longitude
ITL
local authority
region
```

---

# 36. Tests

Every collector requires fixtures.

Minimum tests:

```text
raw payload saved
same response does not duplicate logical source record
changed response creates new observation
parser handles missing fields
parser handles source schema changes
pagination works
429 retry works
5xx retry works
checkpoint resume works
timestamps are UTC
currency preserved
normalized units correct
raw provenance recoverable
```

Entity tests:

```text
aliases resolve deterministically
ambiguous names do not auto-merge
MPNs normalize safely
manufacturer identity stays separate from legal entity
```

Temporal tests:

```text
no historical observation mutated
valid_from/valid_to logical
observation chronology preserved
```

---

# 37. Data-quality reports

Every run outputs:

```text
records fetched
records parsed
records rejected
new entities
changed entities
unchanged entities
missing critical fields
HTTP failures
schema drift
collector duration
freshness lag
```

Create CLI:

```bash
powrobots status
powrobots sources
powrobots collect <source>
powrobots backfill <source>
powrobots validate
powrobots quality
powrobots query
```

---

# 38. Source registry priority

Implement in this order.

### P0 — immediately

```text
UK Trade Tariff classifications
HMRC UK trade statistics
Contracts Finder
Find a Tender
Companies House
UKRI / Gateway to Research
Skills England
Find an Apprenticeship
ONS PPI
Automate UK/BARA directory
ROS/URDF repositories
eBay Browse API
Mouser API
DigiKey API
BGS mineral API
OPSS product safety feed/pages
```

### P1

```text
Adzuna
Made Smarter case studies
MTC
AMRC
manufacturer catalogues
manufacturer partner directories
UK integrator websites
public manuals/support lifecycle
```

### P2 / terms review required

```text
Machineseeker
industrial auction sites
other used-equipment marketplaces
commercial job boards
commercial component aggregators
```

Do not block P0 on P1/P2.

---

# 39. Seeds to create immediately

Create curated seed files:

```text
seeds/
  manufacturers.yml
  robot_models.yml
  component_categories.yml
  distributors.yml
  integrators.yml
  hs_codes.yml
  search_terms.yml
  occupations.yml
  listed_companies.yml
  materials.yml
  ros_repositories.yml
```

Every seed entry includes:

```text
added_at
reason
source
confidence
```

Never hide handcrafted bootstrap data.

---

# 40. Search vocabulary

Maintain domain vocabulary explicitly.

Version vocabulary changes.

Do not bury keywords inside source code.

---

# 41. Data we explicitly do NOT need yet

Avoid:

```text
social sentiment
Twitter scraping
LLM summaries
generic AI news
robot YouTube views
beautiful dashboards
real-time Kafka infrastructure
vector databases everywhere
graph databases before schemas settle
complex agent systems
forecasting neural networks
daily investment picks
```

Those are distractions during Layer 1.

---

# 42. Why robotics gets its own POW

`powproducts` answers:

> What is happening to physical products and components?

`powrobots` answers:

> What physical resources constrain robotic labour substitution and automation?

Those are different systems.

---

# 43. First vertical causal chain to prove

Use industrial robot arms first.

Specifically begin around:

```text
ABB
FANUC
KUKA
Yaskawa
Universal Robots
```

Measure:

```text
UK finished-robot imports
        ↓
UK tenders/grants
        ↓
integrator activity
        ↓
component stock/prices
        ↓
used robot listings/prices
        ↓
robotics jobs/apprenticeships
        ↓
repair/spare signals
```

Do NOT start with humanoids.

Humanoids are strategically interesting but industrial arms currently produce much better UK observations.

After the pipeline works, add:

```text
AMRs
warehouse robotics
agricultural robotics
humanoids
```

---

# 44. Initial tracked component baskets

Construct roughly 10–30 representative components per category initially.

### Motion

```text
servo motors
servo drives
absolute encoders
harmonic reducers
cycloidal reducers
precision bearings
linear rails
```

### Control

```text
PLCs
industrial PCs
safety controllers
MCUs
industrial networking
```

### Vision/sensing

```text
industrial cameras
depth cameras
lidar
force-torque sensors
safety scanners
proximity sensors
```

### Compute

```text
embedded CPU modules
GPU modules
DRAM
industrial SSD
edge AI modules
```

### Electrical

```text
PSUs
contactors
relays
connectors
cabling
inverters
```

### Tooling

```text
electric grippers
pneumatic grippers
vacuum generators
force-control tooling
```

This becomes our first "robot inflation basket."

---

# 45. Core derived object: Robot Cost Basket

Eventually maintain:

```sql
robot_cost_basket_observation (
    basket_id,
    observed_at,
    category,
    indexed_cost,
    availability_index,
    lead_time_index,
    component_count,
    source_coverage
)
```

Then we can see whether building a robot is becoming cheaper or harder even before OEM pricing moves.

---

# 46. Core derived object: Repair Basket

Track:

```text
controllers
teach pendants
servo drives
motors
encoders
gearboxes
fans
PSUs
PCBs
batteries
cables
```

By robot family.

Derived:

```text
repair_basket_cost
repair_basket_availability
legacy_part_scarcity
```

---

# 47. Core derived object: UK Robot Adoption Pulse

Eventually:

```text
trade
+ tenders
+ grants
+ job demand
+ apprenticeship demand
+ integrator activity
+ deployment evidence
```

Do NOT simply average arbitrary z-scores.

Expose each component.

Create a composite only after enough history exists to calibrate it.

---

# 48. Core derived object: Physical Constraint Pulse

For component category `x`:

```text
inventory ↓
price ↑
lead time ↑
imports ↓ relative to demand
used prices ↑
job demand ↑
```

That is the primitive POW ultimately cares about.

Then map:

```text
constraint
→ robot models
→ manufacturers
→ suppliers
→ listed companies
```

---

# 49. Critical engineering rules

1. Raw source data is immutable.

2. Every normalized record links to provenance.

3. Every inferred relationship carries confidence.

4. Never silently merge entities.

5. Never call disappearance a sale.

6. Never call a directory count market size.

7. Never call an import value an installation count.

8. Never infer exact BOM from generic architecture.

9. Source terms/licensing are data fields.

10. A failed collector must fail loudly.

11. Historical backfill is first-class.

12. Continuous observation matters more than a fancy UI.

13. Every source should be individually runnable/testable.

14. No source-specific mess should leak into canonical tables.

15. All measurements need an `as_of` timestamp.

---

# 50. README needs to explain the thesis

README opening:

> POWRobots is a longitudinal data garden for the physical economics of robotics. It continuously records UK robot adoption, supply chains, component availability, prices, trade flows, integration capacity, repair capacity and skills demand. Its objective is to detect physical constraints before their economic consequences are fully reflected elsewhere.

Then explicitly state:

```text
raw data is not the moat

transformation
× continuous collection
× time

is the moat
```

---

# 51. Layer 1 completion criteria

Do not declare Layer 1 complete because directories and schemas exist.

It is complete only when ALL of these are true:

```text
[ ] source registry exists
[ ] raw immutable store works
[ ] normalized Parquet/DuckDB layer works
[ ] provenance is reversible
[ ] automated scheduler works
[ ] collector state/checkpointing works
[ ] historical backfills run
[ ] HMRC robot trade populated
[ ] government procurement populated
[ ] UKRI populated
[ ] Companies House resolution populated
[ ] UK integrator universe populated
[ ] apprenticeship/skills universe populated
[ ] ROS robot model universe populated
[ ] eBay observations accumulating
[ ] component distributor observations accumulating
[ ] ONS price series populated
[ ] BGS material series populated
[ ] product safety populated
[ ] basic OEM model catalogue populated
[ ] first component baskets populated
[ ] tests pass
[ ] freshness report passes
[ ] coverage report exists
[ ] failed collectors alert visibly
```

Target at least:

```text
5 major industrial robot manufacturers
100+ normalized robot models
50+ UK integrators
500+ tracked component SKUs
all available UK HS847950 history
robotics public-procurement history
UKRI robotics history
core skills/apprenticeship history
daily used-market snapshots
daily distributor snapshots
```

Numbers are minimum coverage goals, not reasons to insert junk.

---

# 52. Final output from this push

The coding agent should finish this phase with:

```text
1. working repo
2. documented source registry
3. reproducible historical backfill
4. scheduled live collectors
5. immutable raw archive
6. canonical normalized schemas
7. DuckDB analytical database
8. quality/provenance reports
9. tests
10. first genuinely growing POWRobots garden
```

Do NOT spend this push building speculative alpha models.

The success test is simpler:

> If we stop development for six months but leave the collectors running, do we return to a genuinely valuable historical robotics dataset that cannot simply be recreated from today's web?

If yes, Layer 1 is doing its job.

If no, keep working on the garden.
