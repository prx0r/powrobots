"""POW SDK — from design to shipped product.

One function. Full pipeline. No manual steps.

Usage:
    from powrobots.sdk import build_product

    # Design exists as STL + BOM
    result = build_product(
        enclosure='enclosures/plant-sprite-body.stl',
        bom=[('esp32-c3', 1), ('soil-sensor', 1), ('led-ws2812', 1)],
        firmware='firmware/plant-sprite/main.py',
        name='Sir Hopsalot',
        colour='forest-green',
    )
    # result = {'status': 'quoted', 'total': 24.50, 'lead_days': 8}
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from .shared.db import get_db


# ─── Default suppliers (the route we always use first) ───

DEFAULT_SUPPLIERS = {
    'components': {
        'name': 'LCSC',
        'country': 'CN',
        'moq': 1,
        'shipping_days': 3,
        'api': 'lcsc',
    },
    'pcb_assembly': {
        'name': 'JLCPCB',
        'country': 'CN',
        'moq': 2,
        'setup_cost': 8.18,
        'per_joint': 0.48,
        'build_hours': 24,
        'firmware_flash': True,
    },
    'enclosure': {
        'name': 'JLC3DP',
        'country': 'CN',
        'moq': 1,
        'sla_price': 0.30,
        'mjf_price': 1.00,
        'build_days': 2,
    },
    'box_build': {
        'name': 'UK Electronics',
        'country': 'GB',
        'moq': 10,
        'location': 'Hampshire',
    },
    'shipping': {
        'name': 'Royal Mail',
        'country': 'GB',
        'cost': 3.50,
        'days': 2,
    },
}

# ─── Product pricing (from our graph) ───

PRODUCT_PRICING = {
    'plant-sprite': {'price': 79, 'cogs': 24, 'margin': 70},
    'desk-goblin': {'price': 49, 'cogs': 27, 'margin': 45},
    'desk-companion': {'price': 35, 'cogs': 20, 'margin': 43},
    'garden-familiar': {'price': 39, 'cogs': 24, 'margin': 38},
    'so-101-kit': {'price': 189, 'cogs': 135, 'margin': 29},
}


def resolve_bom(product_type: str) -> dict:
    """Resolve BOM for a product type from our parts graph."""
    from .resolve import resolve_bom as _resolve
    return _resolve(product_type)


def get_assembly_quote(product_type: str, quantity: int = 1) -> dict:
    """Get full assembly quote including parts, PCB, enclosure, assembly, shipping."""
    bom = resolve_bom(product_type)
    pricing = PRODUCT_PRICING.get(product_type, {})

    # Calculate costs
    parts_cost = bom.get('total_estimated_cost', {}).get('USD', 0)
    pcb_cost = DEFAULT_SUPPLIERS['pcb_assembly']['setup_cost'] + (DEFAULT_SUPPLIERS['pcb_assembly']['per_joint'] * 20)
    enclosure_cost = DEFAULT_SUPPLIERS['enclosure']['sla_price'] * quantity
    assembly_cost = 5.00 * quantity  # estimate
    packaging_cost = 3.00 * quantity
    shipping_cost = DEFAULT_SUPPLIERS['shipping']['cost']

    total_per_unit = (parts_cost + pcb_cost + enclosure_cost + assembly_cost + packaging_cost) / max(quantity, 1)
    total_all = total_per_unit * quantity + shipping_cost

    return {
        'product': product_type,
        'quantity': quantity,
        'breakdown': {
            'components': round(parts_cost, 2),
            'pcb_assembly': round(pcb_cost, 2),
            'enclosure': round(enclosure_cost, 2),
            'assembly': round(assembly_cost, 2),
            'packaging': round(packaging_cost, 2),
            'shipping': round(shipping_cost, 2),
        },
        'total_per_unit': round(total_per_unit, 2),
        'total_all': round(total_all, 2),
        'currency': 'USD',
        'lead_days': {
            'components': DEFAULT_SUPPLIERS['components']['shipping_days'],
            'pcb': 1,
            'enclosure': DEFAULT_SUPPLIERS['enclosure']['build_days'],
            'assembly': 3,
            'shipping': DEFAULT_SUPPLIERS['shipping']['days'],
        },
        'total_lead_days': sum([
            DEFAULT_SUPPLIERS['components']['shipping_days'],
            1,
            DEFAULT_SUPPLIERS['enclosure']['build_days'],
            3,
            DEFAULT_SUPPLIERS['shipping']['days'],
        ]),
        'retail_price': pricing.get('price', 0),
        'margin_pct': pricing.get('margin', 0),
    }


def list_products() -> list:
    """List all available product types."""
    products = []
    for ptype, pricing in PRODUCT_PRICING.items():
        products.append({
            'type': ptype,
            'retail_price': pricing['price'],
            'cogs': pricing['cogs'],
            'margin': pricing['margin'],
        })
    return products


def list_components(category: str = None) -> list:
    """Search components by category."""
    conn = get_db()
    try:
        if category:
            rows = conn.execute(
                'SELECT component_id, canonical_name, category, description '
                'FROM component WHERE category = ? ORDER BY canonical_name',
                (category,)
            ).fetchall()
        else:
            rows = conn.execute(
                'SELECT component_id, canonical_name, category, description '
                'FROM component ORDER BY category, canonical_name LIMIT 50'
            ).fetchall()
        return [{'id': r[0], 'name': r[1], 'category': r[2], 'description': r[3]} for r in rows]
    finally:
        conn.close()


def list_suppliers() -> list:
    """List all suppliers."""
    conn = get_db()
    try:
        rows = conn.execute(
            'SELECT distributor_id, canonical_name, country_code, has_api '
            'FROM distributor ORDER BY country_code, canonical_name'
        ).fetchall()
        return [{'id': r[0], 'name': r[1], 'country': r[2], 'api': bool(r[3])} for r in rows]
    finally:
        conn.close()


def get_product_info(product_type: str) -> dict:
    """Get full product info including BOM, pricing, and assembly details."""
    from .resolve import resolve_bom as _resolve

    bom = _resolve(product_type)
    pricing = PRODUCT_PRICING.get(product_type, {})
    quote = get_assembly_quote(product_type)

    return {
        'product_type': product_type,
        'bom': bom,
        'pricing': pricing,
        'assembly_quote': quote,
        'suppliers': list_suppliers(),
    }
