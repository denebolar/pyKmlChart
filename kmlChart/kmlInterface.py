"""
Interface to produce files.
"""

from xml.etree import ElementTree
from argparse import ArgumentTypeError


# Register XML name spaces
namespaces = {
    '': 'http://www.opengis.net/kml/2.2',
    'gx': 'http://www.google.com/kml/ext/2.2',
    'atom': 'http://www.w3.org/2005/Atom',
    'xal': 'urn:oasis:names:tc:ciq:xsdschema:xAL:2.0',
}

for prefix, namespace in namespaces.iteritems():
    ElementTree.register_namespace(prefix, namespace)


def prefixedTag(tag):
    prefix = ''
    if ':' in tag:
        prefix, tag = tag.split(':', 1)
    return '{%s}%s' % (namespaces[prefix], tag)


class StyleData(object):
    def __init__(self):
        """Class to hold style information.
        """
        self.styles = {}

    def addStyle(self, name, listOfStyles):
        self.styles[name] = listOfStyles

    def renderStyles(self, documentNode):
        for name, listOfStyles in self.styles.iteritems():
            if not isinstance(listOfStyles, (list, tuple)):
                listOfStyles = [listOfStyles]
            xmlStyle = ElementTree.SubElement(documentNode, 'Style', id=name)
            for style in listOfStyles:
                _styleRenderer(xmlStyle, style)


class ShapeInterface(object):
    def __init__(self):
        self.shapes = []

    def mayBeAddedTo(self, instance):
        return True

    def add(self, shapeElement):
        if not isinstance(shapeElement, ShapeInterface):
            raise TypeError('Can only add elements of type ShapeInterface.')
        if not shapeElement.mayBeAddedTo(self):
            raise ValueError('This shape does not accept to be added to this instance.');
        self.shapes.append(shapeElement)
        return self     # enable chaining

    def render(self, xmlParent):
        for shape in self.shapes:
            shape.render(xmlParent)


class AbstractShape(ShapeInterface):
    TAG = 'ABSTRACT'

    def __init__(self, shapeID=None, style=None, settings={}):
        ShapeInterface.__init__(self)
        self.shapeID = shapeID
        self.style = style
        self.settings = settings

    def renderNode(self, xml):
        pass

    def render(self, xmlParent):
        xml = ElementTree.SubElement(xmlParent, self.TAG)
        if self.shapeID is not None:
            xml.attrib['id'] = self.shapeID
        if isinstance(self.style, (str, unicode)):
            ElementTree.SubElement(xml, 'styleUrl').text = self.styleURL
        if isinstance(self.style, (list, tuple)):
            styleXml = ElementTree.SubElement(xml, 'Style')
            for style in self.style:
                _styleRenderer(styleXml, style)
        _renderDict(xml, self.settings)
        self.renderNode(xml)
        ShapeInterface.render(self, xml)


class LineString(object):
    TAG = 'LineString'

    def __init__(self, coordinateTuples):
        self.coordinates = []
        for tup in coordinateTuples:
            if isinstance(tup, (tuple, list)) and len(tup) in (2, 3):
                self.coordinates.append(tup)
            else:
                raise ValueError('Tuple %s is no valid coordinate tuple.' % str(tup))

    def render(self, xmlParent):
        xml = ElementTree.SubElement(xmlParent, self.TAG)
        ElementTree.SubElement(xml, 'coordinates').text = ' '.join([','.join((str(value) for value in tup)) for tup in self.coordinates])


class LinearRing(LineString):
    TAG = 'LinearRing'


class Polygon(AbstractShape):
    TAG = 'Polygon'

    def __init__(self, coordinateTuples, altitudeMode=None, extrude=False, shapeID=None):
        AbstractShape.__init__(self, shapeID=shapeID)
        if altitudeMode is not None:
            _validators['altitudeModeEnum'](altitudeMode)
        self.settings = {
            'altitudeMode': altitudeMode,
            #'tesselate': 1 if tesselate else 0,    ignored by Polygon tag
            'extrude': 1 if extrude else 0,
        }
        self.outerBoundaryIs = LinearRing(coordinateTuples)
        self.innerBoundaryIs = []

    def mayBeAddedTo(self, instance):
        return (instance.__class__ == MultiGeometry) or ((instance.__class__ == Placemark) and len(instance.shapes) < 1)

    def addInnerBoundary(self, coordinateTuples):
        self.innerBoundaryIs.append(LinearRing(coordinateTuples))

    def renderNode(self, xml):
        self.outerBoundaryIs.render(ElementTree.SubElement(xml, 'outerBoundaryIs'))
        for item in self.innerBoundaryIs:
            item.render(ElementTree.SubElement(xml, 'innerBoundaryIs'))


class MultiGeometry(AbstractShape):
    TAG = 'MultiGeometry'

    def mayBeAddedTo(self, instance):
        return (instance.__class__ == MultiGeometry) or ((instance.__class__ == Placemark) and len(instance.shapes) < 1)


class Placemark(AbstractShape):
    TAG = 'Placemark'

    def __init__(self, name=None, visibility=True, open=False, description=None, shapeID=None, style=None):
        AbstractShape.__init__(self, shapeID=shapeID, style=style)
        self.settings = {
            'name': name,
            'visibility': 1 if visibility else 0,
            'open': 1 if open else 0,
            'description': description,
        }

    def mayBeAddedTo(self, instance):
        return instance.__class__ in (KMLdata, Folder)


class Folder(Placemark):
    TAG = 'Folder'

    def mayBeAddedTo(self, instance):
        return instance.__class__ == KMLdata


class ScreenOverlay(AbstractShape):
    def __init__(self, href, name=None, description=None, shapeID=None):
        AbstractShape.__init__(self, shapeID=shapeID)
        self.settings = {
            'name': name,
            'description': description,
        }


class KMLdata(ShapeInterface):
    def __init__(self, styles=None, name=None, description=None, visibility=True):
        """Class to produce the actual KML output.
        """
        super(KMLdata, self).__init__()
        self.styles = styles or StyleData()
        self.settings = {
            'name': name,
            'open': 0,
            'visibility': 1 if visibility else 0,
            'description': description,
        }

    def getAsString(self):
        root = ElementTree.Element(prefixedTag('kml'))
        document = ElementTree.SubElement(root, prefixedTag('Document'))
        _renderDict(document, self.settings)
        self.styles.renderStyles(document)
        self.render(document)
        return '<?xml version="1.0" encoding="UTF-8"?>\n' + \
            ElementTree.tostring(root, encoding='utf-8')

#===============================================================================
# <?xml version="1.0" encoding="UTF-8"?>
# <kml xmlns="http://www.opengis.net/kml/2.2">
# <Document>
#   <name>Document.kml</name>
#   <open>1</open>
#   <Style id="exampleStyleDocument">
#     <LabelStyle>
#       <color>ff0000cc</color>
#     </LabelStyle>
#   </Style>
#   <Placemark>
#     <name>Document Feature 1</name>
#     <styleUrl>#exampleStyleDocument</styleUrl>
#     <Point>
#       <coordinates>-122.371,37.816,0</coordinates>
#     </Point>
#   </Placemark>
#   <Placemark>
#     <name>Document Feature 2</name>
#     <styleUrl>#exampleStyleDocument</styleUrl>
#     <Point>
#       <coordinates>-122.370,37.817,0</coordinates>
#     </Point>
#   </Placemark>
# </Document>
# </kml>
#===============================================================================



def _generateStruct(name, *args, **kwargs):
    validators = kwargs.pop('validators', {})
    elements = {}
    elements.update(((name, None) for name in args))
    elements.update(((name, value) for name, value in kwargs.iteritems()))
    def validator(self, name, value):
        if name in validators:
            if validators[name](value) is False:
                raise ValueError('Invalid value for field %s.' % name)
        object.__setattr__(self, name, value)
    def initializer(self, **kwargs):
        for name, value in kwargs.iteritems():
            setattr(self, name, value)
    elements.update({
        '_keys': elements.keys(),
        '__setattr__': validator,
        '__init__': initializer,
        '__setitem__': validator,
        '__getitem__': object.__getattribute__,
    })
    return type(name, (), elements)


def _validatorStr(minLen=None, maxLen=None, exactLen=None):
    def validator(value):
        if not isinstance(value, (str, unicode)):
            raise ValueError('Value is no string.')
        if (exactLen is not None) and (len(value) != exactLen):
            raise ValueError('String must have an exact length of %d characters.' % exactLen)
        if (minLen is not None) and (len(value) < minLen):
            raise ValueError('String must have a length of at least %d characters.' % minLen)
        if (maxLen is not None) and (len(value) < maxLen):
            raise ValueError('String must have a maximum length of %d characters.' % maxLen)
        return True
    return validator


def _validatorChoice(*args):
    def validator(value):
        if value not in args:
            raise ValueError('Value must be either %s.' % ', '.join(args))
        return True
    return validator


# Google Earth KML types
_validators = {
    'altitudeModeEnum': _validatorChoice('clampToGround', 'relativeToGround', 'absolute'),
    'angle90': lambda angle: (angle >= -90) and (angle <= 90),
    'anglepos90': lambda angle: (angle >= 0) and (angle <= 90),
    'angle180': lambda angle: (angle >= -180) and (angle <= 180),
    'angle360': lambda angle: (angle >= -360) and (angle <= 360),
    'color': _validatorStr(exactLen=8),
    'colorModeEnum': _validatorChoice('normal', 'random'),
    'displayModeEnum': _validatorChoice('default', 'hide'),
    'gridOrigin': _validatorChoice('lowerLeft', 'upperLeft'),
    'shapeEnum': _validatorChoice('rectangle', 'cylinder', 'sphere'),
    'styleStateEnum': _validatorChoice('normal', 'highlight'),
    'unitsEnum': _validatorChoice('fraction', 'pixels', 'insetPixels'),
    'numBoolean': _validatorChoice(0, 1),
}


BalloonStyle = _generateStruct('BalloonStyle', 'bgColor', 'textColor', 'text', 'displayMode',
   validators={
       'bgColor': _validators['color'],
       'textColor': _validators['color'],
       'displayMode': _validators['displayModeEnum'],
   })


LineStyle = _generateStruct('LineStyle', 'color', 'gx:outerColor', 'gx:outerWidth', 'gx:physicalWidth', 'gx:labelVisibility',
   colorMode='normal', width=1,
   validators={
       'color': _validators['color'],
       'colorMode': _validators['colorModeEnum'],
       'gx:outerColor': _validators['color'],
       'gx:labelVisibility': _validators['numBoolean'],
   })


PolyStyle = _generateStruct('PolyStyle', 'color', colorMode='normal', fill=1, outline=1,
   validators={
       'color': _validators['color'],
       'colorMode': _validators['colorModeEnum'],
       'fill': _validators['numBoolean'],
       'outline': _validators['numBoolean'],
   })


def _simpleStyleRenderer(xmlNode, style, fields=[]):
    if len(fields) == 0:
        fields = style._keys
    for field in fields:
        if style[field] is not None:
            ElementTree.SubElement(xmlNode, field).text = str(style[field])


def _styleRenderer(xmlParent, style, styleID=None):
    attrib = {}
    if styleID is not None:
        attrib['id'] = styleID
    xmlNode = ElementTree.Element(style.__class__.__name__, attrib)

    try:
        {
            'PolyStyle': _simpleStyleRenderer,
            'BalloonStyle': _simpleStyleRenderer,
            'LineStyle': _simpleStyleRenderer,
        }[style.__class__.__name__](xmlNode, style)
    except KeyError as e:
        raise TypeError('Invalid style class: ' + e.message);

    xmlParent.append(xmlNode)


def _renderDict(xmlParent, aDict):
    for key, value in aDict.iteritems():
        if value is None:
            continue
        xml = ElementTree.SubElement(xmlParent, key)
        if isinstance(value, dict):
            _renderDict(xml, value)
        else:
            xml.text = str(value)



def _renderer(xmlParent, key, element):
    xml = ElementTree.Element(key)
    if isinstance(element, dict):
        for key, value in element.iteritems():
            _renderer(xml, key, value)
        xmlParent.append(xml)

    elif isinstance(element, list):
        for item in element:
            _renderer(xmlParent, key, item)

    elif element is not None:
        xml.text = str(element)
        xmlParent.append(xml)
