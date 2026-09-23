"""Parametric enclosure generator for POW consumer agents.

Generates STL files for 3D-printable enclosures with parametric customisation.

Usage:
    python enclosures/generate.py --product plant-sprite --shape mushroom --colour purple
    python enclosures/generate.py --product desk-goblin --shape goblin --colour green
    python enclosures/generate.py --list-shapes
"""

import argparse
import math
import os
import numpy as np
from stl import mesh


# ─── Shapes ───────────────────────────────────────────────────

def create_box(w, h, d, wall=2.0):
    """Create a box mesh (open top)."""
    t = wall
    verts = [
        [0,0,0],[w,0,0],[w,d,0],[0,d,0],        # bottom
        [0,0,h],[w,0,h],[w,d,h],[0,d,h],        # top outer
        [t,t,h],[w-t,t,h],[w-t,d-t,h],[t,d-t,h], # top inner
        [t,t,t],[w-t,t,t],[w-t,d-t,t],[t,d-t,t], # bottom inner
    ]
    faces = [
        [0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7], # sides
        [0,3,2,1],[4,5,6,7],                       # bottom, top rim
        [8,9,10,11],[12,13,14,15],                  # inner
        [0,4,8,12],[1,5,9,13],[2,6,10,14],[3,7,11,15], # inner walls
    ]
    m = mesh.Mesh(np.zeros(len(faces), dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            m.vectors[i][j] = verts[f[j]]
    return m


def create_cylinder(radius, height, segments=32, wall=2.0):
    """Create a cylinder mesh (open top)."""
    verts = []
    faces = []
    r_inner = radius - wall

    for i in range(segments):
        angle = 2 * math.pi * i / segments
        x_outer = radius * math.cos(angle)
        y_outer = radius * math.sin(angle)
        x_inner = r_inner * math.cos(angle)
        y_inner = r_inner * math.sin(angle)
        verts.extend([
            [x_outer, y_outer, 0],      # bottom outer
            [x_inner, y_inner, 0],      # bottom inner
            [x_outer, y_outer, height], # top outer
            [x_inner, y_inner, height], # top inner
        ])

    for i in range(segments):
        j = (i + 1) % segments
        b1, b2, t1, t2 = i*4, j*4, i*4+2, j*4+2
        faces.extend([
            [b1, b2, t2, t1],           # outer wall
            [b1+1, b2+1, t2+1, t1+1],   # inner wall
            [b1, b1+1, t1+1, t1],       # bottom ring
        ])

    m = mesh.Mesh(np.zeros(len(faces), dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            m.vectors[i][j] = verts[f[j]]
    return m


# ─── Product generators ──────────────────────────────────────

SHAPES = {
    "box": lambda w=80, h=40, d=60: create_box(w, h, d),
    "mushroom": lambda w=60, h=50, d=60: create_cylinder(w/2, h, 32),
    "sphere": lambda w=60, h=50, d=60: create_cylinder(w/2, h, 32),
    "tower": lambda w=50, h=70, d=50: create_box(w, h, d),
    "flat": lambda w=100, h=20, d=70: create_box(w, h, d),
}

PRODUCTS = {
    "plant-sprite": {
        "default_shape": "mushroom",
        "parts": ["body", "sensor-mount", "led-diffuser"],
        "dimensions": {"width": 60, "height": 50, "depth": 60},
        "description": "Plant monitoring companion",
    },
    "desk-goblin": {
        "default_shape": "box",
        "parts": ["body", "display-bezel", "encoder-mount"],
        "dimensions": {"width": 100, "height": 35, "depth": 70},
        "description": "AI assistant status companion",
    },
    "desk-companion": {
        "default_shape": "box",
        "parts": ["body"],
        "dimensions": {"width": 80, "height": 30, "depth": 50},
        "description": "Simple non-connected desk creature",
    },
    "weather-mushroom": {
        "default_shape": "mushroom",
        "parts": ["body", "led-diffuser"],
        "dimensions": {"width": 60, "height": 55, "depth": 60},
        "description": "Weather-reactive mushroom",
    },
    "mood-mushroom": {
        "default_shape": "mushroom",
        "parts": ["body", "led-diffuser"],
        "dimensions": {"width": 55, "height": 45, "depth": 55},
        "description": "Mood display mushroom",
    },
}


def generate(product, shape=None, colour="black", output_dir="enclosures"):
    """Generate enclosure STL files for a product."""
    os.makedirs(output_dir, exist_ok=True)

    config = PRODUCTS.get(product)
    if not config:
        print(f"Unknown product: {product}")
        print(f"Available: {', '.join(PRODUCTS.keys())}")
        return None

    shape = shape or config["default_shape"]
    dims = config["dimensions"]

    result = {"product": product, "shape": shape, "colour": colour, "files": []}

    # Generate body
    body_fn = SHAPES.get(shape, SHAPES["box"])
    body = body_fn(dims["width"], dims["height"], dims["depth"])
    body_path = os.path.join(output_dir, f"{product}-body.stl")
    body.save(body_path)
    result["files"].append(body_path)
    print(f"  {product}-body.stl")

    # Generate accessory parts
    for part in config["parts"][1:]:  # Skip body (already generated)
        part_mesh = create_box(20, 15, 10, wall=1.5)
        part_path = os.path.join(output_dir, f"{product}-{part}.stl")
        part_mesh.save(part_path)
        result["files"].append(part_path)
        print(f"  {product}-{part}.stl")

    return result


def main():
    parser = argparse.ArgumentParser(description="POW Enclosure Generator")
    parser.add_argument("--product", choices=PRODUCTS.keys(), help="Product to generate")
    parser.add_argument("--shape", choices=SHAPES.keys(), help="Override default shape")
    parser.add_argument("--colour", default="black", help="Enclosure colour")
    parser.add_argument("--output", default="enclosures", help="Output directory")
    parser.add_argument("--list-products", action="store_true", help="List available products")
    parser.add_argument("--list-shapes", action="store_true", help="List available shapes")
    args = parser.parse_args()

    if args.list_products:
        for name, config in PRODUCTS.items():
            print(f"  {name:20s} {config['description']}")
        return

    if args.list_shapes:
        for name in SHAPES:
            print(f"  {name}")
        return

    if not args.product:
        parser.print_help()
        return

    result = generate(args.product, shape=args.shape, colour=args.colour, output_dir=args.output)
    if result:
        print(f"\nGenerated {len(result['files'])} STL files for {args.product}")
        for f in result["files"]:
            print(f"  {f}")


if __name__ == "__main__":
    main()
