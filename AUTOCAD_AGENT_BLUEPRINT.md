# CadBridge: System Architecture & Technical Blueprint

**Author & System Architect:** Montasir Tajwar Jihan  
**Project:** CadBridge — Algorithmic CAD Synthesis Engine  
**Standard:** AIA CAD Layer Guidelines (NCS v6) | AutoCAD AC1032 DXF Universal Standard

---

## 1. Architectural Vision

CadBridge is an engineering framework designed to bridge the gap between high-level declarative spatial intent and production-grade CAD drafting. Traditional computer-aided drafting requires manual execution of line drawing, wall offsetting, door swing trimming, block placement, and manual quantity takeoff. 

CadBridge replaces this manual pipeline with an algorithmic compiler:
1. Translates high-level declarative room layouts into standardized schemas (`cad_spec.json`).
2. Solves 2D planar adjacency constraints and structural grid alignments without spatial overlap.
3. Compiles vector geometry into native AutoCAD R2018 DXF files with strict AIA/ISO layer separation.
4. Generates automated Bills of Quantities (BOQ), room schedules, and built-up area (BUA) calculations.
5. Renders headless 200+ DPI vector plot snapshots for immediate verification.

---

## 2. Core Compiler Pipeline

```
[Declarative Spatial Specification] (`cad_spec.json`)
                 │
                 ▼
[Stage 1: Spatial Layout & Constraint Solver] (`cadbridge.solver`)
Resolves room dimensions, cardinal adjacencies, setbacks, and circulation clearances.
                 │
                 ▼
[Stage 2: Headless DXF Geometry Synthesis Engine] (`cadbridge.compiler`)
Generates vector wall polylines, AIA layers, parametric blocks, and dimension lines.
                 │
                 ▼
[Stage 3: Headless Vector/Raster Inspection] (`cadbridge.qa`)
Synthesizes high-resolution inspection snapshots in model space and plot sheet themes.
                 │
                 ▼
[Stage 4: Quantity Surveying & BOQ Takeoff] (`cadbridge.boq`)
Computes net carpet areas, gross BUA, and door/window schedules in Markdown and CSV.
```

---

## 3. Technology Stack & Design Decisions

1. **Headless CAD Engine: `ezdxf` (Python 3.10+)**
   - Headless vector compilation without requiring an AutoCAD GUI or cloud runtime.
   - Sub-100ms compilation speed for complex residential and commercial layouts.
2. **CAD Interoperability: AutoCAD R2018 (AC1032)**
   - Target format compatible across all modern CAD software: AutoCAD 2018–2026, Revit, Civil 3D, LibreCAD, and DWG TrueView.
3. **Drafting Layer Standard: AIA CAD Layer Guidelines**
   - Strict layer segregation (`A-WALL-EXTR`, `A-WALL-INTR`, `A-DOOR`, `A-GLAZ`, `A-COLS`, `A-ANNO-DIMS`, `A-ANNO-TEXT`, `A-TITL`) with standard AutoCAD Color Index (ACI) codes and ISO lineweights.
4. **Automated Takeoff (BOQ):**
   - Precise area calculations via Gauss's shoelace formula, circulation ratios, and opening schedules.

---

## 4. Benchmark Architectural Designs

1. **Compact 1-BHK Studio Apartment (~650 sq.ft)**
   - Located at: `projects/compact_1bhk_studio/`
   - Living/Dining, Modular Kitchenette, Master Studio, Bath, Balcony, and Study Nook.
2. **Modern 2-BHK Urban Apartment (~850 sq.ft)**
   - Located at: `projects/modern_2bhk_apartment/`
   - Living/Dining, Kitchen, Master Bed (Attached Bath), Bedroom 2, Common Bath, and Balconies.

---

## 5. Engineering Inquiries & Contributions

Developed and maintained by **Montasir Tajwar Jihan**.  
Open for academic and engineering collaboration under the MIT License.
