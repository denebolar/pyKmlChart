"""
Unit test cases to cover the module legend.
"""
from __future__ import print_function
import unittest
from kmlChart.legend import *
from kmlChart.colorBars import jet


class LegendTest(unittest.TestCase):
    def test_image(self):
        p = pngLegend((3, 4.5), jet)
        p.save('test.png')
