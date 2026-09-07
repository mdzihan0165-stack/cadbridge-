#!/usr/bin/env python3
"""
CadBridge CLI: JSON Specification to AutoCAD DXF Compiler.

Author: Montasir Tajwar Jihan
Usage:
    python json2dxf.py projects/modern_2bhk_apartment/cad_spec.json -o build/floorplan.dxf --snapshot
"""
import sys
import os
import argparse
from cadbridge.core.spec import CADSpec
from cadbridge.compiler.json2dxf import compile_spec_to_dxf
from cadbridge.qa.cad_snapshot import render_dxf_snapshot

def main():
    parser = argparse.ArgumentParser(description="CadBridge: JSON to AutoCAD DXF Compiler")
    parser.add_argument("spec_file", help="Path to input cad_spec.json")
    parser.add_argument("-o", "--output", help="Path to output .dxf file (default: build/floorplan.dxf)")
    parser.add_argument("--snapshot", action="store_true", help="Automatically generate preview PNG snapshot")
    parser.add_argument("--theme", choices=["dark", "light"], default="dark", help="Snapshot theme (dark or light)")
    parser.add_argument("--dpi", type=int, default=200, help="Snapshot resolution DPI")

    args = parser.parse_args()

    spec_path = os.path.abspath(args.spec_file)
    if not os.path.exists(spec_path):
        print(f"Error: Specification file not found: {spec_path}", file=sys.stderr)
        sys.exit(1)

    output_dxf = args.output
    if not output_dxf:
        base_dir = os.path.dirname(spec_path)
        output_dxf = os.path.join(base_dir, "build", "floorplan.dxf")

    output_dxf = os.path.abspath(output_dxf)

    print(f"[*] Loading CAD specification from: {spec_path}")
    spec = CADSpec.load_json(spec_path)
    print(f"    - Project: {spec.project.name} ({spec.project.drawing_number})")
    print(f"    - Rooms: {len(spec.rooms)}, Doors: {len(spec.doors)}, Windows: {len(spec.windows)}, Columns: {len(spec.columns)}")

    print(f"[*] Compiling geometry to DXF...")
    dxf_result = compile_spec_to_dxf(spec, output_dxf)
    print(f"[+] Successfully compiled DXF: {dxf_result}")

    if args.snapshot:
        png_path = os.path.splitext(output_dxf)[0] + ".png"
        print(f"[*] Rendering visual QA snapshot ({args.theme} theme)...")
        render_dxf_snapshot(dxf_result, png_path, theme=args.theme, dpi=args.dpi)
        print(f"[+] Visual snapshot generated: {png_path}")

if __name__ == "__main__":
    main()
