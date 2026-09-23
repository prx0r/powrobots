"""POW MCP tools for Muse integration.

Exposes device status, control, and profile tools so Muse
can discover and interact with POW consumer agents.

Usage:
    python -m powrobots.mcp
"""

import asyncio
import json
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


# ─── Device Status ──────────────────────────────────────────

if HAS_MCP:
    @mcp.tool()
    async def pow_device_status(device_id: str = "") -> str:
        """Get current sensor readings from a POW device.

        Args:
            device_id: Device ID (e.g. plant-agent-001, desk-agent-001)
        """
        conn = sqlite3.connect(os.path.expanduser("~/.powops/powrobots.db"))
        try:
            rows = conn.execute(
                "SELECT * FROM source_health WHERE source_id LIKE ?",
                (f"%{device_id}%",)
            ).fetchall()
            # Also check component_market_observation for latest readings
            readings = conn.execute(
                """SELECT component_id, unit_price_1, currency, observed_at
                   FROM component_market_observation
                   WHERE component_id LIKE ?
                   ORDER BY observed_at DESC LIMIT 5""",
                (f"%{device_id}%",)
            ).fetchall()

            result = {
                "device_id": device_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "readings": [],
            }

            for r in readings:
                result["readings"].append({
                    "component": r[0],
                    "value": r[1],
                    "currency": r[2],
                    "observed_at": r[3],
                })

            return json.dumps(result, indent=2)
        finally:
            conn.close()


    @mcp.tool()
    async def pow_device_control(device_id: str, action: str, params: str = "") -> str:
        """Control a POW device actuator.

        Args:
            device_id: Device ID
            action: Control action (led, relay, servo, display)
            params: JSON parameters for the action
        """
        # In production, this would send commands to the device
        # For now, log the action
        conn = sqlite3.connect(os.path.expanduser("~/.powops/powrobots.db"))
        try:
            conn.execute(
                """INSERT INTO source_record
                (source_record_id, source_id, dataset, source_native_id,
                 retrieved_at, normalized_json, payload_hash, raw_payload_hash,
                 parser_id, parser_version)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    f"ctrl:{device_id}:{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
                    device_id, "device_control", f"ctrl_{action}",
                    datetime.now(timezone.utc).isoformat(),
                    json.dumps({"action": action, "params": params}),
                    "control", "control", "mcp", "1.0"
                )
            )
            conn.commit()
            return json.dumps({
                "device_id": device_id,
                "action": action,
                "params": params,
                "status": "sent",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
        finally:
            conn.close()


    @mcp.tool()
    async def pow_device_profile(device_id: str) -> str:
        """Get personalisation profile for a POW device.

        Args:
            device_id: Device ID
        """
        # In production, this would read from the device's config
        # For now, return a default profile
        return json.dumps({
            "device_id": device_id,
            "name": "Default Agent",
            "colour": "black",
            "personality": "friendly",
            "created_at": datetime.now(timezone.utc).isoformat(),
        })


    @mcp.tool()
    async def pow_resolve_bom(product_type: str) -> str:
        """Resolve BOM for a POW product type.

        Args:
            product_type: Product type (plant-agent, desk-agent, pet-agent, etc.)
        """
        from powrobots.resolve import resolve_bom

        bom_map = {
            "plant-agent": "pow-agent-node-plant",
            "desk-agent": "pow-agent-node-desk",
            "pet-agent": "pow-agent-node-pet",
            "lamp-agent": "pow-agent-node-lamp",
            "speaker-agent": "pow-agent-node-speaker",
            "camera-agent": "pow-agent-node-camera",
            "tiny-robot": "pow-agent-node-robot",
        }

        model_id = bom_map.get(product_type)
        if not model_id:
            return json.dumps({"error": f"Unknown product type: {product_type}"})

        result = await _run_sync(resolve_bom, model_id)
        return json.dumps(result, indent=2)


async def main():
    if not HAS_MCP:
        print("MCP not installed: pip install mcp")
        return
    await mcp.run_stdio_async()


if __name__ == "__main__":
    asyncio.run(main())
