"""BOM resolution and substitution engine.

Implements the core procurement intelligence:
- resolve_bom: given a robot, return full BOM with prices from multiple suppliers
- find_substitutes: given a part, return alternatives with evidence
- optimize_bom: compare cost vs delivery time across suppliers
"""

import sqlite3
from typing import Optional
from .shared.db import get_db


def resolve_bom(model_id: str) -> dict:
    """Resolve a robot's complete BOM with pricing from available suppliers.

    Returns:
        {
            "model": {...},
            "components": [
                {
                    "component_id": "...",
                    "name": "...",
                    "category": "...",
                    "required": True,
                    "confidence": "declared",
                    "suppliers": [
                        {"distributor": "...", "price": 13.89, "currency": "USD", "moq": 10}
                    ],
                    "substitutes": [...]
                }
            ],
            "total_estimated_cost": {...},
            "suppliers_used": [...]
        }
    """
    conn = get_db()

    # Get model info
    model = conn.execute(
        "SELECT * FROM robot_model WHERE model_id = ?", (model_id,)
    ).fetchone()

    if not model:
        conn.close()
        return {"error": f"Model '{model_id}' not found"}

    model_dict = {
        "model_id": model[0], "manufacturer_id": model[1],
        "canonical_name": model[2], "robot_type": model[3],
        "axes": model[4], "payload_kg": model[5],
        "reach_mm": model[6], "mass_kg": model[7],
    }

    # Get required components
    req_relations = conn.execute("""
        SELECT pr.dst_entity_id, pr.confidence, pr.evidence_json,
               c.canonical_name, c.category, c.mpn, c.description
        FROM product_relation pr
        JOIN component c ON c.component_id = pr.dst_entity_id
        WHERE pr.src_entity_id = ? AND pr.relation_type = 'REQUIRES'
    """, (model_id,)).fetchall()

    components = []
    suppliers_used = set()

    for comp_id, conf, evidence, name, category, mpn, desc in req_relations:
        # Get pricing from all suppliers
        prices = conn.execute("""
            SELECT d.canonical_name, d.country_code, d.has_api,
                   cmo.unit_price_1, cmo.currency, cmo.minimum_order_qty,
                   cmo.lead_time_days, cmo.stock_qty
            FROM component_market_observation cmo
            JOIN distributor d ON d.distributor_id = cmo.distributor_id
            WHERE cmo.component_id = ?
            ORDER BY cmo.unit_price_1
        """, (comp_id,)).fetchall()

        suppliers = []
        for s_name, s_country, s_api, price, curr, moq, lead, stock in prices:
            suppliers.append({
                "distributor": s_name, "country": s_country,
                "price": price, "currency": curr,
                "moq": moq, "lead_time_days": lead, "stock": stock,
            })
            suppliers_used.add(s_name)

        # Get substitutes
        subs = conn.execute("""
            SELECT c2.canonical_name, c2.component_id, pr2.confidence
            FROM product_relation pr2
            JOIN component c2 ON c2.component_id = pr2.src_entity_id
            WHERE pr2.dst_entity_id = ? AND pr2.relation_type = 'compatible'
        """, (comp_id,)).fetchall()

        substitutes = [{"name": s[0], "id": s[1], "confidence": s[2]} for s in subs]

        components.append({
            "component_id": comp_id, "name": name, "category": category,
            "mpn": mpn, "description": desc,
            "confidence": conf, "evidence": evidence,
            "suppliers": suppliers, "substitutes": substitutes,
        })

    # Compute total estimated cost (cheapest per component)
    total = {"USD": 0, "GBP": 0, "CNY": 0, "EUR": 0}
    for comp in components:
        if comp["suppliers"]:
            cheapest = min(comp["suppliers"], key=lambda s: s["price"] or 9999)
            curr = cheapest["currency"]
            if curr in total:
                total[curr] += cheapest["price"] or 0

    conn.close()

    return {
        "model": model_dict,
        "components": components,
        "total_estimated_cost": {k: round(v, 2) for k, v in total.items() if v > 0},
        "suppliers_used": sorted(suppliers_used),
    }


def find_substitutes(component_id: str) -> dict:
    """Find substitute parts for a given component.

    Returns alternatives with compatibility evidence and pricing.
    """
    conn = get_db()

    # Get the component
    comp = conn.execute(
        "SELECT * FROM component WHERE component_id = ?", (component_id,)
    ).fetchone()

    if not comp:
        conn.close()
        return {"error": f"Component '{component_id}' not found"}

    comp_dict = {
        "component_id": comp[0], "name": comp[1],
        "manufacturer_id": comp[2], "mpn": comp[3],
        "category": comp[4], "description": comp[5],
    }

    # Find what robots use this component
    used_by = conn.execute("""
        SELECT rm.canonical_name, rm.robot_type, pr.confidence
        FROM product_relation pr
        JOIN robot_model rm ON rm.model_id = pr.src_entity_id
        WHERE pr.dst_entity_id = ? AND pr.relation_type = 'REQUIRES'
    """, (component_id,)).fetchall()

    # Find substitutes (components compatible with same robots)
    substitutes = []
    for robot_name, robot_type, _ in used_by:
        subs = conn.execute("""
            SELECT c2.canonical_name, c2.component_id, c2.category,
                   c2.mpn, pr2.confidence, pr2.evidence_json
            FROM product_relation pr2
            JOIN component c2 ON c2.component_id = pr2.src_entity_id
            WHERE pr2.dst_entity_id = (
                SELECT src_entity_id FROM product_relation
                WHERE dst_entity_id = ? AND relation_type = 'REQUIRES'
                AND src_entity_id IN (
                    SELECT src_entity_id FROM product_relation
                    WHERE dst_entity_id = ? AND relation_type = 'REQUIRES'
                )
                LIMIT 1
            ) AND pr2.relation_type = 'compatible'
            AND c2.component_id != ?
        """, (component_id, component_id, component_id)).fetchall()

        for sub in subs:
            # Get pricing for substitute
            prices = conn.execute("""
                SELECT d.canonical_name, cmo.unit_price_1, cmo.currency
                FROM component_market_observation cmo
                JOIN distributor d ON d.distributor_id = cmo.distributor_id
                WHERE cmo.component_id = ?
            """, (sub[1],)).fetchall()

            substitutes.append({
                "component_id": sub[1], "name": sub[0],
                "category": sub[2], "mpn": sub[3],
                "confidence": sub[4], "evidence": sub[5],
                "fits_robot": robot_name,
                "pricing": [{"supplier": p[0], "price": p[1], "currency": p[2]} for p in prices],
            })

    # Deduplicate substitutes
    seen = set()
    unique_subs = []
    for s in substitutes:
        key = s["component_id"]
        if key not in seen:
            seen.add(key)
            unique_subs.append(s)

    conn.close()

    return {
        "component": comp_dict,
        "used_by": [{"robot": r[0], "type": r[1], "confidence": r[2]} for r in used_by],
        "substitutes": unique_subs,
    }


def optimize_bom(model_id: str, strategy: str = "cheapest") -> dict:
    """Optimize BOM procurement by strategy.

    strategy: 'cheapest' (lowest total cost) or 'fastest' (shortest delivery)
    """
    bom = resolve_bom(model_id)

    if "error" in bom:
        return bom

    optimized = []
    for comp in bom["components"]:
        if not comp["suppliers"]:
            optimized.append({"component": comp["name"], "selected": None, "reason": "no supplier found"})
            continue

        if strategy == "cheapest":
            selected = min(comp["suppliers"], key=lambda s: s["price"] or 9999)
            reason = "lowest price"
        elif strategy == "fastest":
            with_lead = [s for s in comp["suppliers"] if s["lead_time_days"] is not None]
            selected = min(with_lead, key=lambda s: s["lead_time_days"]) if with_lead else comp["suppliers"][0]
            reason = "shortest lead time"
        else:
            selected = comp["suppliers"][0]
            reason = "first available"

        optimized.append({
            "component": comp["name"],
            "selected": selected,
            "reason": reason,
            "alternatives": len(comp["suppliers"]) - 1,
        })

    return {
        "model_id": model_id,
        "strategy": strategy,
        "items": optimized,
    }
