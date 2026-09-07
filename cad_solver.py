#!/usr/bin/env python3
"""
CadBridge CLI: 2D Spatial Layout & Planar Constraint Solver.

Author: Montasir Tajwar Jihan
Usage:
    python cad_solver.py --test
    python cad_solver.py input_rooms.json -o solved_spec.json
"""
import sys
import os
import json
import argparse
from cadbridge.solver.spatial_solver import SpatialLayoutSolver

def run_test():
    print("[*] Running built-in spatial solver test...")
    solver = SpatialLayoutSolver(grid_snap=100.0)

    test_requests = [
        {"id": "living", "name": "LIVING & DINING", "width": 6000, "height": 4200},
        {"id": "kitchen", "name": "KITCHEN", "width": 3000, "height": 2400, "rel_to": "living", "side": "E", "align": "bottom"},
        {"id": "master_bed", "name": "MASTER BEDROOM", "width": 4200, "height": 3600, "rel_to": "living", "side": "N", "align": "left"},
        {"id": "attached_bath", "name": "ATTACHED BATH", "width": 1800, "height": 2100, "rel_to": "master_bed", "side": "E", "align": "bottom"},
        {"id": "common_bed", "name": "BEDROOM 2", "width": 3000, "height": 3600, "rel_to": "kitchen", "side": "N", "align": "left"}
    ]

    solved = solver.solve_layout(test_requests)
    valid, issues = solver.validate_no_overlap(solved)

    print(f"[+] Placed {len(solved)} rooms:")
    for r in solved:
        print(f"    - {r['name']:<18}: rect={r['rect']}")

    if valid:
        print("[+] Spatial Constraint Check PASSED: Zero overlaps detected.")
    else:
        print(f"[!] Spatial Constraint Issues: {issues}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="CadBridge: Spatial Constraint & Layout Solver")
    parser.add_argument("input_file", nargs="?", help="Optional JSON file with room adjacency rules")
    parser.add_argument("-o", "--output", help="Output JSON path")
    parser.add_argument("--test", action="store_true", help="Run built-in spatial placement test")

    args = parser.parse_args()

    if args.test or not args.input_file:
        run_test()
        return

    inp_path = os.path.abspath(args.input_file)
    with open(inp_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    solver = SpatialLayoutSolver(grid_snap=100.0)
    solved_rooms = solver.solve_layout(data.get("rooms", data))
    valid, issues = solver.validate_no_overlap(solved_rooms)

    if not valid:
        print(f"[!] Warning: Layout has overlap issues: {issues}", file=sys.stderr)

    if args.output:
        out_path = os.path.abspath(args.output)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump({"rooms": solved_rooms}, f, indent=2)
        print(f"[+] Solved rooms written to: {out_path}")
    else:
        print(json.dumps({"rooms": solved_rooms}, indent=2))

if __name__ == "__main__":
    main()
