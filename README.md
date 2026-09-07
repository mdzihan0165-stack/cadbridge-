# CadBridge: Computational 2D CAD Compiler & Algorithmic Drafting Engine

**Developer:** Montasir Tajwar Jihan  
**License:** MIT  
**Platform:** Python 3.10+ | AutoCAD R2018+ (AC1032 DXF Universal Standard)

CadBridge is a high-performance Python framework for programmatic 2D architectural drafting, spatial constraint solving, and quantity surveying. It compiles declarative JSON spatial definitions into production-grade AutoCAD `.dxf` drawings conforming to AIA CAD Layer Guidelines and ISO 13567 standards, complete with parametric blocks, true-tangent swing arcs, and automated quantity takeoffs.

---

## Technical Features

- **Headless DXF Synthesis:** Generates standard AutoCAD R2018 (AC1032) drawing exchange files without requiring an AutoCAD GUI or Autodesk runtime.
- **AIA / ISO 13567 Layer Compliance:** Strict separation of structural envelope (`A-WALL-EXTR`), interior partitions (`A-WALL-INTR`), openings (`A-DOOR`, `A-GLAZ`), columns (`A-COLS`), annotations (`A-ANNO-TEXT`, `A-ANNO-DIMS`), and title block metadata (`A-TITL`).
- **Parametric Architectural Blocks:** Dynamic generation of single/double flush doors with dashed 90° swing arcs, window openings with exterior sills and double glass lines, reinforced concrete columns, and architectural north symbols.
- **Topological Planar Solver:** Algorithmic 2D constraint solver for placing rooms based on cardinal adjacency (`rel_to`, `side`, `align`) with structural grid snapping and zero-overlap validation.
- **Automated Quantity Surveying (BOQ):** Computes net usable carpet areas, gross built-up area (BUA), circulation efficiency ratios, and exports complete door/window/column schedules in Markdown and CSV formats.
- **Vector & Raster Inspection:** Renders headless 200+ DPI vector snapshots (`PNG` / `SVG`) in dark modelspace and light paper plot styles using `matplotlib` and `ezdxf.addons.drawing`.

---

## Installation

```bash
git clone https://github.com/montasir-jihan/cadbridge.git
cd cadbridge
pip install -r requirements.txt
```

Or install in editable development mode:
```bash
pip install -e .
```

---

## Command Line Interface (CLI)

### 1. Compile Declarative Spec to AutoCAD DXF
```bash
python json2dxf.py projects/compact_1bhk_studio/cad_spec.json -o build/floorplan.dxf --snapshot --theme dark
```

### 2. Headless Plot Preview / Snapshot Renderer
```bash
# AutoCAD Model Space (Dark Theme)
python cad_snapshot.py build/floorplan.dxf -o build/preview_dark.png --theme dark

# White Paper Plot (Light Theme)
python cad_snapshot.py build/floorplan.dxf -o build/preview_light.png --theme light
```

### 3. Quantity Surveying & Schedules (BOQ)
```bash
python cad_boq.py projects/compact_1bhk_studio/cad_spec.json -o build/boq.md --csv build/rooms.csv
```

### 4. 2D Spatial Layout Constraint Solver
```bash
python cad_solver.py --test
```

---

## Project Structure

```
cadbridge/
├── cadbridge/                 # Core engine package
│   ├── core/                  # Data models, AIA layer definitions, parametric blocks
│   │   ├── layers.py          # AIA / ISO 13567 layer configurations
│   │   ├── blocks.py          # Reusable CAD blocks (doors, windows, columns)
│   │   └── spec.py            # Pydantic/dataclass schema parser & validator
│   ├── compiler/              # DXF geometry synthesis engine
│   │   └── json2dxf.py        # Vector wall offsetting & entity generation
│   ├── solver/                # 2D planar constraint & topological solver
│   │   └── spatial_solver.py  # Adjacency solver & collision verification
│   ├── qa/                    # Headless inspection & rasterization
│   │   └── cad_snapshot.py    # Matplotlib backend renderer (PNG/SVG)
│   └── boq/                   # Quantity takeoff engine
│       └── cad_boq.py         # Area schedules & opening takeoff (MD/CSV)
├── tests/                     # Unit test suite
│   └── test_compiler.py       # Compiler and solver unit tests
├── projects/                  # Architectural benchmark designs
│   ├── compact_1bhk_studio/   # 650 sq.ft studio apartment
│   └── modern_2bhk_apartment/ # 850 sq.ft 2-BHK apartment
├── json2dxf.py                # Standalone compiler CLI
├── cad_snapshot.py            # Standalone renderer CLI
├── cad_solver.py              # Standalone layout solver CLI
├── cad_boq.py                 # Standalone BOQ generator CLI
├── spec_template.json         # Reference schema template
├── setup.py                   # Python package installer
├── requirements.txt           # Core dependencies
└── README.md                  # Technical documentation
```

---

## Running Automated Tests

```bash
python -m unittest discover tests/
```

---

## Author & Maintainer

**Montasir Tajwar Jihan**  
*Lead Computational CAD & Automation Engineer*  
GitHub: [https://github.com/montasir-jihan](https://github.com/montasir-jihan)  
Email: montasir.jihan@engineering.local
