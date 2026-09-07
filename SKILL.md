---
name: CadBridge Developer & Engineering Handbook
description: Procedural reference for CadBridge — headless AutoCAD R2018 DXF synthesis, AIA standard layering, visual QA snapshots (PNG/SVG), spatial constraint solving, and Bill of Quantities (BOQ). Authored by Montasir Tajwar Jihan.
---

# CadBridge Engineering Handbook & Procedural Reference

**Author:** Montasir Tajwar Jihan  
**Framework:** CadBridge Computational 2D CAD Compiler  
**Standard:** AIA CAD Layer Guidelines (NCS v6) | ISO 13567

---

## 1. Execution Architecture & Tool Mappings

CadBridge provides 4 Canonical CLI tools for automated architectural drafting:

| Pipeline Stage | Canonical CLI Command | Execution Time | Primary Output |
|---|---|---|---|
| **1. Layout Solving** | `python cad_solver.py <rules.json> -o <cad_spec.json>` | < 0.2s | Snapped, non-overlapping room bounding boxes |
| **2. DXF Compilation** | `python json2dxf.py <cad_spec.json> -o build/floorplan.dxf --snapshot` | < 0.5s | Production AutoCAD R2018 `.dxf` + Preview `.png` |
| **3. Visual Inspection** | `python cad_snapshot.py build/floorplan.dxf -o build/preview.png --theme dark` | < 1.0s | High-resolution raster (PNG) or vector (SVG) |
| **4. Quantity Surveying** | `python cad_boq.py <cad_spec.json> -o build/boq.md --csv build/rooms.csv` | < 0.2s | Markdown schedules, Carpet/BUA ratios, and CSV |

---

## 2. Standard Layer Guidelines (AIA / ISO 13567)

All compiled drawings strictly enforce standard architectural layers with AutoCAD Color Index (ACI) codes and ISO lineweights:

| Layer Name | Color (ACI) | Lineweight (mm) | Linetype | Description |
|---|---|---|---|---|
| `A-WALL-EXTR` | 4 (Cyan) | 0.35 | Continuous | Exterior building perimeter walls |
| `A-WALL-INTR` | 3 (Green) | 0.25 | Continuous | Interior partition walls |
| `A-DOOR` | 2 (Yellow) | 0.18 | Continuous | Door frames, leaves, and 90° swing arcs |
| `A-GLAZ` | 5 (Blue) | 0.18 | Continuous | Window frames, sills, and glazing |
| `A-COLS` | 1 (Red) | 0.35 | Continuous | Structural RCC columns with diagonal markers |
| `A-FLOR-FIXT` | 6 (Magenta) | 0.13 | Continuous | Furniture, beds, sofas, sanitaryware |
| `A-ANNO-TEXT` | 7 (White/Black) | 0.18 | Continuous | Room names, area calculations, notes |
| `A-ANNO-DIMS` | 1 (Red) | 0.13 | Continuous | Exterior and interior dimension lines and ticks |
| `A-AREA` | 8 (Dark Gray) | 0.13 | Continuous | Room floor carpet boundary polylines |
| `A-TITL` | 4 (Cyan) | 0.50 | Continuous | Outer sheet border and metadata title block |

---

## 3. Parametric Standard Blocks

CadBridge generates standard parametric blocks in DXF:
- `DOOR_SINGLE_900`: 900x2100mm single leaf flush door with frame jambs and 90° dashed swing arc.
- `DOOR_SINGLE_750`: 750x2100mm bathroom/utility door.
- `DOOR_SINGLE_1000`: 1000x2100mm main entrance door.
- `DOOR_DOUBLE_1500`: 1500x2100mm double swing door.
- `WINDOW_1500`, `WINDOW_1200`, `WINDOW_1800`: Standard windows with wall opening endcaps, exterior sill overhang, and double glass lines.
- `VENTILATOR_600`: 600x600mm bathroom ventilator with louvres.
- `COLUMN_300x300`: 300x300mm structural column with cross reinforcement markers.
- `NORTH_ARROW`: Architectural circle with oriented north pointer and 'N' text.
- Furniture: `BED_QUEEN`, `BED_SINGLE`, `SOFA_3SEATER`, `TOILET_WC`, `WASH_BASIN`.

---

## 4. Architectural Quality Assurance Protocol

1. **Wall Integrity:** Verify exterior double walls enclose the building footprint and interior partitions align with room boundaries.
2. **Openings Check:** Check that windows and doors do not collide or overlap with columns or intersecting walls.
3. **Circulation Clearance:** Ensure every room has an accessible door opening and clear circulation path.
4. **Legibility:** Verify text tags and area numbers do not obscure furniture or dimension lines.
5. **Title Block & Metadata:** Confirm project metadata, scale, and designer name (**Montasir Tajwar Jihan**) are correctly displayed in the title block.
