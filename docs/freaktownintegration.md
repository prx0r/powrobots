# Glimlings × Freak Town: the physical character studio

I reviewed `prx0r/freaktown`. There's a substantial amount you can reuse. In fact, Freak Town has already explored much of the digital character side of Glimlings: generating personalities and portraits, assigning voices, creating 3D avatars, animating them, maintaining character bundles and publishing them.

The opportunity is to take that character creation system and add the missing half: a verified physical design, electronics, manufacturing and fulfilment pipeline.

Imagine a creator designing a mischievous mushroom in Glimlings Studio. Their character could exist as a digital companion, but customers could also buy it as a garden sensor, a bedside clock or a desktop AI button. Every physical version would share the character's appearance and personality, while using a tested hardware module.

Freak Town has the foundations for the first part. POW's parts graph and manufacturing infrastructure would supply the second.

## 1. What to reuse from Freak Town

| Existing implementation | Application to Glimlings |
| --- | --- |
| [Character packs](https://github.com/prx0r/freaktown/blob/main/docs/CHARACTER_PACK.md) | Identity, personality, voice, portrait, 3D body and version history |
| [3D character stage](https://github.com/prx0r/freaktown/blob/main/apps/live/src/pages/ThreeWsStagePage.tsx) | Preview creatures moving, speaking and reacting |
| [Character design editor](https://github.com/prx0r/freaktown/blob/main/static/editor.html) | Starting point for conversational design and iterative character creation |
| [Asset and bundle validation](https://github.com/prx0r/freaktown/tree/main/contracts) | Reproducible, versioned designs with validated assets and hashes |
| [Voice infrastructure](https://github.com/prx0r/freaktown/tree/main/backend/services/tts) | Voice selection, audio previews and optional personalised greetings |
| [Motion system](https://github.com/prx0r/freaktown/blob/main/backend/services/motion_compiler.py) | Reusable animation behaviours for digital characters |

The character-pack approach is especially relevant. Freak Town already treats identity, appearance, voice and animation capabilities as separate elements rather than tying everything to one avatar provider.

Keep that separation. One Glimling can have a beautifully animated digital body, a simple printable figurine and a physical garden-sensor variant without pretending all three are the same technical asset.

The one thing I would not do is move Freak Town wholesale into the Glimlings repository. Its comedy, live-show, judging and performance infrastructure is mostly unrelated to making garden creatures. Extract the reusable character contracts, editor ideas, rendering and asset-management components, then connect those to POW.

## 2. The important caveat from the repository review

Freak Town's current Flask application includes an actual three.ws generation path: portrait to Forge, then a GLB avatar stored in the character bundle. Its stage can animate a static creature with simple movement and use richer facial animation when the model supports it.

But I wouldn't treat the entire repository as production-ready infrastructure. The latest commit I found is September 8, 2026, and its GitHub Actions run failed in both the Python tests and browser tests. Contract and format validation passed. The imported React stage also references modules that aren't present at the expected paths in the current repository tree. [Latest CI run](https://github.com/prx0r/freaktown/actions/runs/34282926217).

Reuse the architecture and selected working components, but verify them independently before building Glimlings on top. Otherwise you risk importing Freak Town's unrelated migration and deployment problems into a new consumer product.

The other major distinction is that Freak Town validates a character for digital performance. Glimlings must additionally validate it for physical production: real dimensions, printable geometry, a compatible electronic capsule, safe assembly and a manufacturer willing to produce it.

## 3. The design stack I'd use

The strongest approach is a hybrid: AI generates the character's appearance, while a deterministic CAD system ensures that the physical product can actually be manufactured.

| Layer | Technology | Responsibility |
| --- | --- | --- |
| Conversational design | Muse when supported; another MCP-capable assistant initially | Interpret the customer's ideas and refine the design |
| Character artwork | Quiver Arrow 2 | Faces, eyes, expression sets, patterns and decorative motifs |
| Digital character generation | three.ws | Generate optional 3D characters from prompts or reference images |
| 3D editing | Blender and Blender MCP | Clean up character meshes, arrange decorative features, render previews |
| Mechanical CAD | build123d or CadQuery | Precise internal enclosures, PCB mounts, gaskets, connectors and interchangeable fittings |
| Customer preview | Three.js | Display the exact proposed physical design, colours, scale and accessories |
| Manufacturing | JLC3DP initially, with additional suppliers later | Quote and produce approved designs |
| Physical intelligence | POW's existing parts and supplier graph | Verified component compatibility, costs, revisions and repair data |

Quiver's Arrow 2 has an official text-to-SVG API and an image-to-SVG API, plus a hosted MCP server. That makes it suitable for your proposed AI design conversation.

For digital bodies, three.ws already exposes generation, rigging and conversational refinement. Its documented Forge pipeline includes image-conditioned and geometry-first generation and several quality tiers. Freak Town has already integrated parts of those APIs.

For physical engineering, build123d provides exact parametric models through Python. It is designed for applications including 3D printing and can generate families of components by changing parameters.

The key architectural rule is that the 3D avatar and the printable model are different deliverables. A character that looks perfect in a browser might contain paper-thin wings, disconnected geometry or decorative features that cannot survive printing.

### One character, three representations

- **The original Glimling** — Name, personality, appearance, creator, artwork, voice and design history.
- **Digital body** — GLB or VRM avatar, animations, facial expressions and character dialogue.
- **Physical body** — Validated enclosure, printable shell, exact electronics, assembly and test specification.
- **Connected identity** — A customer-owned device identity and clearly defined capabilities exposed through POW's approved assistant integrations.

## 4. How the customer design experience should work

Imagine an independent Etsy creator designs magical garden creatures.

They open Glimlings Studio and ask their AI to create a tiny, round, moss-covered pixie with oversized ears and an unnecessarily large mushroom hat. They approve the initial artwork, refine the expression and choose a standard garden-sensor body.

The studio then generates a design that fits the electronics. The creator can change the ears, hat, face, colours, accessories and nameplate while the internal electronics housing remains protected.

### Example: Mossbert

A little garden guardian with an enormous mushroom hat.

*Illustrative concept, not a verified production design.*

**Customisable appearance:** Hat shape, ear size, facial expression, accessories, colours and personalised nameplate.

**Available physical abilities:** NFC identity, optional moisture sensing and a status light.

### The proposed buying experience

1. Describe or select a character, then refine its appearance through conversation.
2. Choose what it does: garden guardian, desk companion, decorative gift or another supported hardware configuration.
3. Preview the actual manufactured dimensions and colours, not just an AI illustration.
4. Receive an accurate quote covering fabrication, electronics, testing, delivery and the creator's royalty.
5. Order the Glimling. Its final files and component revisions are frozen and sent for production.
6. Pair it to your account after delivery and optionally connect it to your personal AI.

That could become a compelling experience for both buyers and creators. The digital character is instantly shareable; the physical version is something people can actually purchase.

## 5. The easiest route to custom manufacturing

Initially, don't allow users to generate arbitrary, mechanically unconstrained bodies and automatically send them to a printer.

Define a small number of physical platforms with fixed interfaces: garden stake, tabletop figurine, bedside clock and desktop button. Each platform has an exact electronics volume, fastening method, cable routing and material requirements.

The creative system can produce different outer bodies, but it must preserve those interfaces. The printable output should then pass geometry checks and human review before going to a manufacturer.

For generated sculpture-style meshes, Meshy and Tripo are additional providers worth testing. Both expose model-generation and export APIs, including printable formats, but an STL export is not proof that a model is structurally sound or fits your electronics. Tripo explicitly permits commercial use of outputs from paid plans, while its free-tier terms differ.

Blender MCP can speed up experimental modelling. Its current community implementation connects an AI agent to Blender and can execute Python inside the application. Its documentation warns that the socket has no built-in authentication or encryption, and it offers a restricted safe mode. Keep experimental agents isolated and never expose unrestricted Blender execution to arbitrary marketplace users.

For actual supplier integration, JLC3DP has a published Pricing API and a more comprehensive Ordering API covering file submission, quoting, ordering and order-status tracking. Access requires application and approval, with the fuller ordering interface directed at established commercial partners. Start with manual manufacturer quotes and automate only after access has been approved.

## 6. The creator marketplace

This is the expansion that could turn Glimlings into considerably more than an Etsy shop.

### A creator's Glimlings shop

Illustrative listing and economics.

| Example sale | Hypothetical amount |
| --- | --- |
| Customer retail price | £39 |
| Manufacturing, packing and delivery | £19 |
| Platform, payment and support allocation | £8 |
| Creator royalty | £5 |
| Remaining contribution | £7 |

*Illustrative unit economics only; costs, VAT, product testing, returns and seller obligations need to be established before launch.*

I'd distinguish three relationships: customers commissioning a private design, independent creators publishing designs on the Glimlings marketplace, and customers buying your own original Glimlings through Etsy.

On your own marketplace, creators could receive royalties on qualified sales under an explicit commercial licence. Track original authorship, permitted derivatives, use of third-party assets, production rights and whether a design is exclusive.

For Etsy, apply more care. Etsy allows seller-designed products and appropriately disclosed production partners, including buyer-personalised products. It generally prohibits reselling ordinary commercially available goods that the Etsy seller neither designed nor meaningfully customised. An unrestricted marketplace of unrelated third-party designs is therefore better hosted on your own site, rather than automatically copied into your Etsy shop.

Creator royalties should attach to the specific approved design revision. A generic mushroom shape, an internally generated variation and a substantial derivative created by another artist may have different ownership and licensing implications. Record these before accepting listings rather than resolving disputes after sales.

## 7. The development plan I'd give your coding agent

Build the minimum version as a distinct Glimlings application, extracting selected Freak Town components and referencing POW's physical-component catalogue.

| Checkpoint | Implementation | Acceptance test |
| --- | --- | --- |
| 1. Character kernel | Versioned character schema, creator identity, artwork, optional avatar, physical-platform selection and design history | Save, reopen, duplicate and branch a character without losing provenance |
| 2. Design studio | Conversational design, Arrow 2 artwork, Blender/three.ws adapters and interactive preview | Create and modify a fictional character through three independent design iterations |
| 3. Mechanical compiler | Fixed physical platforms, parametric component interfaces, geometry validation and manufacturing exports | Produce a valid garden-shell assembly with correct electronic clearances |
| 4. Quoting | BOM resolution, fabrication cost, packaging, shipping and creator royalty calculation | Quote identical frozen designs consistently and reject unsupported configurations |
| 5. Marketplace | Creator profiles, versioned listings, licences, purchasing, order states and payout ledger | Complete a simulated creator sale, cancellation and refund |
| 6. Device onboarding | Device identity, provisioning, approved capabilities and assistant-facing tools | Pair a fictional sensor without allowing access to another customer's device |
| 7. Manufacturing pilot | Actual printed and assembled samples, supplier receipts and quality-control records | Verify physical fit, function, appearance, assembly time and delivered cost |

The first end-to-end deliverable should be modest but complete: a customer designs a named garden creature from an approved shell family, previews its exact configuration, receives a quote and buys a fabricated personalised figurine. Add the tested sensor module as the next product.

Retain the actual design files, material and supplier information, fabrication outcome, assembly instructions, rejected prototypes and repair records. Those are the observations that make the POW manufacturing graph increasingly useful.

## 8. Focus: engine development

For Freak Town specifically, extract the character-bundle concept, existing could be useful in the future but maybe premature for now basically i think the focus should be on developing as many engines as possible to find the limitations of what's possible given our assembly line.

### Why engines first

The assembly line is the constraint. Before building a marketplace or character studio, we need to know:

- What combinations of components can actually be assembled reliably?
- What are the failure modes for each engine?
- What tolerances does JLC3DP achieve for our enclosure designs?
- How long does assembly take per engine type?
- What's the minimum viable test for each engine?

### Engine development priorities

| Engine | Status | Next step | Assembly risk |
| --- | --- | --- | --- |
| SENSE | Defined, parts in graph | Build first prototype | Low |
| REMEMBER | Defined, parts in graph | Build first prototype | Low |
| ACT | Defined, parts in graph | Build first prototype | Low |
| TALK | Defined, parts in graph | Build first prototype | Medium (speaker mounting) |
| SEE | Defined, parts in graph | Build first prototype | Medium (camera alignment) |
| COMPANION | Defined, parts in graph | Build first prototype | High (touchscreen + camera + NFC) |

### What we learn from each engine

| Engine | Learning goal |
| --- | --- |
| SENSE | Sensor accuracy, calibration, enclosure sealing |
| REMEMBER | RTC drift, SD card reliability, data persistence |
| ACT | Servo precision, LED brightness, relay switching |
| TALK | Speaker quality, microphone sensitivity, button durability |
| SEE | Camera resolution, image processing, low-light performance |
| COMPANION | Touchscreen responsiveness, GPS accuracy, fall detection reliability |

### Assembly line validation

For each engine, document:

1. **Component sourcing** — Can we get all parts from LCSC/JLCPCB?
2. **PCB design** — Does it fit on a standard 2-layer board?
3. **Enclosure** — Can JLC3DP print it with acceptable tolerances?
4. **Assembly** — How many minutes per unit?
5. **Testing** — What's the minimum test suite?
6. **Failure modes** — What breaks first?
7. **Cost** — What's the real COGS at 10, 100, 1000 units?

Once we have 6 working engines, we'll know exactly what the assembly line can and cannot do. That's when the character marketplace becomes viable — because we'll know which physical platforms are actually manufacturable.
