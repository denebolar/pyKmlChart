"""
Test module for chart module.
"""
from __future__ import print_function
import unittest
from kmlChart.chart import *
from kmlChart.colorBars import jet2


class chartTests(unittest.TestCase):
    def test_chart(self):
        chart = Bar3D('TestBarChart')
        num = 20
        chart.add([10]*num, [51 + i*0.01 for i in xrange(num)], [500 + i*100 for i in xrange(num)], radius=0.005*0.8, colorbar=jet2)
        chart.add([10.02]*num, [51 + i*0.01 for i in xrange(num)], [500 + i*100 for i in xrange(num)], radius=0.005*0.8, colorbar=jet)
        chart.save('chart.kml')

        chart = Surface('TestSurfaceChart')
        c = ((-0.005, -0.005), (+0.005, -0.005), (+0.005, +0.005), (-0.005, +0.005), (-0.005, -0.005), )
        chart.add(tuple(tuple((i[0] + 10.04, i[1] + (51 + lat*0.01)) for i in c) for lat in xrange(num)), tuple(i for i in xrange(num)),
                  display_name='Surface plot')
        chart.add(tuple(tuple((i[0] + 10.06, i[1] + (51 + lat*0.01)) for i in c) for lat in xrange(num)), tuple(i for i in xrange(num)),
            border_color=(0x00, 0x00, 0xff),
            display_name='Surface plot with border',
        )
        chart.add(tuple(tuple((i[0] + 10.08, i[1] + (51 + lat*0.01)) for i in c) for lat in xrange(num)), tuple(i for i in xrange(num)),
            border_color=(0xff, 0xff, 0xff),
            opacity=0x80,
            border_opacity=0xff,
            border_width=1,
            display_name='Transparent surface plot',
        )
        chart.save('chart2.kml')
