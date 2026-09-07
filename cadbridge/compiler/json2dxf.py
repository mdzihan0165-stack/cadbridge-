"""
CadBridge DXF Synthesis Engine.

Compiles declarative CAD specifications into production-grade AutoCAD R2018 DXF files.
Implements vector wall double-line offsets, clean non-colliding architectural tag bubbles,
linear exterior chain dimensioning, and standard sheet title blocks.

Author: Montasir Tajwar Jihan
"""
import os
import math
from typing import Optional, List, Tuple
import ezdxf
from ezdxf.enums import TextEntityAlignment

from ..core.layers import setup_standard_layers
from ..core.blocks import setup_standard_blocks
from ..core.spec import CADSpec, Room, Door, Window, Column, Fixture

def compile_spec_to_dxf(spec: CADSpec, output_path: str) -> str:
    """Compiles a CADSpec into a clean, high-quality, professional DXF drawing."""
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    # 1. Create R2018 drawing with millimeters units
    doc = ezdxf.new("R2018", setup=True)
    doc.header["$INSUNITS"] = 4    # 4 = Millimeters
    doc.header["$LUNITS"] = 2      # Decimal
    doc.header["$MEASUREMENT"] = 1 # Metric

    # 2. Setup standard layers & blocks
    setup_standard_layers(doc)
    setup_standard_blocks(doc)

    msp = doc.modelspace()

    # 3. Draw Room Envelopes & Wall Structure
    _draw_rooms_and_walls(msp, spec)

    # 4. Insert Columns
    _draw_columns(msp, spec)

    # 5. Insert Doors & Door Tags
    _draw_doors(msp, spec)

    # 6. Insert Windows & Window Tags
    _draw_windows(msp, spec)

    # 7. Insert Fixtures
    _draw_fixtures(msp, spec)

    # 8. Room Annotations (Labels & Carpet Areas)
    _draw_room_labels(msp, spec)

    # 9. Dimensions
    if spec.settings.auto_exterior_dimensions:
        _draw_exterior_dimensions(msp, spec)

    # 10. Sheet Border, Title Block & North Arrow
    if spec.settings.include_title_block:
        _draw_title_block_and_border(msp, spec)

    # Save drawing
    doc.saveas(output_path)
    return output_path

def _draw_rooms_and_walls(msp, spec: CADSpec) -> None:
    """
    Renders clean architectural walls without duplicate overlapping lines.
    """
    ext_t = spec.settings.wall_exterior_thickness
    int_t = spec.settings.wall_interior_thickness

    # Collect all unique wall edges
    edges_count = {}
    for room in spec.rooms:
        if room.is_open:
            continue
        if room.rect:
            x, y, w, h = room.rect
            room_edges = [
                ((x, y), (x + w, y)),
                ((x + w, y), (x + w, y + h)),
                ((x + w, y + h), (x, y + h)),
                ((x, y + h), (x, y))
            ]
            for p1, p2 in room_edges:
                canon = tuple(sorted([p1, p2]))
                edges_count[canon] = edges_count.get(canon, 0) + 1

    min_x, min_y, max_x, max_y = spec.get_overall_bounding_box()
    c_x = (min_x + max_x) / 2.0
    c_y = (min_y + max_y) / 2.0

    # Draw walls
    for edge, count in edges_count.items():
        p1, p2 = edge
        is_exterior = (count == 1)
        layer = "A-WALL-EXTR" if is_exterior else "A-WALL-INTR"
        thickness = ext_t if is_exterior else int_t

        # Primary baseline
        msp.add_line(p1, p2, dxfattribs={"layer": layer})

        # Calculate normal vector for double wall
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        length = math.hypot(dx, dy)
        if length > 0:
            nx = -dy / length
            ny = dx / length

            mid_x = (p1[0] + p2[0]) / 2.0
            mid_y = (p1[1] + p2[1]) / 2.0

            if is_exterior:
                # Always offset exterior wall outwards
                to_mid_x = mid_x - c_x
                to_mid_y = mid_y - c_y
                if (nx * to_mid_x + ny * to_mid_y) < 0:
                    nx = -nx
                    ny = -ny
                off_p1 = (p1[0] + nx * thickness, p1[1] + ny * thickness)
                off_p2 = (p2[0] + nx * thickness, p2[1] + ny * thickness)
                msp.add_line(off_p1, off_p2, dxfattribs={"layer": layer})
            else:
                # Interior partition: clean single parallel line
                off_p1 = (p1[0] + nx * thickness, p1[1] + ny * thickness)
                off_p2 = (p2[0] + nx * thickness, p2[1] + ny * thickness)
                msp.add_line(off_p1, off_p2, dxfattribs={"layer": layer})

def _draw_columns(msp, spec: CADSpec) -> None:
    """Inserts reinforced concrete column blocks."""
    for col in spec.columns:
        x, y = col.pos
        msp.add_blockref("COLUMN_300x300", insert=(x, y), dxfattribs={"layer": "A-COLS"})

def _extract_short_tag(label_or_id: str, default_prefix: str = "D") -> str:
    """Extracts a short, clean tag (e.g. 'D1', 'W1', 'DM') without long dimensions."""
    if not label_or_id:
        return default_prefix
    # Remove anything in parenthesis (e.g. "D1 (900x2100)" -> "D1")
    raw = label_or_id.split("(")[0].strip()
    if "MAIN" in raw.upper():
        return "DM"
    if "_" in raw:
        parts = raw.split("_")
        return (parts[0][0] + parts[1][:2]).upper()
    return raw[:4].upper()

def _draw_doors(msp, spec: CADSpec) -> None:
    """Inserts door blocks with clean, non-cluttering architectural tag bubbles."""
    orientation_angles = {
        "S": 0.0,
        "E": 90.0,
        "N": 180.0,
        "W": 270.0
    }

    for door in spec.doors:
        x, y = door.pos
        angle = orientation_angles.get(door.orientation.upper(), 0.0)
        try:
            angle = float(door.orientation)
        except ValueError:
            pass

        # Choose block
        blk_name = "DOOR_SINGLE_900"
        if door.type == "double" or door.width >= 1400:
            blk_name = "DOOR_DOUBLE_1500"
        elif door.width <= 750:
            blk_name = "DOOR_SINGLE_750"
        elif door.width >= 1000:
            blk_name = "DOOR_SINGLE_1000"

        msp.add_blockref(
            blk_name,
            insert=(x, y),
            dxfattribs={
                "layer": "A-DOOR",
                "rotation": angle
            }
        )

        # Professional Door Tag: neat small circle with short tag (e.g. 'D1', 'DM')
        short_tag = _extract_short_tag(door.label or door.id, "D")
        # Position tag slightly offset from door hinge
        rad = math.radians(angle + 45)
        tag_x = x + 250 * math.cos(rad)
        tag_y = y + 250 * math.sin(rad)

        # Draw neat tag bubble
        msp.add_circle((tag_x, tag_y), radius=90.0, dxfattribs={"layer": "A-ANNO-TEXT"})
        msp.add_text(
            short_tag,
            dxfattribs={
                "layer": "A-ANNO-TEXT",
                "height": 70.0
            }
        ).set_placement((tag_x, tag_y), align=TextEntityAlignment.MIDDLE_CENTER)

def _draw_windows(msp, spec: CADSpec) -> None:
    """Inserts window blocks and clean exterior tag bubbles."""
    orientation_angles = {
        "S": 0.0,
        "E": 90.0,
        "N": 180.0,
        "W": 270.0
    }

    for win in spec.windows:
        x, y = win.pos
        angle = orientation_angles.get(win.orientation.upper(), 0.0)
        try:
            angle = float(win.orientation)
        except ValueError:
            pass

        # Select window block
        blk_name = "WINDOW_1500"
        if win.width >= 1700:
            blk_name = "WINDOW_1800"
        elif win.width <= 700:
            blk_name = "VENTILATOR_600"
        elif win.width <= 1300:
            blk_name = "WINDOW_1200"

        msp.add_blockref(
            blk_name,
            insert=(x, y),
            dxfattribs={
                "layer": "A-GLAZ",
                "rotation": angle
            }
        )

        # Window Tag Symbol: placed cleanly on exterior side
        short_tag = _extract_short_tag(win.label or win.id, "W")
        rad = math.radians(angle - 90) # Exterior side
        tag_x = x + (win.width / 2.0) * math.cos(math.radians(angle)) + 280.0 * math.cos(rad)
        tag_y = y + (win.width / 2.0) * math.sin(math.radians(angle)) + 280.0 * math.sin(rad)

        msp.add_circle((tag_x, tag_y), radius=90.0, dxfattribs={"layer": "A-ANNO-TEXT"})
        msp.add_text(
            short_tag,
            dxfattribs={
                "layer": "A-ANNO-TEXT",
                "height": 70.0
            }
        ).set_placement((tag_x, tag_y), align=TextEntityAlignment.MIDDLE_CENTER)

def _draw_fixtures(msp, spec: CADSpec) -> None:
    """Inserts furniture and sanitary fixtures."""
    fixture_map = {
        "bed_queen": "BED_QUEEN",
        "bed_single": "BED_SINGLE",
        "sofa_3seater": "SOFA_3SEATER",
        "toilet_water_closet": "TOILET_WC",
        "toilet_wc": "TOILET_WC",
        "wash_basin": "WASH_BASIN"
    }

    for fix in spec.fixtures:
        blk_name = fixture_map.get(fix.type.lower())
        if blk_name:
            msp.add_blockref(
                blk_name,
                insert=(fix.pos[0], fix.pos[1]),
                dxfattribs={
                    "layer": "A-FLOR-FIXT",
                    "rotation": fix.rotation
                }
            )

def _draw_room_labels(msp, spec: CADSpec) -> None:
    """
    Draws clean, professional 2-line room labels:
    Line 1: Room Name (e.g. 'BEDROOM', 'LIVING')
    Line 2: Area (e.g. '18.9 m²')
    Zero clutter: finish notes are kept in schedules.
    """
    for room in spec.rooms:
        cx, cy = room.center
        area_sqm = room.area_sqm

        # Adaptive text height based on room dimension
        min_dim = 3000.0
        if room.rect:
            min_dim = min(room.rect[2], room.rect[3])

        if min_dim < 2000.0:
            name_h = 100.0
            area_h = 75.0
            gap = 65.0
        elif min_dim < 3000.0:
            name_h = 120.0
            area_h = 85.0
            gap = 75.0
        else:
            name_h = 150.0
            area_h = 100.0
            gap = 95.0

        # Room Name
        msp.add_text(
            room.name.upper(),
            dxfattribs={
                "layer": "A-ANNO-TEXT",
                "height": name_h,
            }
        ).set_placement((cx, cy + gap * 0.6), align=TextEntityAlignment.MIDDLE_CENTER)

        # Area
        msp.add_text(
            f"{area_sqm:.1f} m²",
            dxfattribs={
                "layer": "A-ANNO-TEXT",
                "height": area_h,
            }
        ).set_placement((cx, cy - gap * 0.6), align=TextEntityAlignment.MIDDLE_CENTER)

def _draw_exterior_dimensions(msp, spec: CADSpec) -> None:
    """Generates crisp architectural dimension lines around building perimeter."""
    min_x, min_y, max_x, max_y = spec.get_overall_bounding_box()
    ext_t = spec.settings.wall_exterior_thickness
    offset_dist = ext_t + 700.0

    # Overall Width Dimension (Bottom)
    _add_architectural_dimension(
        msp,
        p1=(min_x, min_y - offset_dist),
        p2=(max_x, min_y - offset_dist),
        text=f"{int(max_x - min_x)}",
        is_horizontal=True,
        ext_points=((min_x, min_y), (max_x, min_y))
    )

    # Overall Height Dimension (Left)
    _add_architectural_dimension(
        msp,
        p1=(min_x - offset_dist, min_y),
        p2=(min_x - offset_dist, max_y),
        text=f"{int(max_y - min_y)}",
        is_horizontal=False,
        ext_points=((min_x, min_y), (min_x, max_y))
    )

def _add_architectural_dimension(
    msp,
    p1: Tuple[float, float],
    p2: Tuple[float, float],
    text: str,
    is_horizontal: bool,
    ext_points: Optional[Tuple[Tuple[float, float], Tuple[float, float]]] = None
) -> None:
    """Draws a vector architectural dimension line with extension lines, 45-degree ticks, and centered text."""
    layer = "A-ANNO-DIMS"
    tick_len = 100.0

    # Main dimension line
    msp.add_line(p1, p2, dxfattribs={"layer": layer})

    # Extension lines from building corners
    if ext_points:
        ep1, ep2 = ext_points
        msp.add_line(ep1, p1, dxfattribs={"layer": layer})
        msp.add_line(ep2, p2, dxfattribs={"layer": layer})

    # 45-degree ticks
    t_dx = tick_len * 0.7071
    t_dy = tick_len * 0.7071
    msp.add_line((p1[0] - t_dx, p1[1] - t_dy), (p1[0] + t_dx, p1[1] + t_dy), dxfattribs={"layer": layer})
    msp.add_line((p2[0] - t_dx, p2[1] - t_dy), (p2[0] + t_dx, p2[1] + t_dy), dxfattribs={"layer": layer})

    # Center text
    mid_x = (p1[0] + p2[0]) / 2.0
    mid_y = (p1[1] + p2[1]) / 2.0
    text_offset = 100.0

    if is_horizontal:
        pos = (mid_x, mid_y + text_offset)
        rot = 0.0
    else:
        pos = (mid_x - text_offset, mid_y)
        rot = 90.0

    msp.add_text(
        text,
        dxfattribs={
            "layer": "A-ANNO-TEXT",
            "height": 130.0,
            "rotation": rot
        }
    ).set_placement(pos, align=TextEntityAlignment.MIDDLE_CENTER)

def _draw_title_block_and_border(msp, spec: CADSpec) -> None:
    """Generates standard architectural sheet border and title block with generous spacing."""
    min_x, min_y, max_x, max_y = spec.get_overall_bounding_box()
    margin = 1500.0

    bx1 = min_x - margin
    by1 = min_y - margin
    bx2 = max_x + margin + 3500.0 # Room on right for title block
    by2 = max_y + margin

    border_layer = "A-TITL"
    text_layer = "A-ANNO-TEXT"

    # Outer Sheet Border
    msp.add_lwpolyline([(bx1, by1), (bx2, by1), (bx2, by2), (bx1, by2), (bx1, by1)], close=True, dxfattribs={"layer": border_layer})

    # Inner Margin Line (100mm offset)
    in_offset = 100.0
    msp.add_lwpolyline([
        (bx1 + in_offset, by1 + in_offset),
        (bx2 - in_offset, by1 + in_offset),
        (bx2 - in_offset, by2 - in_offset),
        (bx1 + in_offset, by2 - in_offset),
        (bx1 + in_offset, by1 + in_offset)
    ], close=True, dxfattribs={"layer": border_layer})

    # Title Block in Bottom Right Corner (3200 x 1800 mm)
    tb_w = 3200.0
    tb_h = 1800.0
    tb_x1 = bx2 - in_offset - tb_w
    tb_y1 = by1 + in_offset
    tb_x2 = bx2 - in_offset
    tb_y2 = tb_y1 + tb_h

    # Title box outline
    msp.add_lwpolyline([(tb_x1, tb_y1), (tb_x2, tb_y1), (tb_x2, tb_y2), (tb_x1, tb_y2), (tb_x1, tb_y1)], close=True, dxfattribs={"layer": border_layer})

    # Row dividers
    msp.add_line((tb_x1, tb_y1 + 1200), (tb_x2, tb_y1 + 1200), dxfattribs={"layer": border_layer})
    msp.add_line((tb_x1, tb_y1 + 600), (tb_x2, tb_y1 + 600), dxfattribs={"layer": border_layer})
    # Vertical divider for bottom row
    msp.add_line((tb_x1 + 1600, tb_y1), (tb_x1 + 1600, tb_y1 + 600), dxfattribs={"layer": border_layer})

    # Metadata
    meta = spec.project

    # Top cell: Project Name
    msp.add_text("PROJECT:", dxfattribs={"layer": text_layer, "height": 70.0}).set_placement((tb_x1 + 100, tb_y2 - 120))
    msp.add_text(meta.name.upper(), dxfattribs={"layer": text_layer, "height": 110.0}).set_placement((tb_x1 + 100, tb_y2 - 320))

    # Middle cell: Client & Designer
    msp.add_text(f"CLIENT: {meta.client}", dxfattribs={"layer": text_layer, "height": 80.0}).set_placement((tb_x1 + 100, tb_y1 + 960))
    msp.add_text(f"DESIGNER: {meta.designer}", dxfattribs={"layer": text_layer, "height": 80.0}).set_placement((tb_x1 + 100, tb_y1 + 760))

    # Bottom left: Scale & Date
    msp.add_text(f"SCALE: {meta.scale}", dxfattribs={"layer": text_layer, "height": 75.0}).set_placement((tb_x1 + 100, tb_y1 + 380))
    msp.add_text(f"DATE: {meta.date}", dxfattribs={"layer": text_layer, "height": 75.0}).set_placement((tb_x1 + 100, tb_y1 + 180))

    # Bottom right: Sheet No & Rev
    msp.add_text(f"SHEET: {meta.drawing_number}", dxfattribs={"layer": text_layer, "height": 95.0}).set_placement((tb_x1 + 1700, tb_y1 + 380))
    msp.add_text(f"REV: {meta.revision}", dxfattribs={"layer": text_layer, "height": 75.0}).set_placement((tb_x1 + 1700, tb_y1 + 180))

    # North Arrow in top-right
    north_x = bx2 - in_offset - 1000.0
    north_y = by2 - in_offset - 1000.0
    msp.add_blockref(
        "NORTH_ARROW",
        insert=(north_x, north_y),
        dxfattribs={
            "layer": text_layer,
            "rotation": spec.settings.north_angle_deg
        }
    )
