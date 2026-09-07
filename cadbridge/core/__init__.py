"""Core modules for CADBridge: layers, blocks, and spec definitions."""
from .layers import setup_standard_layers, LayerConfig, STANDARD_LAYERS
from .blocks import setup_standard_blocks
from .spec import CADSpec, Room, Door, Window, Column, Fixture

__all__ = [
    "setup_standard_layers",
    "LayerConfig",
    "STANDARD_LAYERS",
    "setup_standard_blocks",
    "CADSpec",
    "Room",
    "Door",
    "Window",
    "Column",
    "Fixture",
]
