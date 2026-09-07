"""
Parametric Architectural Block Generators.

Synthesizes standard reusable CAD blocks: flush single/double doors with
true 90-degree swing arcs, window openings with sill overhangs and glazing,
reinforced concrete columns, north symbols, and interior fixtures.

Author: Montasir Tajwar Jihan
"""
import math
import ezdxf

def setup_standard_blocks(doc: ezdxf.document.Drawing) -> None:
    """Instantiate standard reusable block definitions in the DXF drawing."""
    _create_door_block(doc, "DOOR_SINGLE_900", width=900)
    _create_door_block(doc, "DOOR_SINGLE_750", width=750)
    _create_door_block(doc, "DOOR_SINGLE_1000", width=1000)
    _create_double_door_block(doc, "DOOR_DOUBLE_1500", width=1500)
    _create_window_block(doc, "WINDOW_1500", width=1500, wall_thickness=250)
    _create_window_block(doc, "WINDOW_1200", width=1200, wall_thickness=250)
    _create_window_block(doc, "WINDOW_1800", width=1800, wall_thickness=250)
    _create_ventilator_block(doc, "VENTILATOR_600", width=600, wall_thickness=125)
    _create_column_block(doc, "COLUMN_300x300", width=300, depth=300)
    _create_north_arrow_block(doc, "NORTH_ARROW", radius=250)
    _create_furniture_blocks(doc)

def _create_door_block(doc: ezdxf.document.Drawing, name: str, width: float) -> None:
    """Standard 90-degree single flush door with timber frame jambs and swing arc."""
    if name in doc.blocks:
        return
    blk = doc.blocks.new(name=name)
    layer = "A-DOOR"
    jamb_w = 50.0
    jamb_d = 125.0
    leaf_t = 40.0

    # Door jambs (left and right frame)
    blk.add_lwpolyline([(0, 0), (jamb_w, 0), (jamb_w, jamb_d), (0, jamb_d), (0, 0)], close=True, dxfattribs={"layer": layer})
    blk.add_lwpolyline([(width - jamb_w, 0), (width, 0), (width, jamb_d), (width - jamb_w, jamb_d), (width - jamb_w, 0)], close=True, dxfattribs={"layer": layer})

    # Door leaf (open at 90 deg along left jamb)
    leaf_len = width - jamb_w
    blk.add_lwpolyline([
        (jamb_w, 0),
        (jamb_w, leaf_len),
        (jamb_w + leaf_t, leaf_len),
        (jamb_w + leaf_t, 0),
        (jamb_w, 0)
    ], close=True, dxfattribs={"layer": layer})

    # 90 degree swing arc
    blk.add_arc(
        center=(jamb_w, 0),
        radius=leaf_len,
        start_angle=0,
        end_angle=90,
        dxfattribs={"layer": layer, "linetype": "DASHED"}
    )

def _create_double_door_block(doc: ezdxf.document.Drawing, name: str, width: float) -> None:
    """Double swing main entrance door."""
    if name in doc.blocks:
        return
    blk = doc.blocks.new(name=name)
    layer = "A-DOOR"
    half_w = width / 2.0
    jamb_w = 50.0
    jamb_d = 150.0
    leaf_t = 40.0

    # Jambs
    blk.add_lwpolyline([(0, 0), (jamb_w, 0), (jamb_w, jamb_d), (0, jamb_d), (0, 0)], close=True, dxfattribs={"layer": layer})
    blk.add_lwpolyline([(width - jamb_w, 0), (width, 0), (width, jamb_d), (width - jamb_w, jamb_d), (width - jamb_w, 0)], close=True, dxfattribs={"layer": layer})

    # Left leaf and swing arc
    left_len = half_w - jamb_w
    blk.add_lwpolyline([
        (jamb_w, 0), (jamb_w, left_len), (jamb_w + leaf_t, left_len), (jamb_w + leaf_t, 0), (jamb_w, 0)
    ], close=True, dxfattribs={"layer": layer})
    blk.add_arc(center=(jamb_w, 0), radius=left_len, start_angle=0, end_angle=90, dxfattribs={"layer": layer, "linetype": "DASHED"})

    # Right leaf and swing arc
    right_len = half_w - jamb_w
    blk.add_lwpolyline([
        (width - jamb_w, 0), (width - jamb_w, right_len), (width - jamb_w - leaf_t, right_len), (width - jamb_w - leaf_t, 0), (width - jamb_w, 0)
    ], close=True, dxfattribs={"layer": layer})
    blk.add_arc(center=(width - jamb_w, 0), radius=right_len, start_angle=90, end_angle=180, dxfattribs={"layer": layer, "linetype": "DASHED"})

def _create_window_block(doc: ezdxf.document.Drawing, name: str, width: float, wall_thickness: float = 250) -> None:
    """Standard architectural window with sill, wall opening endcaps, and double glass lines."""
    if name in doc.blocks:
        return
    blk = doc.blocks.new(name=name)
    layer = "A-GLAZ"
    wt = wall_thickness
    frame_w = 50.0

    # Outer wall opening lines (end caps)
    blk.add_line((0, 0), (0, wt), dxfattribs={"layer": "A-WALL-EXTR"})
    blk.add_line((width, 0), (width, wt), dxfattribs={"layer": "A-WALL-EXTR"})

    # Sill line (exterior side)
    sill_overhang = 40.0
    blk.add_lwpolyline([(-sill_overhang, -20), (width + sill_overhang, -20), (width + sill_overhang, 0), (-sill_overhang, 0), (-sill_overhang, -20)], close=True, dxfattribs={"layer": layer})

    # Interior sill / wall line
    blk.add_line((0, wt), (width, wt), dxfattribs={"layer": layer})

    # Window frame (left, right)
    blk.add_lwpolyline([(0, 0), (frame_w, 0), (frame_w, wt), (0, wt), (0, 0)], close=True, dxfattribs={"layer": layer})
    blk.add_lwpolyline([(width - frame_w, 0), (width, 0), (width, wt), (width - frame_w, wt), (width - frame_w, 0)], close=True, dxfattribs={"layer": layer})

    # Center glazing pane lines
    mid_y = wt / 2.0
    blk.add_line((frame_w, mid_y - 15), (width - frame_w, mid_y - 15), dxfattribs={"layer": layer})
    blk.add_line((frame_w, mid_y + 15), (width - frame_w, mid_y + 15), dxfattribs={"layer": layer})

def _create_ventilator_block(doc: ezdxf.document.Drawing, name: str, width: float, wall_thickness: float = 125) -> None:
    """Toilet/Bathroom ventilator block with louvres."""
    if name in doc.blocks:
        return
    blk = doc.blocks.new(name=name)
    layer = "A-GLAZ"
    blk.add_lwpolyline([(0, 0), (width, 0), (width, wall_thickness), (0, wall_thickness), (0, 0)], close=True, dxfattribs={"layer": layer})
    blk.add_line((0, 0), (width, wall_thickness), dxfattribs={"layer": layer})
    blk.add_line((0, wall_thickness), (width, 0), dxfattribs={"layer": layer})

def _create_column_block(doc: ezdxf.document.Drawing, name: str, width: float = 300, depth: float = 300) -> None:
    """Reinforced concrete (RCC) column with cross markers."""
    if name in doc.blocks:
        return
    blk = doc.blocks.new(name=name)
    layer = "A-COLS"
    hw, hd = width / 2.0, depth / 2.0
    points = [(-hw, -hd), (hw, -hd), (hw, hd), (-hw, hd), (-hw, -hd)]
    blk.add_lwpolyline(points, close=True, dxfattribs={"layer": layer})

    # Diagonal ties representation
    blk.add_line((-hw, -hd), (hw, hd), dxfattribs={"layer": layer})
    blk.add_line((-hw, hd), (hw, -hd), dxfattribs={"layer": layer})

def _create_north_arrow_block(doc: ezdxf.document.Drawing, name: str, radius: float = 250) -> None:
    """Standard architectural true-north pointer."""
    if name in doc.blocks:
        return
    blk = doc.blocks.new(name=name)
    layer = "A-ANNO-TEXT"
    blk.add_circle((0, 0), radius=radius, dxfattribs={"layer": layer})

    tip = (0, radius * 1.5)
    left = (-radius * 0.4, -radius * 0.5)
    right = (radius * 0.4, -radius * 0.5)
    center = (0, 0)

    blk.add_lwpolyline([tip, left, center, tip], close=True, dxfattribs={"layer": layer})
    blk.add_lwpolyline([tip, right, center, tip], close=True, dxfattribs={"layer": layer})

    blk.add_text("N", dxfattribs={
        "layer": layer,
        "height": radius * 0.8,
        "style": "OpenSans" if "OpenSans" in doc.styles else "Standard"
    }).set_placement((0, radius * 1.8), align=ezdxf.enums.TextEntityAlignment.CENTER)

def _create_furniture_blocks(doc: ezdxf.document.Drawing) -> None:
    """Standard 2D architectural furniture symbols."""
    layer = "A-FLOR-FIXT"

    # Queen Bed (1500 x 2000 mm)
    if "BED_QUEEN" not in doc.blocks:
        blk = doc.blocks.new(name="BED_QUEEN")
        blk.add_lwpolyline([(0, 0), (1500, 0), (1500, 2000), (0, 2000), (0, 0)], close=True, dxfattribs={"layer": layer})
        blk.add_lwpolyline([(0, 1900), (1500, 1900), (1500, 2000), (0, 2000), (0, 1900)], close=True, dxfattribs={"layer": layer})
        blk.add_lwpolyline([(100, 1450), (650, 1450), (650, 1850), (100, 1850), (100, 1450)], close=True, dxfattribs={"layer": layer})
        blk.add_lwpolyline([(850, 1450), (1400, 1450), (1400, 1850), (850, 1850), (850, 1450)], close=True, dxfattribs={"layer": layer})
        blk.add_line((0, 800), (1500, 800), dxfattribs={"layer": layer})

    # Single Bed (900 x 1900 mm)
    if "BED_SINGLE" not in doc.blocks:
        blk = doc.blocks.new(name="BED_SINGLE")
        blk.add_lwpolyline([(0, 0), (900, 0), (900, 1900), (0, 1900), (0, 0)], close=True, dxfattribs={"layer": layer})
        blk.add_lwpolyline([(150, 1400), (750, 1400), (750, 1800), (150, 1800), (150, 1400)], close=True, dxfattribs={"layer": layer})

    # Water Closet (450 x 650 mm)
    if "TOILET_WC" not in doc.blocks:
        blk = doc.blocks.new(name="TOILET_WC")
        blk.add_lwpolyline([(0, 500), (450, 500), (450, 650), (0, 650), (0, 500)], close=True, dxfattribs={"layer": layer})
        blk.add_arc(center=(225, 270), radius=180, start_angle=180, end_angle=360, dxfattribs={"layer": layer})
        blk.add_line((45, 270), (45, 500), dxfattribs={"layer": layer})
        blk.add_line((405, 270), (405, 500), dxfattribs={"layer": layer})

    # Wash Basin (550 x 420 mm)
    if "WASH_BASIN" not in doc.blocks:
        blk = doc.blocks.new(name="WASH_BASIN")
        blk.add_lwpolyline([(0, 0), (550, 0), (550, 420), (0, 420), (0, 0)], close=True, dxfattribs={"layer": layer})
        blk.add_circle((275, 210), radius=150, dxfattribs={"layer": layer})
        blk.add_circle((275, 340), radius=25, dxfattribs={"layer": layer})

    # 3-Seater Living Sofa (2100 x 850 mm)
    if "SOFA_3SEATER" not in doc.blocks:
        blk = doc.blocks.new(name="SOFA_3SEATER")
        blk.add_lwpolyline([(0, 0), (2100, 0), (2100, 850), (0, 850), (0, 0)], close=True, dxfattribs={"layer": layer})
        blk.add_line((0, 650), (2100, 650), dxfattribs={"layer": layer})
        blk.add_lwpolyline([(0, 0), (180, 0), (180, 650), (0, 650), (0, 0)], close=True, dxfattribs={"layer": layer})
        blk.add_lwpolyline([(1920, 0), (2100, 0), (2100, 650), (1920, 650), (1920, 0)], close=True, dxfattribs={"layer": layer})
        blk.add_line((760, 0), (760, 650), dxfattribs={"layer": layer})
        blk.add_line((1340, 0), (1340, 650), dxfattribs={"layer": layer})
