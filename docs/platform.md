# Platform Architecture — Engines + Community + Marketplace

POW provides the engines. Users design and publish. Others buy.

---

## The platform model

```
POW provides:
  ├── 5 electronics engines (SENSE, REMEMBER, ACT, TALK, SEE)
  ├── Parts graph (137 components, 15 suppliers, 90 prices)
  ├── MCP tools (resolve_bom, find_substitutes, quote_build)
  ├── Manufacturing pipeline (JLCPCB → Seeed → shipped)
  └── Glimlings brand + templates

Users create:
  ├── Custom Glimling designs (Blender/Muse/any tool)
  ├── Published designs (shared with community)
  ├── Personalised collections (their own Glimlings)
  └── Store listings (sell to others)

Community marketplace:
  ├── Browse published designs
  ├── Buy pre-made Glimlings
  ├── Commission custom designs
  └── Share and remix
```

## How it works

### For the designer ( creator)
1. Open Blender (or use Muse's design tools)
2. Choose an engine (SENSE, REMEMBER, ACT, TALK, SEE)
3. Design the enclosure and character
4. POW MCP resolves the BOM automatically
5. Export design → POW assembles and ships
6. Publish to marketplace or keep private

### For the buyer ( customer)
1. Browse marketplace for pre-made Glimlings
2. Or describe what they want to Muse
3. Muse designs it via Blender MCP
4. POW resolves parts and pricing
5. Customer approves and pays
6. POW assembles and ships

### For the collector ( enthusiast)
1. Buy Glimlings from marketplace
2. Connect to Muse/ChatGPT
3. Each Glimling has its own memory and personality
4. Build a collection of connected creatures
5. Share collection with friends

## The key insight

**We don't design the products. We provide the infrastructure that lets anyone design, build, and sell them.**

The engines are the platform. The MCP is the API. The marketplace is the distribution. The community creates the value.
