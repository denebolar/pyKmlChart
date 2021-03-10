"""
Unit test cases to cover the module TransversalMercator.
"""
from __future__ import print_function
import unittest
from kmlChart.TransversalMercator import BESSEL, lla2tm, tm2lla, WGS84
from kmlChart.ECEF import lla2ecef, applyHelmert, WGS84toDHDN_Potsdam, ecef2lla,\
    DHDN_PotsdamToWGS84
from math import pi


class GeodesyTest(unittest.TestCase):
    def test_lla2tm(self):
        lla = (51.0/180*pi, 10.0/180*pi, 0)   # 51deg. north, 10deg. east, GK 3570272.656m, 5652121.859m (Bessel ellipsoid)
        ecef = lla2ecef(lla, **WGS84)
        print('ECEF vor Helmert:', ecef)
        ecef = applyHelmert(ecef, **WGS84toDHDN_Potsdam)
        print('ECEF nach Helmert:', ecef)
        lla = ecef2lla(ecef, **BESSEL)
        print('LLA nach Helmert:', lla[0]/pi*180, lla[1]/pi*180, lla[2])
        gk = (3570272.656, 5652121.859)
        ref = int(gk[0]/1e6)  # reference meridian
        ll4tm = (lla[0], lla[1] - ref*3.0/180*pi)
        tm = (gk[0] - ref*1e6 - 500e3, gk[1])
        (R, H) = lla2tm(ll4tm[0], ll4tm[1], **BESSEL)
        print('lla2tm(%f,%f) = %f,%f (should be %f,%f)' % (ll4tm[0]/pi*180, ll4tm[1]/pi*180, R, H, tm[0], tm[1]))
        llFromTM = tm2lla(R, H, **BESSEL)
        print('tm2lla(%f,%f) = %f,%f (should be %f,%f)' % (R, H, llFromTM[0]/pi*180, llFromTM[1]/pi*180, ll4tm[0]/pi*180, ll4tm[1]/pi*180))
        llaFromTM = (llFromTM[0], llFromTM[1] + ref*3.0/180*pi, lla[2])
        ecefFromTM = lla2ecef(llaFromTM, **BESSEL)
        ecefFromTM = applyHelmert(ecefFromTM, **DHDN_PotsdamToWGS84)
        llaFromTM = ecef2lla(ecefFromTM, **WGS84)
        print('llaFromTM: %f,%f,%f' % (llaFromTM[0]/pi*180, llaFromTM[1]/pi*180, llaFromTM[2]))
        #self.assertAlmostEqual(R, tm[0], delta=2.1)
        #self.assertAlmostEqual(H, tm[1])
