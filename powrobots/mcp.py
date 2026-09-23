"""POW MCP Adapter — connects our tools to Muse/ChatGPT/Blender.

This is the bridge between AI agents and our parts intelligence.
Exposes resolve_bom, find_substitutes, quote_build, and submission tools.

Usage:
    python -m powrobots.mcp
"""

import asyncio
import json
import os
import sqlite3
from datetime import datetime, timezone

try:
    from mcp.server.mcpserver import MCPServer
    HAS_MCP = True
except ImportError:
    HAS_MCP = False

if HAS_MCP:
    mcp = MCPServer("pow-glimlings")


def _run_sync(fn, *args, **kwargs):
    return asyncio.get_event_loop().run_in_executor(None, lambda: fn(*args, **kwargs))


def _get_db():
    return sqlite3.connect(os.path.expanduser("~/.powops/powrobots.db"))


if HAS_MCP:
    # ─── BOM Resolution ──────────────────────────────────────

    @mcp.tool()
    async def pow_resolve_bom(model_id: str) -> str:
        """Resolve full BOM for a robot model with pricing from multiple suppliers.

        Args:
            model_id: Robot model ID (e.g. so-101, roborock-s7, pow-agent-node-plant)
        """
        from powrobots.resolve import resolve_bom
        result = await _run_sync(resolve_bom, model_id)
        return json.dumps(result, indent=2)


    @mcp.tool()
    async def pow_find_substitutes(component_id: str) -> str:
        """Find substitute parts for a component with pricing.

        Args:
            component_id: Component ID to find alternatives for
        """
        from powrobots.resolve import find_substitutes
        result = await _run_sync(find_substitutes, component_id)
        return json.dumps(result, indent=2)


    @mcp.tool()
    async def pow_optimize_bom(model_id: str, strategy: str = "cheapest") -> str:
        """Optimize BOM procurement by strategy.

        Args:
            model_id: Robot model ID
            strategy: 'cheapest' or 'fastest'
        """
        from powrobots.resolve import optimize_bom
        result = await _run_sync(optimize_bom, model_id, strategy)
        return json.dumps(result, indent=2)


    # ─── Parts Search ──────────────────────────────────────────

    @mcp.tool()
    async def pow_list_components(query: str = "", category: str = "") -> str:
        """Search components by name or category.

        Args:
            query: Search term (e.g. 'servo', 'ESP32', 'battery')
            category: Filter by category (e.g. 'servo_motor', 'sensor')
        """
        conn = _get_db()
        try:
            if query:
                rows = conn.execute(
                    "SELECT component_id, canonical_name, category, description "
                    "FROM component WHERE canonical_name LIKE ? OR description LIKE ? LIMIT 20",
                    (f"%{query}%", f"%{query}%")
                ).fetchall()
            elif category:
                rows = conn.execute(
                    "SELECT component_id, canonical_name, category, description "
                    "FROM component WHERE category = ? LIMIT 20",
                    (category,)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT component_id, canonical_name, category, description "
                    "FROM component LIMIT 20"
                ).fetchall()

            results = [{"id": r[0], "name": r[1], "category": r[2], "description": r[3]} for r in rows]
            return json.dumps({"count": len(results), "components": results}, indent=2)
        finally:
            conn.close()


    @mcp.tool()
    async def pow_robot_info(model_id: str) -> str:
        """Get detailed info about a robot model including parts and compatibility.

        Args:
            model_id: Robot model ID
        """
        conn = _get_db()
        try:
            row = conn.execute(
                "SELECT model_id, canonical_name, manufacturer_id, robot_type, "
                "axes, payload_kg, reach_mm, mass_kg "
                "FROM robot_model WHERE model_id = ?", (model_id,)
            ).fetchone()

            if not row:
                return json.dumps({"error": f"Model '{model_id}' not found"})

            parts = conn.execute(
                "SELECT c.canonical_name, c.category, pr.confidence "
                "FROM product_relation pr JOIN component c ON c.component_id = pr.dst_entity_id "
                "WHERE pr.src_entity_id = ? AND pr.relation_type = 'REQUIRES'", (model_id,)
            ).fetchall()

            subs = conn.execute(
                "SELECT c.canonical_name, pr.confidence "
                "FROM product_relation pr JOIN component c ON c.component_id = pr.src_entity_id "
                "WHERE pr.dst_entity_id = ? AND pr.relation_type = 'compatible'", (model_id,)
            ).fetchall()

            return json.dumps({
                "model": {"id": row[0], "name": row[1], "manufacturer": row[2],
                          "type": row[3], "axes": row[4], "payload_kg": row[5],
                          "reach_mm": row[6], "mass_kg": row[7]},
                "parts": [{"name": p[0], "category": p[1], "confidence": p[2]} for p in parts],
                "substitutes": [{"name": s[0], "confidence": s[1]} for s in subs],
            }, indent=2)
        finally:
            conn.close()


    # ─── Manufacturing ─────────────────────────────────────────

    @mcp.tool()
    async def pow_quote_build(model_id: str) -> str:
        """Get a full assembly quote for a robot model.

        Args:
            model_id: Robot model ID
        """
        from powrobots.resolve import resolve_bom
        bom = await _run_sync(resolve_bom, model_id)

        if "error" in bom:
            return json.dumps(bom)

        # Calculate assembly costs
        parts_cost = bom["total_estimated_cost"]
        assembly_cost = {"USD": 5.00, "GBP": 4.00}
        packaging_cost = {"USD": 3.00, "GBP": 2.50}

        total = {}
        for curr in set(list(parts_cost.keys()) + list(assembly_cost.keys()) + list(packaging_cost.keys())):
            total[curr] = parts_cost.get(curr, 0) + assembly_cost.get(curr, 0) + packaging_cost.get(curr, 0)

        return json.dumps({
            "model": bom.get("model", {}),
            "parts_cost": parts_cost,
            "assembly_cost": assembly_cost,
            "packaging_cost": packaging_cost,
            "total_estimated": {k: round(v, 2) for k, v in total.items() if v > 0},
            "components_count": len(bom.get("components", [])),
            "suppliers": bom.get("suppliers_used", []),
        }, indent=2)


    @mcp.tool()
    async def pow_list_robots(robot_type: str = "") -> str:
        """List all robot models, optionally filtered by type.

        Args:
            robot_type: Filter by type (robot_vacuum, robotic_arm, robot_mower, consumer_agent, etc.)
        """
        conn = _get_db()
        try:
            if robot_type:
                rows = conn.execute(
                    "SELECT model_id, canonical_name, manufacturer_id, robot_type "
                    "FROM robot_model WHERE robot_type = ? ORDER BY canonical_name",
                    (robot_type,)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT model_id, canonical_name, manufacturer_id, robot_type "
                    "FROM robot_model ORDER BY robot_type, canonical_name"
                ).fetchall()

            results = [{"id": r[0], "name": r[1], "manufacturer": r[2], "type": r[3]} for r in rows]
            return json.dumps({"count": len(results), "robots": results}, indent=2)
        finally:
            conn.close()


    @mcp.tool()
    async def pow_list_products(product_line: str = "") -> str:
        """List products in the Glimlings catalogue.

        Args:
            product_line: Filter by line (glimlings, etc.)
        """
        conn = _get_db()
        try:
            if product_line:
                rows = conn.execute(
                    "SELECT product_id, product_name, product_line, target_price_gbp, margin_pct "
                    "FROM product WHERE product_line = ? ORDER BY target_price_gbp",
                    (product_line,)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT product_id, product_name, product_line, target_price_gbp, margin_pct "
                    "FROM product ORDER BY product_line, target_price_gbp"
                ).fetchall()

            results = [{"id": r[0], "name": r[1], "line": r[2], "price_gbp": r[3], "margin": r[4]} for r in rows]
            return json.dumps({"count": len(results), "products": results}, indent=2)
        finally:
            conn.close()


async def main():
    if not HAS_MCP:
        print("MCP not installed: pip install mcp")
        return
    await mcp.run_stdio_async()


if __name__ == "__main__":
    asyncio.run(main())
