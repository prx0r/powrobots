# AI/MCP Tooling for 3D Design

## The Answer

**No, OpenSCAD is NOT what you submit to the supplier.** You submit **STL files**.

OpenSCAD is a design tool. STL is the output. Suppliers (JLC3DP) accept STL, STEP, or OBJ.

---

## What Suppliers Accept

| Format | JLC3DP | PCBWay | Makerfabs | Notes |
|--------|--------|--------|-----------|-------|
| **STL** | ✅ | ✅ | ✅ | Most common, universal |
| **STEP** | ✅ | ✅ | ✅ | Better for CAD, parametric |
| **OBJ** | ✅ | ✅ | ⚠️ | With textures |
| **3MF** | ✅ | ✅ | ⚠️ | Newer, includes colour |
| **STL (binary)** | ✅ | ✅ | ✅ | Smaller file size |

**For Glimlings: Submit STL files.** They're universal, simple, and accepted everywhere.

---

## AI/MCP Tools for 3D Design

### Option 1: OpenSCAD MCP (Parametric, Free)

| Tool | What It Does | Link |
|------|--------------|------|
| **openscad-mcp** | MCP server for OpenSCAD | https://github.com/dkpoulsen/openscad-mcp |
| **openscad-mcp** (Python) | Create, preview, export STL | https://github.com/sergiudanstan/openscad-mcp |
| **openscad-mcp-server** | Local OpenSCAD MCP | https://github.com/ClemensSchartmueller/openscad-mcp-server |
| **openscad-mcp** (vision) | 8-angle inspection images | https://github.com/alexlenk/openscad-mcp |

**Pros:** Free, parametric, precise, code-based
**Cons:** Steep learning curve, limited organic shapes

### Option 2: Blender MCP (Free, Full-Featured)

| Tool | What It Does | Link |
|------|--------------|------|
| **blender-mcp** | Control Blender from AI | https://github.com/MCPBlender/blender-mcp |
| **blender-mcp-pro** | 120+ tools, $15 one-time | https://github.com/youichi-uda/blender-mcp-pro |
| **blender-mcp** (AI skill) | Agent skill for Claude Code | https://github.com/jithinolickal/blender |
| **ageless-blender-mcp** | 29 tools, 4-layer architecture | https://github.com/ageless-h/blender-mcp |

**Pros:** Free, powerful, organic shapes, visual feedback
**Cons:** Requires Blender installed, complex setup

### Option 3: AI 3D Generation (Paid, Easiest)

| Tool | What It Does | Cost | Link |
|------|--------------|------|------|
| **Meshy** | Text/image to 3D, MCP server | Free tier + paid | https://www.meshy.ai/mcp |
| **Tripo** | Text/image to 3D, Blender addon | Free tier + paid | https://github.com/VAST-AI-Research/tripo-mcp |
| **Hyper3D Rodin** | Watertight meshes for printing | Paid | https://hyper3d.ai |
| **Hi3D** | AI workflow for 3D printing | Paid | https://www.hi3d.ai |

**Pros:** Easiest, fastest, print-ready output
**Cons:** Paid, less control, may not fit constraints

### Option 4: Fusion360 MCP (Free for Personal)

| Tool | What It Does | Link |
|------|--------------|------|
| **FusionMCP** | Control Fusion360 from Claude | https://github.com/Anonimus124/FusionMCP |

**Pros:** Professional CAD, precise dimensions
**Cons:** Requires Fusion360, complex setup

---

## Recommendation for Glimlings

### For Default Designs (Templates)

**Use OpenSCAD MCP** — parametric, free, precise

```
1. Create parametric templates in OpenSCAD
2. Use MCP to modify parameters (colour, name, size)
3. Export STL
4. Submit to JLC3DP
```

### For Custom Designs (Customer Requests)

**Use Meshy MCP** — fastest, print-ready

```
1. Customer describes character
2. Meshy generates 3D model
3. MCP validates against constraints
4. Export STL
5. Submit to JLC3DP
```

### For Complex Characters

**Use Blender MCP** — most control

```
1. AI designs character in Blender
2. MCP modifies mesh
3. Export STL
4. Submit to JLC3DP
```

---

## The Workflow

```
CUSTOMER: "I want a green mushroom named Sporebert"
    ↓
DESIGN MCP:
  1. Load parametric template (frog.scad)
  2. Modify parameters (colour=green, name=Sporebert)
  3. Validate against constraints
  4. Export STL
    ↓
QUOTE MCP:
  1. Calculate print cost (volume × $1.00/cm³)
  2. Add parts cost
  3. Add packaging + shipping
  4. Return quote
    ↓
ORDER MCP:
  1. Submit STL to JLC3DP
  2. Order parts from AliExpress
  3. Ship kit to customer
```

---

## What to Build

### Phase 1: Parametric Templates (Now)

1. Create OpenSCAD templates for all 8 products
2. Use OpenSCAD MCP to generate default STLs
3. Pre-print 5 of each
4. List on Etsy

### Phase 2: Custom Design MCP (Next)

1. Install Meshy MCP
2. Build validation layer (check constraints)
3. Connect to JLC3DP API
4. Allow customers to describe characters

### Phase 3: Full AI Pipeline (Later)

1. Install Blender MCP
2. Build character design agent
3. Generate unique characters
4. Auto-validate and quote

---

## The Key Insight

**OpenSCAD is the design tool. STL is the output.**

For Glimlings:
1. **Default designs:** OpenSCAD templates → STL → JLC3DP
2. **Custom designs:** Meshy/Blender → STL → JLC3DP
3. **Always:** STL files submitted to supplier

**MCP validates constraints. Suppliers build. Customers receive.**
