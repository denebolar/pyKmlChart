"""
Unit test cases to cover the module kmlInterface.
"""

from __future__ import print_function
import unittest
from kmlChart.kmlInterface import *
from kmlChart.kmlInterface import _renderer
from math import sin, pi, cos


class InterfaceTest( unittest.TestCase ):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.kmlData = KMLdata()

    def test_kmlOutput(self):
        print(self.kmlData.getAsString())

    def test_kmlStyles(self):
        bs = BalloonStyle(bgColor='11223344', text='blakram')
        ps = PolyStyle(color='44332211', fill=1)
        self.kmlData.styles.addStyle('singlePolyStyle', ps)
        self.kmlData.styles.addStyle('multiStyle', [ps, bs])
        print(self.kmlData.getAsString())

    def test_kml_renderer(self):
        xml = ElementTree.Element('root')
        data = {
            'bla': 2,
            'kram': [
                'foo',
                'bar',
                {
                    'nested': 'text'
                },
            ],
            'gedoens': 'geraffel',
        }
        _renderer(xml, 'key', data)
        print(ElementTree.tostring(xml, encoding='utf-8'))

    def test_Polygon(self):
        self.kmlData.add(Placemark().add(Polygon(((1,1), (2,2,2), (3,3)))))
        print(self.kmlData.getAsString())

    def test_Bar(self):
        c = circle(center=(10,50), radius=(0.01 / cos(50.0/180*pi), 0.01))
        c2 = circle(center=(10.01,50), radius=(0.01 / cos(50.0/180*pi), 0.01))
        kml = KMLdata()
        kml.styles.addStyle('myStyle', (PolyStyle(color='ffff0000', outline=False), LineStyle(color='ff00ff00')))
        kml.add(Folder(name='TestFolder')
            .add(Placemark('TestPlacemark', description='TestDescription', style='#myStyle')
                 .add(Polygon((i + (1000,) for i in c), extrude=True, altitudeMode='relativeToGround')))
            .add(Placemark('TestPlacemark2', description='TestDescription2', style='#myStyle')
                 .add(Polygon((i + (1000,) for i in c2), extrude=True, altitudeMode='relativeToGround')))
        )
        #with open('test.kml', 'w') as f:
        #    f.write(kml.getAsString())


def circle(corners=32, center=(0,0), radius=(1,1)):
    circle = []
    for i in xrange(corners):
        circle.append((center[0] + radius[0] * sin(2.0 * i/corners * pi), center[1] + radius[1] * cos(2.0 * i/corners * pi)))
    circle.append(circle[0])    # close circle
    return circle
