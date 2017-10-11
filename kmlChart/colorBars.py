"""
Module with color bar definitions.
"""

def _inflate_colorbar(cbar, numColors):
    if len(cbar) >= numColors:
        return cbar     # do not reduce color bars
    newBar = [None] * numColors
    step = float(len(cbar) - 1) / (numColors - 1)
    for i in xrange(numColors):
        c_int = int(step * i)
        c_frac = step * i - c_int
        if c_frac < 1e-5:
            newBar[i] = cbar[c_int]
        else:
            newBar[i] = tuple(cbar[c_int][k] * (1 - c_frac) + cbar[c_int + 1][k] * c_frac for k in xrange(len(cbar[c_int])))
    return newBar


jet = _inflate_colorbar((
    (0x00, 0x00, 0x80),
    (0x00, 0x00, 0xff),
    (0x00, 0x80, 0xff),
    (0x00, 0xff, 0xff),
    (0x80, 0xff, 0x80),
    (0xff, 0xff, 0x00),
    (0xff, 0x80, 0x00),
    (0xff, 0x00, 0x00),
    (0x80, 0x00, 0x00),
), 64)


jet2 = _inflate_colorbar((
    (0x00, 0x00, 0x80),
    (0x00, 0x00, 0xff),
    (0x00, 0x80, 0xff),
    (0x00, 0xff, 0xff),
    (0x00, 0xff, 0x80),
    (0x00, 0xff, 0x00),
    (0x80, 0xff, 0x00),
    (0xff, 0xff, 0x00),
    (0xff, 0x80, 0x00),
    (0xff, 0x00, 0x00),
    (0x80, 0x00, 0x00),
), 64)