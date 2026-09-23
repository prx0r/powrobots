"""POW MCP tools for Muse integration.

Exposes device status, control, and BOM resolution tools
so Muse can discover and interact with POW consumer agents.

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
    mcp = MCPServer("pow-devices")


def _run_sync(fn, *args, **kwargs):
    return asyncio.get_event_loop().run_in_executor(None, lambda: fn(*args, **kwargs))


def _get_db():
    return sqlite3.connect(os.path.expanduser("~/.powops/powrobots.db"))


if HAS_MCP:
    @mcp.tool()
    async def pow_device_status(device_id: str = "") -> str:
        """Get current sensor readings from a POW device.

        Args:
            device_id: Device ID (e.g. plant-sprite-001, desk-goblin-001)
        """
        conn = _get_db()
        try:
            # Check latest device event
            rows = conn.execute(
                """SELECT normalized_json FROM source_record
                   WHERE source_id LIKE ? AND dataset = 'device_event'
                   ORDER BY retrieved_at DESC LIMIT 1""",
                (f"%{device_id}%",)
            ).fetchall()

            if rows:
                return json.dumps(json.loads(rows[0][0]), indent=2)

            return json.dumps({
                "device_id": device_id,
                "status": "no_data",
                "message": "Device not yet reporting. Check it's connected to WiFi.",
            })
        finally:
            conn.close()


    @mcp.tool()
    async def pow_device_control(device_id: str, action: str, params: str = "{}") -> str:
        """Control a POW device actuator.

        Args:
            device_id: Device ID
            action: Control action (led, relay, display, buzzer)
            params: JSON parameters (e.g. {"r": 255, "g": 0, "b": 0} for LED)
        """
        conn = _get_db()
        try:
            now = datetime.now(timezone.utc).isoformat()
            event = {
                "action": action,
                "params": json.loads(params),
                "timestamp": now,
            }
            conn.execute(
                """INSERT INTO source_record
                (source_record_id, source_id, dataset, source_native_id,
                 retrieved_at, normalized_json, payload_hash, raw_payload_hash,
                 parser_id, parser_version)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (f"ctrl:{device_id}:{now}", device_id, "device_control",
                 f"ctrl_{action}", now, json.dumps(event),
                 "control", "control", "mcp", "1.0")
            )
            conn.commit()
            return json.dumps({"device_id": device_id, "action": action, "status": "sent"})
        finally:
            conn.close()


    @mcp.tool()
    async def pow_resolve_bom(product_type: str) -> str:
        """Resolve BOM for a POW product type.

        Args:
            product_type: Product type (plant-sprite, desk-goblin, desk-companion, etc.)
        """
        from powrobots.resolve import resolve_bom

        bom_map = {
            "plant-sprite": "pow-agent-node-plant",
            "desk-goblin": "pow-agent-node-desk",
            "desk-companion": "pow-agent-node-desk",
            "lamp-agent": "pow-agent-node-lamp",
            "speaker-agent": "pow-agent-node-speaker",
            "camera-agent": "pow-agent-node-camera",
            "tiny-robot": "pow-agent-node-robot",
        }

        model_id = bom_map.get(product_type)
        if not model_id:
            return json.dumps({"error": f"Unknown product: {product_type}. Available: {list(bom_map.keys())}"})

        result = await _run_sync(resolve_bom, model_id)
        return json.dumps(result, indent=2)


    @mcp.tool()
    async def pow_find_part(query: str) -> str:
        """Find a robot part by name or description.

        Args:
            query: Part name, description, or model number
        """
        conn = _get_db()
        try:
            rows = conn.execute(
                """SELECT component_id, canonical_name, category, description
                   FROM component
                   WHERE canonical_name LIKE ? OR description LIKE ?
                   LIMIT 10""",
                (f"%{query}%", f"%{query}%")
            ).fetchall()

            results = []
            for r in rows:
                results.append({
                    "component_id": r[0],
                    "name": r[1],
                    "category": r[2],
                    "description": r[3],
                })

            return json.dumps({"query": query, "results": results, "count": len(results)})
        finally:
            conn.close()


    @mcp.tool()
    async def pow_robot_info(model_id: str) -> str:
        """Get information about a robot model.

        Args:
            model_id: Robot model ID (e.g. roborock-s7, so-101)
        """
        conn = _get_db()
        try:
            row = conn.execute(
                """SELECT model_id, canonical_name, manufacturer_id, robot_type,
                          axes, payload_kg, reach_mm, mass_kg
                   FROM robot_model WHERE model_id = ?""",
                (model_id,)
            ).fetchone()

            if not row:
                return json.dumps({"error": f"Model '{model_id}' not found"})

            # Get parts
            parts = conn.execute(
                """SELECT c.canonical_name, c.category, pr.confidence
                   FROM product_relation pr
                   JOIN component c ON c.component_id = pr.dst_entity_id
                   WHERE pr.src_entity_id = ? AND pr.relation_type = 'REQUIRES'""",
                (model_id,)
            ).fetchall()

            # Get compatible substitutes
            subs = conn.execute(
                """SELECT c.canonical_name, pr.confidence
                   FROM product_relation pr
                   JOIN component c ON c.component_id = pr.src_entity_id
                   WHERE pr.dst_entity_id = ? AND pr.relation_type = 'compatible'""",
                (model_id,)
            ).fetchall()

            return json.dumps({
                "model_id": row[0],
                "name": row[1],
                "manufacturer": row[2],
                "type": row[3],
                "axes": row[4],
                "payload_kg": row[5],
                "reach_mm": row[6],
                "mass_kg": row[7],
                "parts": [{"name": p[0], "category": p[1], "confidence": p[2]} for p in parts],
                "substitutes": [{"name": s[0], "confidence": s[1]} for s in subs],
            }, indent=2)
        finally:
            conn.close()


    @mcp.tool()
    async def pow_find_substitutes(component_id: str) -> str:
        """Find substitute parts for a component.

        Args:
            component_id: Component ID to find alternatives for
        """
        conn = _get_db()
        try:
            # Get the component
            comp = conn.execute(
                "SELECT canonical_name, category, description FROM component WHERE component_id = ?",
                (component_id,)
            ).fetchone()

            if not comp:
                return json.dumps({"error": f"Component '{component_id}' not found"})

            # Find substitutes
            subs = conn.execute(
                """SELECT c.canonical_name, c.component_id, c.category, pr.confidence
                   FROM product_relation pr
                   JOIN component c ON c.component_id = pr.src_entity_id
                   WHERE pr.dst_entity_id = ? AND pr.relation_type = 'compatible'""",
                (component_id,)
            ).fetchall()

            # Get pricing for each
            results = []
            for name, cid, cat, conf in subs:
                prices = conn.execute(
                    """SELECT d.canonical_name, cmo.unit_price_1, cmo.currency
                       FROM component_market_observation cmo
                       JOIN distributor d ON d.distributor_id = cmo.distributor_id
                       WHERE cmo.component_id = ?""",
                    (cid,)
                ).fetchall()
                results.append({
                    "name": name, "id": cid, "category": cat,
                    "confidence": conf,
                    "pricing": [{"supplier": p[0], "price": p[1], "currency": p[2]} for p in prices],
                })

            return json.dumps({
                "component": comp[0],
                "category": comp[1],
                "substitutes": results,
                "count": len(results),
            }, indent=2)
        finally:
            conn.close()


async def main():
    if not HAS_MCP:
        print("MCP not installed: pip install mcp")
        return
    await mcp.run_stdio_async()


if __name__ == "__main__":
    asyncio.run(main())
