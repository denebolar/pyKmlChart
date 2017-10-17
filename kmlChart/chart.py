"""
Module to create charts.
"""
from __future__ import absolute_import
from .kmlInterface import KMLdata, Placemark, Polygon
from math import cos, pi, sin
from .colorBars import jet
from kmlChart.kmlInterface import PolyStyle, LineStyle, Folder


def diff(aList):
    """Helper function to compute the differences between elements of a list.
    """
    d = [None] * (len(aList) - 1)
    for i in xrange(len(d)):
        d[i] = aList[i+1] - aList[i]
    return d


def circle(corners=32, center=(0,0), radius=(1,1)):
    """Helper function to compute a circle or an ellipse with N corners.
    """
    circle = []
    for i in xrange(corners):
        circle.append((center[0] + radius[0] * sin(2.0 * i/corners * pi), center[1] + radius[1] * cos(2.0 * i/corners * pi)))
    circle.append(circle[0])    # close circle
    return circle


class chart(object):
    """Abstract base class for charts.
    """
    def __init__(self, title=None, description=None):
        self.kml = KMLdata(name=title, description=description)
        self.title = title

    def save(self, filename):
        """Save the chart as KML file with filename filename.
        """
        with open(filename, 'w') as f:
            f.write(self.kml.getAsString())


class Bar3D(chart):
    """Generate a three-dimensional bar graph.
    """
    def add(self, lon_list, lat_list, z_list, label=None, description=None, colorbar=jet, radius=None,
            relativeToGround=False, display_name='MeasSeries', visibility=True):
        """Add a measurement series to the bar graph. lon_list is a list with N longitudes, lat_list a list with N latitudes,
        and z_list a list of N altitudes. You may specify a custom cylinder radius of radius longitude degrees.
        """
        folder = Folder(name=display_name, visibility=visibility)
        self.kml.add(folder)
        if radius is None:
            try:
                radius = 0.8 * min(filter(lambda x: x > 0, diff(lon_list)))
            except ValueError:
                raise Exception('Radius cannot be determined, please specify one.')
        z_list_noNone = filter(lambda x: x is not None, z_list)
        zaxis = (min(z_list_noNone), max(z_list_noNone))
        for i in xrange(len(lon_list)):
            lat = lat_list[i]
            lon = lon_list[i]
            z   = z_list[i]
            if z is None:
                continue    # equal to NaN, skip this value
            col = _colorbar_color(colorbar, zaxis, z)
            c = circle(center=(lon, lat), radius=(radius / cos(lat), radius))
            if isinstance(label, (list, tuple)): pname = label[i]
            else: pname = label
            if isinstance(description, (list, tuple)): pdesc = description[i]
            else: pdesc = description
            folder.add(
                Placemark(
                    name=pname,
                    description=pdesc,
                    style=[
                        PolyStyle(
                            color='ff%02x%02x%02x' % (col[2], col[1], col[0]),    # attention, color format aabbggrr (alpha, blue, green, red)
                            outline=0,
                        )
                    ]).add(
                        Polygon((i + (z,) for i in c), extrude=True, altitudeMode='relativeToGround' if relativeToGround else 'absolute')
                    )
                )


class Surface(chart):
    """Generate a surface plot.
    """
    def add(self, corner_point_tuple_list, value_list, label=None, description=None, colorbar=jet, border_color=None,
            border_width=1, opacity=0xff, border_opacity=None, display_name='MeasSeries', visibility=True):
        """Add a measurement series to the surface plot. corner_point_tuple_list is a list of polygon corner points of the form
        ((lon1, lat1), (lon2, lat2), ...) with N elements (meaning a list with N polygons described by M points (tuples), consisting
        of two coordinates (lon, lat). Example: [((poly1_lon1, poly1_lat1), (poly1_lon2, poly1_lon2), (poly1_lon3, poly1_lon3)),
        ((poly2_lon1, ...))])
        """
        folder = Folder(name=display_name, visibility=visibility)
        self.kml.add(folder)
        if border_opacity is None:
            border_opacity = opacity
        value_noNone = filter(lambda x: x is not None, value_list)
        zaxis = (min(value_noNone), max(value_noNone))
        for i in xrange(len(value_list)):
            coordinates = corner_point_tuple_list[i]
            z   = value_list[i]
            if z is None:
                continue    # equal to NaN, skip this value
            col = _colorbar_color(colorbar, zaxis, z)
            styles = [
                PolyStyle(
                    color='%02x%02x%02x%02x' % (opacity, col[2], col[1], col[0]),    # attention, color format aabbggrr (alpha, blue, green, red)
                    outline=1 if border_color is not None else 0,
                )
            ]
            if border_color is not None:
                styles.append(
                    LineStyle(
                        color='%02x%02x%02x%02x' % (border_opacity, border_color[2], border_color[1], border_color[0]),
                        width=border_width,
                    )
                )
            if isinstance(label, (list, tuple)): pname = label[i]
            else: pname = label
            if isinstance(description, (list, tuple)): pdesc = description[i]
            else: pdesc = description
            folder.add(
                Placemark(style=styles, name=pname, description=pdesc).add(
                        Polygon(coordinates)
                    )
                )


def _colorbar_color(colorbar, caxis, c):
    caxis = (min(caxis), max(caxis))
    col = int(len(colorbar) * (float(c) - caxis[0]) / (caxis[1] - caxis[0])) if caxis[1] > caxis[0] else 0
    if col < 0:
        col = 0
    if col >= len(colorbar):
        col = len(colorbar) - 1
    return colorbar[col]
