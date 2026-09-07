"""
Declarative Architectural Specification and Data Schema.

Defines Pydantic/dataclass representations for project metadata, spatial boundaries,
structural columns, architectural openings, and interior fixtures with unit conversions.

Author: Montasir Tajwar Jihan
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
import json
import os

@dataclass
class ProjectMeta:
    name: str = "Architectural CAD Project"
    project_id: str = "PRJ-001"
    client: str = "Standard Client"
    designer: str = "Montasir Tajwar Jihan"
    date: str = "2026-09-08"
    units: str = "mm"
    scale: str = "1:100"
    drawing_number: str = "A-101"
    revision: str = "R1"

@dataclass
class Settings:
    units: str = "mm"
    wall_exterior_thickness: float = 250.0
    wall_interior_thickness: float = 125.0
    default_ceiling_height: float = 2800.0
    grid_snap: float = 50.0
    north_angle_deg: float = 0.0
    auto_exterior_dimensions: bool = True
    include_title_block: bool = True

@dataclass
class Room:
    id: str
    name: str
    category: str = "general"
    rect: Optional[List[float]] = None          # [x, y, width, height]
    polygon: Optional[List[List[float]]] = None # [[x1, y1], [x2, y2], ...]
    finish: str = "Standard"
    color: str = "white"

    @property
    def bounds(self) -> Tuple[float, float, float, float]:
        """Returns bounding envelope (min_x, min_y, max_x, max_y)."""
        if self.rect:
            x, y, w, h = self.rect
            return (x, y, x + w, y + h)
        elif self.polygon:
            xs = [p[0] for p in self.polygon]
            ys = [p[1] for p in self.polygon]
            return (min(xs), min(ys), max(xs), max(ys))
        return (0.0, 0.0, 0.0, 0.0)

    @property
    def area_sqm(self) -> float:
        """Computes internal net carpet area in square meters."""
        if self.rect:
            _, _, w, h = self.rect
            return (w * h) / 1_000_000.0
        elif self.polygon and len(self.polygon) >= 3:
            # Gauss's shoelace formula
            area = 0.0
            n = len(self.polygon)
            for i in range(n):
                j = (i + 1) % n
                area += self.polygon[i][0] * self.polygon[j][1]
                area -= self.polygon[j][0] * self.polygon[i][1]
            return abs(area) / 2.0 / 1_000_000.0
        return 0.0

    @property
    def center(self) -> Tuple[float, float]:
        """Returns centroid (cx, cy) of room bounding box."""
        min_x, min_y, max_x, max_y = self.bounds
        return ((min_x + max_x) / 2.0, (min_y + max_y) / 2.0)

@dataclass
class Door:
    id: str
    pos: List[float]               # Insertion point [x, y]
    width: float = 900.0
    height: float = 2100.0
    orientation: str = "S"         # Cardinal ("N", "S", "E", "W") or angle
    swing: str = "left"            # "left", "right", "double", "sliding"
    label: str = ""
    room_id: str = ""
    type: str = "single"

@dataclass
class Window:
    id: str
    pos: List[float]               # Insertion point [x, y]
    width: float = 1500.0
    height: float = 1200.0
    sill_height: float = 900.0
    orientation: str = "N"
    label: str = ""

@dataclass
class Column:
    id: str
    pos: List[float]
    size: List[float] = field(default_factory=lambda: [300.0, 300.0])

@dataclass
class Fixture:
    id: str
    type: str
    pos: List[float]
    rotation: float = 0.0

@dataclass
class CADSpec:
    project: ProjectMeta = field(default_factory=ProjectMeta)
    settings: Settings = field(default_factory=Settings)
    rooms: List[Room] = field(default_factory=list)
    doors: List[Door] = field(default_factory=list)
    windows: List[Window] = field(default_factory=list)
    columns: List[Column] = field(default_factory=list)
    fixtures: List[Fixture] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CADSpec":
        proj_data = data.get("project", {})
        project = ProjectMeta(
            name=proj_data.get("name", "Architectural CAD Project"),
            project_id=proj_data.get("project_id", "PRJ-001"),
            client=proj_data.get("client", "Standard Client"),
            designer=proj_data.get("designer", "Montasir Tajwar Jihan"),
            date=proj_data.get("date", "2026-09-08"),
            units=proj_data.get("units", "mm"),
            scale=proj_data.get("scale", "1:100"),
            drawing_number=proj_data.get("drawing_number", "A-101"),
            revision=proj_data.get("revision", "R1")
        )

        set_data = data.get("settings", {})
        settings = Settings(
            units=set_data.get("units", "mm"),
            wall_exterior_thickness=float(set_data.get("wall_exterior_thickness", 250.0)),
            wall_interior_thickness=float(set_data.get("wall_interior_thickness", 125.0)),
            default_ceiling_height=float(set_data.get("default_ceiling_height", 2800.0)),
            grid_snap=float(set_data.get("grid_snap", 50.0)),
            north_angle_deg=float(set_data.get("north_angle_deg", 0.0)),
            auto_exterior_dimensions=bool(set_data.get("auto_exterior_dimensions", True)),
            include_title_block=bool(set_data.get("include_title_block", True))
        )

        rooms = []
        for r in data.get("rooms", []):
            rooms.append(Room(
                id=r["id"],
                name=r.get("name", r["id"].upper()),
                category=r.get("category", "general"),
                rect=r.get("rect"),
                polygon=r.get("polygon"),
                finish=r.get("finish", "Standard"),
                color=r.get("color", "white")
            ))

        openings = data.get("openings", {})
        doors = []
        for d in openings.get("doors", []):
            doors.append(Door(
                id=d["id"],
                pos=d["pos"],
                width=float(d.get("width", 900.0)),
                height=float(d.get("height", 2100.0)),
                orientation=str(d.get("orientation", "S")),
                swing=d.get("swing", "left"),
                label=d.get("label", d["id"]),
                room_id=d.get("room_id", ""),
                type=d.get("type", "single")
            ))

        windows = []
        for w in openings.get("windows", []):
            windows.append(Window(
                id=w["id"],
                pos=w["pos"],
                width=float(w.get("width", 1500.0)),
                height=float(w.get("height", 1200.0)),
                sill_height=float(w.get("sill_height", 900.0)),
                orientation=str(w.get("orientation", "N")),
                label=w.get("label", w["id"])
            ))

        columns = []
        for c in data.get("columns", []):
            columns.append(Column(
                id=c["id"],
                pos=c["pos"],
                size=[float(s) for s in c.get("size", [300.0, 300.0])]
            ))

        fixtures = []
        for f in data.get("fixtures", []):
            fixtures.append(Fixture(
                id=f["id"],
                type=f["type"],
                pos=f["pos"],
                rotation=float(f.get("rotation", 0.0))
            ))

        return cls(
            project=project,
            settings=settings,
            rooms=rooms,
            doors=doors,
            windows=windows,
            columns=columns,
            fixtures=fixtures
        )

    @classmethod
    def load_json(cls, file_path: str) -> "CADSpec":
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)

    def get_overall_bounding_box(self) -> Tuple[float, float, float, float]:
        """Calculates boundary envelope of all rooms."""
        if not self.rooms:
            return (0.0, 0.0, 1000.0, 1000.0)
        min_x = min(r.bounds[0] for r in self.rooms)
        min_y = min(r.bounds[1] for r in self.rooms)
        max_x = max(r.bounds[2] for r in self.rooms)
        max_y = max(r.bounds[3] for r in self.rooms)
        return (min_x, min_y, max_x, max_y)
