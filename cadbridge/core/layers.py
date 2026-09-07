"""
AIA CAD Layer Guidelines and ISO 13567 Architectural Layer Standards.

Implements color index, lineweight conventions, and linetypes for
interoperable CAD workflows across AutoCAD, Revit, and Civil 3D.

Author: Montasir Tajwar Jihan
"""
from dataclasses import dataclass
from typing import Dict
import ezdxf

@dataclass
class LayerConfig:
    name: str
    color: int        # AutoCAD Color Index (ACI: 1=Red, 2=Yellow, 3=Green, 4=Cyan, 5=Blue, 6=Magenta, 7=White/Black, 8=Dark Gray)
    lineweight: int   # 100ths of mm (e.g. 35 = 0.35mm as per ISO 128)
    linetype: str     # "Continuous", "DASHED", "CENTER", etc.
    description: str

# Standard AIA CAD Layer Mapping (National CAD Standard v6.0 / ISO 13567)
STANDARD_LAYERS: Dict[str, LayerConfig] = {
    "A-WALL-EXTR": LayerConfig(
        name="A-WALL-EXTR",
        color=4,         # Cyan
        lineweight=35,   # 0.35mm heavy cut line
        linetype="Continuous",
        description="Exterior Building Envelope Walls"
    ),
    "A-WALL-INTR": LayerConfig(
        name="A-WALL-INTR",
        color=3,         # Green
        lineweight=25,   # 0.25mm medium partition line
        linetype="Continuous",
        description="Interior Partition Walls"
    ),
    "A-DOOR": LayerConfig(
        name="A-DOOR",
        color=2,         # Yellow
        lineweight=18,   # 0.18mm light swing arc and leaf
        linetype="Continuous",
        description="Doors, Frames, and Swing Arcs"
    ),
    "A-GLAZ": LayerConfig(
        name="A-GLAZ",
        color=5,         # Blue
        lineweight=18,   # 0.18mm window sill and glazing lines
        linetype="Continuous",
        description="Windows, Glazing, and Sills"
    ),
    "A-COLS": LayerConfig(
        name="A-COLS",
        color=1,         # Red
        lineweight=35,   # 0.35mm structural columns
        linetype="Continuous",
        description="Structural RCC Columns & Pillars"
    ),
    "A-FLOR-FIXT": LayerConfig(
        name="A-FLOR-FIXT",
        color=6,         # Magenta
        lineweight=13,   # 0.13mm fine furniture / sanitary line
        linetype="Continuous",
        description="Furniture, Sanitaryware & Kitchen Fixtures"
    ),
    "A-ANNO-TEXT": LayerConfig(
        name="A-ANNO-TEXT",
        color=7,         # White/Black text
        lineweight=18,   # 0.18mm annotations and titles
        linetype="Continuous",
        description="Room Names, Area Tags & Drawing Notes"
    ),
    "A-ANNO-DIMS": LayerConfig(
        name="A-ANNO-DIMS",
        color=1,         # Red
        lineweight=13,   # 0.13mm dimension lines & ticks
        linetype="Continuous",
        description="Linear Dimension Lines & Ticks"
    ),
    "A-AREA": LayerConfig(
        name="A-AREA",
        color=8,         # Dark Gray
        lineweight=13,   # 0.13mm calculation boundary
        linetype="Continuous",
        description="Internal Area Calculation Polylines"
    ),
    "A-GRID": LayerConfig(
        name="A-GRID",
        color=1,         # Red
        lineweight=13,   # 0.13mm centerline
        linetype="CENTER",
        description="Structural Grid & Centerlines"
    ),
    "A-TITL": LayerConfig(
        name="A-TITL",
        color=4,         # Cyan
        lineweight=50,   # 0.50mm border outline
        linetype="Continuous",
        description="Sheet Border & Title Block"
    ),
}

def setup_standard_layers(doc: ezdxf.document.Drawing) -> None:
    """Register standard AIA layers in the target DXF document."""
    # Ensure standard line definitions are present
    if "CENTER" not in doc.linetypes:
        doc.linetypes.add("CENTER", pattern=[1.25, 0.75, -0.25, 0.25, -0.25], description="Center ____ _ ____ _ ____")
    if "DASHED" not in doc.linetypes:
        doc.linetypes.add("DASHED", pattern=[0.5, 0.5, -0.5], description="Dashed __ __ __ __")

    for cfg in STANDARD_LAYERS.values():
        if cfg.name not in doc.layers:
            layer = doc.layers.add(
                name=cfg.name,
                color=cfg.color,
                linetype=cfg.linetype
            )
            layer.set_dxf_attrib("lineweight", cfg.lineweight)
            layer.description = cfg.description
