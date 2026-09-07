"""
Unit tests for CadBridge CAD compiler and DXF synthesis.

Author: Montasir Tajwar Jihan
"""
import os
import unittest
import tempfile
import ezdxf

from cadbridge.core.spec import CADSpec, Room, Door, Window, Column
from cadbridge.compiler.json2dxf import compile_spec_to_dxf
from cadbridge.solver.spatial_solver import SpatialLayoutSolver
from cadbridge.boq.cad_boq import generate_boq_report

class TestCADCompiler(unittest.TestCase):

    def setUp(self):
        self.spec_dict = {
            "project": {
                "name": "Test Floorplan",
                "designer": "Montasir Tajwar Jihan"
            },
            "rooms": [
                {"id": "living", "name": "LIVING", "rect": [0, 0, 5000, 4000]},
                {"id": "bed", "name": "BEDROOM", "rect": [5000, 0, 4000, 4000]}
            ],
            "openings": {
                "doors": [{"id": "D1", "pos": [2000, 0], "width": 900}],
                "windows": [{"id": "W1", "pos": [1000, 4000], "width": 1200}]
            },
            "columns": [
                {"id": "C1", "pos": [0, 0]},
                {"id": "C2", "pos": [5000, 0]}
            ]
        }
        self.spec = CADSpec.from_dict(self.spec_dict)

    def test_dxf_synthesis_and_layers(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_dxf = os.path.join(tmp_dir, "test.dxf")
            res_path = compile_spec_to_dxf(self.spec, out_dxf)

            self.assertTrue(os.path.exists(res_path))

            doc = ezdxf.readfile(res_path)
            msp = doc.modelspace()

            # Verify standard AIA layers exist
            expected_layers = ["A-WALL-EXTR", "A-DOOR", "A-GLAZ", "A-COLS", "A-ANNO-TEXT", "A-TITL"]
            for lay in expected_layers:
                self.assertIn(lay, doc.layers)

            # Verify entities exist
            lines = list(msp.query("LINE"))
            self.assertGreater(len(lines), 0)

            # Verify title block designer is Montasir Tajwar Jihan
            texts = [t.dxf.text for t in msp.query("TEXT")]
            self.assertTrue(any("MONTASIR TAJWAR JIHAN" in t.upper() for t in texts))

    def test_spatial_solver(self):
        solver = SpatialLayoutSolver(grid_snap=100.0)
        requests = [
            {"id": "r1", "width": 4000, "height": 3000},
            {"id": "r2", "width": 3000, "height": 3000, "rel_to": "r1", "side": "E"}
        ]
        solved = solver.solve_layout(requests)
        self.assertEqual(len(solved), 2)
        valid, issues = solver.validate_no_overlap(solved)
        self.assertTrue(valid)
        self.assertEqual(len(issues), 0)

    def test_boq_generation(self):
        md = generate_boq_report(self.spec)
        self.assertIn("Total Carpet Area", md)
        self.assertIn("LIVING", md)
        self.assertIn("BEDROOM", md)

if __name__ == "__main__":
    unittest.main()
