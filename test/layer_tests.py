from copy import deepcopy
import unittest

from src.constants import CONSTANTS
from src.layers import Layers, Layer

class TestLayer(unittest.TestCase):
    
    def test_default_layers(self):
        # from morris_constants.toml: top=Du=0, bottom=Db=-30
        testobj = Layers()
        self.assertListEqual([Layer(top=0.0, bottom=-30.0)], testobj.layers)

    def test_update_bed_accretion(self):
        testobj = Layers()
        testobj.update_bed(deposition=1.0)
        self.assertListEqual([Layer(top=0.0, bottom=-30.0), Layer(top=1, bottom=0)], testobj.layers)

    def test_update_bed_erosion_in_bottom_layer(self):
        testobj = Layers()
        testobj.update_bed(deposition=-1.0)
        self.assertListEqual([Layer(top=-1.0, bottom=-31.0), Layer(top=-1.0, bottom=-1.0)], testobj.layers)

    def test_update_bed_erosion_in_one_previous_layer(self):
        testobj = Layers()
        deposition_sequence = [2, -1]
        for d in deposition_sequence:
            testobj.update_bed(deposition=d)
        self.assertListEqual([Layer(top=0.0, bottom=-30.0), Layer(top=1.0, bottom=0.0), Layer(top=1.0, bottom=1.0)], testobj.layers)

    def test_update_bed_erosion_excess_erosion_in_bottom_layer(self):
        testobj = Layers()
        deposition_sequence = [2, -3]
        for d in deposition_sequence:
            testobj.update_bed(deposition=d)
        self.assertListEqual([Layer(top=-1.0, bottom=-31.0), Layer(top=-1.0, bottom=-1.0), Layer(top=-1.0, bottom=-1.0)], testobj.layers)

