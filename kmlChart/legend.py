"""
Module to create image legends.
"""
from PIL import Image, ImageDraw, ImageFont
import os.path
from kmlChart.colorBars import jet
from math import log, floor, ceil


class legend(object):
    def __init__(self, caxis, colorbar):
        self.caxis = (min(caxis), max(caxis))
        self.colorbar = colorbar
        self._generateTicks()

    def _generateTicks(self):
        self.ticks = []
        spread = self.caxis[1] - self.caxis[0]
        log_step = log(float(spread), 10) - log(2,10)
        step = 10 ** floor(log_step)
        lowest = ceil(float(self.caxis[0]) / step)
        highest = floor(float(self.caxis[1]) / step)
        for i in xrange(int(highest - lowest) + 1):
            self.ticks.append(((lowest + i) * step, str((lowest + i) * step)))


class pngLegend(legend):
    def __init__(self, caxis, colorbar):
        super(pngLegend, self).__init__(caxis, colorbar)
        self._image = Image.new('RGBA', (200, 400), (0,0,0,0))
        self._font = ImageFont.truetype(os.path.join(os.path.dirname(__file__), '__data__', 'HELR45W.ttf'), 16)
        self._drawLegend()

    def _drawLegend(self):
        canvas = ImageDraw.Draw(self._image)
        canvas.rectangle(((10, 10), (60, 390)), outline=(0xff, 0xff, 0xff, 0xff))
        colorbar = self.colorbar
        tile = float(389-10) / len(colorbar)
        for i in xrange(len(colorbar)):
            canvas.rectangle(((11, 389-int((i+1) * tile)+1), (59, 389-int(i * tile))), fill=colorbar[i] + (0xff,))
        for tick in self.ticks:
            y = int(float(tick[0] - self.caxis[0]) / (self.caxis[1]- self.caxis[0]) * (390-10))
            canvas.line(((60, 390-y), (70, 390-y)), fill=(0xff, 0xff, 0xff, 0xff))
            canvas.text((80-1, 390-y-10), tick[1], font=self._font, fill=(0x00, 0x00, 0x00, 0xff))   # RGBA
            canvas.text((80, 390-y-10-1), tick[1], font=self._font, fill=(0x00, 0x00, 0x00, 0xff))   # RGBA
            canvas.text((80, 390-y-10+1), tick[1], font=self._font, fill=(0x00, 0x00, 0x00, 0xff))   # RGBA
            canvas.text((80+1, 390-y-10), tick[1], font=self._font, fill=(0x00, 0x00, 0x00, 0xff))   # RGBA
            canvas.text((80, 390-y-10), tick[1], font=self._font, fill=(0xff, 0xff, 0xff, 0xff))   # RGBA


    def save(self, filename):
        with open(filename, 'w') as f:
            self._image.save(f, format='PNG')
