#!/usr/bin/env python3
"""
CadBridge CLI: Quantity Surveying (BOQ) & Architectural Schedules Generator.

Author: Montasir Tajwar Jihan
Usage:
    python cad_boq.py projects/modern_2bhk_apartment/cad_spec.json -o build/boq.md --csv build/rooms.csv
"""
import sys
import os
import argparse
from cadbridge.core.spec import CADSpec
from cadbridge.boq.cad_boq import generate_boq_report

def main():
    parser = argparse.ArgumentParser(description="CadBridge: Bill of Quantities & Schedule Generator")
    parser.add_argument("spec_file", help="Path to input cad_spec.json")
    parser.add_argument("-o", "--output", help="Path to output Markdown report (e.g. build/boq.md)")
    parser.add_argument("--csv", help="Optional path to output CSV room schedule")

    args = parser.parse_args()

    spec_path = os.path.abspath(args.spec_file)
    if not os.path.exists(spec_path):
        print(f"Error: Spec file not found: {spec_path}", file=sys.stderr)
        sys.exit(1)

    out_md = args.output
    if not out_md:
        base_dir = os.path.dirname(spec_path)
        out_md = os.path.join(base_dir, "build", "boq_schedule.md")

    out_md = os.path.abspath(out_md)
    out_csv = os.path.abspath(args.csv) if args.csv else None

    print(f"[*] Generating BOQ and Schedules for: {spec_path}")
    spec = CADSpec.load_json(spec_path)
    report_content = generate_boq_report(spec, output_md_path=out_md, output_csv_path=out_csv)

    print(f"[+] Markdown BOQ Report written to: {out_md}")
    if out_csv:
        print(f"[+] CSV Room Schedule written to: {out_csv}")

    print("\n--- Summary Highlights ---")
    for line in report_content.splitlines():
        if line.startswith("| **Total Carpet Area**") or line.startswith("| **Gross Built-Up Area") or line.startswith("| **Carpet Efficiency"):
            print("  " + line.replace("|", " ").strip())

if __name__ == "__main__":
    main()
