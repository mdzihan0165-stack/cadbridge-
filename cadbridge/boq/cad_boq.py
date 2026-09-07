"""
Quantity Surveying (QS) and Material Takeoff Engine.

Computes net usable carpet areas, gross built-up area (BUA), circulation efficiency ratios,
and schedules for doors, windows, and structural columns in Markdown and CSV formats.

Author: Montasir Tajwar Jihan
"""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import os
import csv
from ..core.spec import CADSpec

@dataclass
class BOQSummary:
    carpet_area_sqm: float
    carpet_area_sqft: float
    built_up_area_sqm: float
    built_up_area_sqft: float
    efficiency_ratio_pct: float
    total_doors: int
    total_windows: int
    total_columns: int

def generate_boq_report(spec: CADSpec, output_md_path: Optional[str] = None, output_csv_path: Optional[str] = None) -> str:
    """Generates a detailed architectural schedule and BOQ markdown report."""
    room_rows = []
    total_carpet_sqm = 0.0

    for room in spec.rooms:
        sqm = room.area_sqm
        sqft = sqm * 10.7639
        total_carpet_sqm += sqm

        dims_str = ""
        perimeter_m = 0.0
        if room.rect:
            _, _, w, h = room.rect
            dims_str = f"{w/1000.0:.2f}m x {h/1000.0:.2f}m"
            perimeter_m = 2 * (w + h) / 1000.0

        room_rows.append({
            "id": room.id,
            "name": room.name,
            "category": room.category.title(),
            "dimensions": dims_str,
            "sqm": sqm,
            "sqft": sqft,
            "perimeter_m": perimeter_m,
            "finish": room.finish
        })

    # Envelope Built-Up Area (BUA)
    min_x, min_y, max_x, max_y = spec.get_overall_bounding_box()
    ext_t = spec.settings.wall_exterior_thickness
    # Envelope includes exterior wall thickness
    bua_w = (max_x - min_x) + (2 * ext_t)
    bua_h = (max_y - min_y) + (2 * ext_t)
    bua_sqm = (bua_w * bua_h) / 1_000_000.0
    bua_sqft = bua_sqm * 10.7639

    total_carpet_sqft = total_carpet_sqm * 10.7639
    efficiency = (total_carpet_sqm / bua_sqm * 100.0) if bua_sqm > 0 else 0.0

    # Door schedule aggregation
    door_groups: Dict[str, Dict[str, Any]] = {}
    for d in spec.doors:
        key = f"{d.width:.0f}x{d.height:.0f}_{d.type}"
        if key not in door_groups:
            door_groups[key] = {
                "width": d.width,
                "height": d.height,
                "type": d.type.title(),
                "label": d.label or d.id,
                "count": 0
            }
        door_groups[key]["count"] += 1

    # Window schedule aggregation
    win_groups: Dict[str, Dict[str, Any]] = {}
    for w in spec.windows:
        key = f"{w.width:.0f}x{w.height:.0f}_{w.sill_height:.0f}"
        if key not in win_groups:
            win_groups[key] = {
                "width": w.width,
                "height": w.height,
                "sill": w.sill_height,
                "label": w.label or w.id,
                "count": 0
            }
        win_groups[key]["count"] += 1

    # Build Markdown
    lines = []
    lines.append(f"# Bill of Quantities & Architectural Schedules: {spec.project.name}")
    lines.append(f"**Project ID:** `{spec.project.project_id}` | **Date:** {spec.project.date} | **Scale:** {spec.project.scale}")
    lines.append("")
    lines.append("## 1. Area Summary (Carpet Area vs Built-Up Area)")
    lines.append("")
    lines.append("| Metric | Metric (SQ.M.) | Imperial (SQ.FT.) | Notes |")
    lines.append("|---|---|---|---|")
    lines.append(f"| **Total Carpet Area** | **{total_carpet_sqm:.2f} m²** | **{total_carpet_sqft:.1f} ft²** | Usable internal room area |")
    lines.append(f"| **Gross Built-Up Area (BUA)** | **{bua_sqm:.2f} m²** | **{bua_sqft:.1f} ft²** | Outer envelope including walls |")
    lines.append(f"| **Wall & Circulation Area** | {bua_sqm - total_carpet_sqm:.2f} m² | {bua_sqft - total_carpet_sqft:.1f} ft² | Wall thicknesses & partitions |")
    lines.append(f"| **Carpet Efficiency Ratio** | **{efficiency:.1f}%** | - | Standard residential target: 70-80% |")
    lines.append("")

    lines.append("## 2. Room-by-Room Schedule")
    lines.append("")
    lines.append("| # | Room Name | Category | Dimensions | Carpet Area (m²) | Area (ft²) | Floor Finish |")
    lines.append("|---|---|---|---|---|---|---|")
    for idx, r in enumerate(room_rows, 1):
        lines.append(f"| {idx} | **{r['name']}** | {r['category']} | {r['dimensions']} | {r['sqm']:.2f} | {r['sqft']:.1f} | {r['finish']} |")
    lines.append("")

    lines.append("## 3. Door Schedule")
    lines.append("")
    lines.append("| Tag / Type | Width (mm) | Height (mm) | Type | Quantity |")
    lines.append("|---|---|---|---|---|")
    for key, d in door_groups.items():
        lines.append(f"| `{d['label']}` | {d['width']:.0f} | {d['height']:.0f} | {d['type']} | {d['count']} |")
    lines.append("")

    lines.append("## 4. Window & Ventilator Schedule")
    lines.append("")
    lines.append("| Tag / Type | Width (mm) | Height (mm) | Sill Height (mm) | Quantity |")
    lines.append("|---|---|---|---|---|")
    for key, w in win_groups.items():
        lines.append(f"| `{w['label']}` | {w['width']:.0f} | {w['height']:.0f} | {w['sill']:.0f} | {w['count']} |")
    lines.append("")

    if spec.columns:
        lines.append("## 5. Structural Column Schedule")
        lines.append("")
        lines.append(f"Total Structural Columns: **{len(spec.columns)} units**")
        lines.append("")
        col_sizes = {}
        for col in spec.columns:
            s_key = f"{col.size[0]:.0f}x{col.size[1]:.0f} mm"
            col_sizes[s_key] = col_sizes.get(s_key, 0) + 1
        lines.append("| Column Type / Size | Count |")
        lines.append("|---|---|")
        for s_key, c_cnt in col_sizes.items():
            lines.append(f"| RCC Column ({s_key}) | {c_cnt} |")
        lines.append("")

    md_content = "\n".join(lines)

    if output_md_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_md_path)), exist_ok=True)
        with open(output_md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

    if output_csv_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_csv_path)), exist_ok=True)
        with open(output_csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Room Name", "Category", "Dimensions", "Area SQ.M", "Area SQ.FT", "Floor Finish"])
            for r in room_rows:
                writer.writerow([r["name"], r["category"], r["dimensions"], f"{r['sqm']:.2f}", f"{r['sqft']:.1f}", r["finish"]])

    return md_content
