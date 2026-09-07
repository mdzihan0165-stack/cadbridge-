"""
Headless CAD Vector Rasterizer and Plot Preview Renderer.

Utilizes matplotlib and ezdxf.addons.drawing to synthesize high-resolution
inspection snapshots (PNG/SVG) in dark modelspace and light paper plot styles.

Author: Montasir Tajwar Jihan
"""
import os
import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing.config import Configuration, BackgroundPolicy, ColorPolicy
import matplotlib
matplotlib.use("Agg")  # Non-interactive headless backend
import matplotlib.pyplot as plt

def render_dxf_snapshot(
    dxf_path: str,
    output_image_path: str,
    theme: str = "dark",
    dpi: int = 200,
    width_inches: float = 16.0,
    height_inches: float = 12.0
) -> str:
    """
    Renders a DXF file to an image file (PNG/SVG/PDF).

    Args:
        dxf_path: Path to input .dxf file
        output_image_path: Path to output image (.png, .svg, .pdf)
        theme: 'dark' (AutoCAD model space style) or 'light' (white paper/plot style)
        dpi: Resolution for raster output (default 200)
        width_inches: Figure width
        height_inches: Figure height

    Returns:
        output_image_path on success
    """
    if not os.path.exists(dxf_path):
        raise FileNotFoundError(f"DXF file not found: {dxf_path}")

    os.makedirs(os.path.dirname(os.path.abspath(output_image_path)), exist_ok=True)

    doc = ezdxf.readfile(dxf_path)
    msp = doc.modelspace()

    # Determine background and line color policies
    is_dark = (theme.lower() == "dark")
    bg_color = "#1e222a" if is_dark else "#ffffff"

    # Configure ezdxf rendering context
    config = Configuration(
        background_policy=BackgroundPolicy.CUSTOM,
        custom_bg_color=bg_color,
        color_policy=ColorPolicy.COLOR if is_dark else ColorPolicy.COLOR
    )

    ctx = RenderContext(doc)

    fig = plt.figure(figsize=(width_inches, height_inches), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(bg_color)
    fig.patch.set_facecolor(bg_color)

    out = MatplotlibBackend(ax)
    frontend = Frontend(ctx, out, config=config)
    frontend.draw_layout(msp, finalize=True)

    # Save figure
    fig.savefig(
        output_image_path,
        dpi=dpi,
        facecolor=bg_color,
        edgecolor="none",
        bbox_inches="tight",
        pad_inches=0.1
    )
    plt.close(fig)

    return output_image_path
