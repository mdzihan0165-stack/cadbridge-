"""
CadBridge: Computational 2D CAD Compiler & Algorithmic Drafting Engine.

An engineering automation framework for synthesizing production-ready
AutoCAD DXF drawings from declarative spatial models with automated
AIA/ISO layer standards, parametric blocks, and quantity takeoff.

Author: Montasir Tajwar Jihan
License: MIT License
"""

__version__ = "1.0.0"
__author__ = "Montasir Tajwar Jihan"
__email__ = "montasir.jihan@engineering.local"

from .core.spec import CADSpec, Room, Door, Window, Column, Fixture
from .compiler.json2dxf import compile_spec_to_dxf
from .solver.spatial_solver import SpatialLayoutSolver
from .qa.cad_snapshot import render_dxf_snapshot
from .boq.cad_boq import generate_boq_report

__all__ = [
    "CADSpec",
    "Room",
    "Door",
    "Window",
    "Column",
    "Fixture",
    "compile_spec_to_dxf",
    "SpatialLayoutSolver",
    "render_dxf_snapshot",
    "generate_boq_report",
]
