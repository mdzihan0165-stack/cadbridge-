"""
Spatial Layout and 2D Planar Constraint Solver.

Resolves topological room adjacency constraints, target surface areas, and structural
grid snapping to compute collision-free architectural floorplan bounding boxes.

Author: Montasir Tajwar Jihan
"""
from typing import List, Dict, Any, Tuple, Optional
import math

class SpatialLayoutSolver:
    """
    Solves 2D spatial layout constraints for architectural floorplans.
    Maps high-level topological rules (e.g. 'kitchen East of living') into snapped coordinates.
    """

    def __init__(self, grid_snap: float = 100.0):
        self.grid_snap = grid_snap

    def snap(self, val: float) -> float:
        """Snap value to grid increment."""
        return round(val / self.grid_snap) * self.grid_snap

    def solve_layout(
        self,
        room_requests: List[Dict[str, Any]],
        starting_point: Tuple[float, float] = (0.0, 0.0)
    ) -> List[Dict[str, Any]]:
        """
        Solves and positions rooms based on adjacency constraints.

        room_requests example:
        [
            {"id": "living", "name": "Living & Dining", "width": 6000, "height": 4200},
            {"id": "kitchen", "name": "Kitchen", "width": 3000, "height": 2400, "rel_to": "living", "side": "E", "align": "bottom"},
            {"id": "master_bed", "name": "Master Bed", "width": 4200, "height": 3600, "rel_to": "living", "side": "N", "align": "left"},
            {"id": "attached_bath", "name": "Attached Bath", "width": 1800, "height": 2100, "rel_to": "master_bed", "side": "E", "align": "bottom"}
        ]
        """
        placed_rooms: Dict[str, Dict[str, Any]] = {}
        result_rooms: List[Dict[str, Any]] = []

        for req in room_requests:
            r_id = req["id"]
            name = req.get("name", r_id.upper())
            w = self.snap(float(req.get("width", 3000.0)))
            h = self.snap(float(req.get("height", 3000.0)))

            rel_to = req.get("rel_to")
            side = req.get("side", "E").upper()
            align = req.get("align", "bottom").lower()

            if not rel_to or rel_to not in placed_rooms:
                # Place at origin or starting point
                x = self.snap(starting_point[0])
                y = self.snap(starting_point[1])
            else:
                ref = placed_rooms[rel_to]
                ref_x, ref_y, ref_w, ref_h = ref["rect"]

                if side == "E": # East (Right of ref)
                    x = ref_x + ref_w
                    if align == "top":
                        y = ref_y + ref_h - h
                    elif align == "center":
                        y = ref_y + (ref_h - h) / 2.0
                    else: # bottom
                        y = ref_y
                elif side == "W": # West (Left of ref)
                    x = ref_x - w
                    if align == "top":
                        y = ref_y + ref_h - h
                    elif align == "center":
                        y = ref_y + (ref_h - h) / 2.0
                    else:
                        y = ref_y
                elif side == "N": # North (Above ref)
                    y = ref_y + ref_h
                    if align == "right":
                        x = ref_x + ref_w - w
                    elif align == "center":
                        x = ref_x + (ref_w - w) / 2.0
                    else: # left
                        x = ref_x
                elif side == "S": # South (Below ref)
                    y = ref_y - h
                    if align == "right":
                        x = ref_x + ref_w - w
                    elif align == "center":
                        x = ref_x + (ref_w - w) / 2.0
                    else: # left
                        x = ref_x
                else:
                    x = ref_x + ref_w
                    y = ref_y

                x = self.snap(x)
                y = self.snap(y)

            room_entry = {
                "id": r_id,
                "name": name,
                "category": req.get("category", "general"),
                "rect": [x, y, w, h],
                "finish": req.get("finish", "Standard")
            }
            placed_rooms[r_id] = room_entry
            result_rooms.append(room_entry)

        return result_rooms

    def validate_no_overlap(self, rooms: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
        """Checks whether any rooms overlap destructively."""
        issues = []
        n = len(rooms)
        for i in range(n):
            for j in range(i + 1, n):
                r1 = rooms[i]
                r2 = rooms[j]
                x1, y1, w1, h1 = r1["rect"]
                x2, y2, w2, h2 = r2["rect"]

                # Check intersection with positive area
                overlap_x = max(0.0, min(x1 + w1, x2 + w2) - max(x1, x2))
                overlap_y = max(0.0, min(y1 + h1, y2 + h2) - max(y1, y2))

                if overlap_x > 1.0 and overlap_y > 1.0:
                    issues.append(f"Room '{r1['id']}' overlaps with '{r2['id']}' by {overlap_x:.0f}x{overlap_y:.0f} mm")

        return (len(issues) == 0, issues)
