#!/usr/bin/env python3
"""
CadBridge CLI: Headless DXF Plot Preview & Snapshot Renderer.

Author: Montasir Tajwar Jihan
Usage:
    python cad_snapshot.py build/floorplan.dxf -o build/preview.png --theme dark --dpi 200
"""
import sys
import os
import argparse
from cadbridge.qa.cad_snapshot import render_dxf_snapshot

def main():
    parser = argparse.ArgumentParser(description="CadBridge: DXF Visual QA Snapshot Renderer")
    parser.add_argument("dxf_file", help="Path to input .dxf file")
    parser.add_argument("-o", "--output", help="Path to output image file (.png, .svg)")
    parser.add_argument("--theme", choices=["dark", "light"], default="dark", help="Color theme (dark or light)")
    parser.add_argument("--dpi", type=int, default=200, help="Image resolution DPI (for PNG)")

    args = parser.parse_args()

    dxf_path = os.path.abspath(args.dxf_file)
    if not os.path.exists(dxf_path):
        print(f"Error: DXF file not found: {dxf_path}", file=sys.stderr)
        sys.exit(1)

    out_img = args.output
    if not out_img:
        out_img = os.path.splitext(dxf_path)[0] + ("_preview.png" if args.theme == "dark" else "_preview_light.png")

    out_img = os.path.abspath(out_img)
    print(f"[*] Rendering DXF snapshot from: {dxf_path}")
    print(f"    - Theme: {args.theme}")
    print(f"    - DPI: {args.dpi}")

    result = render_dxf_snapshot(dxf_path, out_img, theme=args.theme, dpi=args.dpi)
    print(f"[+] Snapshot saved successfully to: {result}")

if __name__ == "__main__":
    main()
