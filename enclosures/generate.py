"""Parametric enclosure generator for POW consumer agents.

Generates STL files for 3D-printable enclosures.
Uses numpy-stl for programmatic STL generation.

Usage:
    python -m powrobots.enclosures.generate --product plant-agent --colour black
    python -m powrobots.enclosures.generate --product desk-agent --name Gerald
"""

import argparse
import math
import os
import numpy as np
from stl import mesh


def create_box(width, height, depth, wall_thickness=2.0):
    """Create a simple box mesh (open top)."""
    w, h, d = width, height, depth
    t = wall_thickness

    vertices = [
        # Bottom face
        [0, 0, 0], [w, 0, 0], [w, d, 0], [0, d, 0],
        # Top outer
        [0, 0, h], [w, 0, h], [w, d, h], [0, d, h],
        # Top inner (open top)
        [t, t, h], [w-t, t, h], [w-t, d-t, h], [t, d-t, h],
        # Bottom inner
        [t, t, t], [w-t, t, t], [w-t, d-t, t], [t, d-t, t],
    ]

    faces = [
        [0, 1, 5, 4],  # front
        [1, 2, 6, 5],  # right
        [2, 3, 7, 6],  # back
        [3, 0, 4, 7],  # left
        [0, 3, 2, 1],  # bottom outer
        [4, 5, 6, 7],  # top outer rim
        [8, 9, 10, 11],  # top inner rim
        [12, 13, 14, 15],  # bottom inner
        [0, 4, 8, 12],  # inner front
        [1, 5, 9, 13],  # inner right
        [2, 6, 10, 14],  # inner back
        [3, 7, 11, 15],  # inner left
    ]

    m = mesh.Mesh(np.zeros(len(faces), dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            m.vectors[i][j] = vertices[f[j]]
    return m


def generate_plant_agent_enclosure(colour="black", output_dir="enclosures"):
    """Generate enclosure for Plant Agent."""
    os.makedirs(output_dir, exist_ok=True)

    # Main body: 80mm x 60mm x 40mm
    body = create_box(80, 60, 40, wall_thickness=2.0)
    body_path = os.path.join(output_dir, "plant-agent-body.stl")
    body.save(body_path)
    print(f"Generated: {body_path}")

    # Sensor mount: 20mm x 15mm x 10mm (attaches to side)
    sensor_mount = create_box(20, 15, 10, wall_thickness=1.5)
    sensor_path = os.path.join(output_dir, "plant-agent-sensor-mount.stl")
    sensor_mount.save(sensor_path)
    print(f"Generated: {sensor_path}")

    # LED diffuser: 15mm x 15mm x 5mm (transparent, fits on top)
    led_cover = create_box(15, 15, 5, wall_thickness=1.0)
    led_path = os.path.join(output_dir, "plant-agent-led-diffuser.stl")
    led_cover.save(led_path)
    print(f"Generated: {led_path}")

    return {
        "body": body_path,
        "sensor_mount": sensor_path,
        "led_diffuser": led_path,
        "colour": colour,
        "dimensions": {"width": 80, "height": 40, "depth": 60},
    }


def generate_desk_agent_enclosure(colour="black", output_dir="enclosures"):
    """Generate enclosure for Desk Agent."""
    os.makedirs(output_dir, exist_ok=True)

    # Main body: 100mm x 70mm x 35mm (wider for display + encoder)
    body = create_box(100, 70, 35, wall_thickness=2.0)
    body_path = os.path.join(output_dir, "desk-agent-body.stl")
    body.save(body_path)
    print(f"Generated: {body_path}")

    # Display bezel: 30mm x 20mm x 3mm
    bezel = create_box(30, 20, 3, wall_thickness=1.0)
    bezel_path = os.path.join(output_dir, "desk-agent-display-bezel.stl")
    bezel.save(bezel_path)
    print(f"Generated: {bezel_path}")

    return {
        "body": body_path,
        "display_bezel": bezel_path,
        "colour": colour,
        "dimensions": {"width": 100, "height": 35, "depth": 70},
    }


PRODUCTS = {
    "plant-agent": generate_plant_agent_enclosure,
    "desk-agent": generate_desk_agent_enclosure,
}


def main():
    parser = argparse.ArgumentParser(description="Generate enclosure STL files")
    parser.add_argument("--product", choices=PRODUCTS.keys(), required=True)
    parser.add_argument("--colour", default="black", help="Enclosure colour")
    parser.add_argument("--output", default="enclosures", help="Output directory")
    args = parser.parse_args()

    result = PRODUCTS[args.product](colour=args.colour, output_dir=args.output)
    print(f"\nGenerated {len(result)-2} STL files for {args.product}")
    for key, path in result.items():
        if key not in ("colour", "dimensions"):
            print(f"  {key}: {path}")


if __name__ == "__main__":
    main()
