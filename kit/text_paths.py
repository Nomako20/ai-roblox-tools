"""Text -> SVG paths (Lilita One), drawn exactly like the snow-button labels:
shadow copy + thick outline + white fill. Looks identical on any machine, no font needed."""
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

import os
FONT_PATH = os.environ.get('UIKIT_FONT', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts', 'LilitaOne-Regular.ttf'))
_font = TTFont(FONT_PATH)
_gs = _font.getGlyphSet()
_cmap = _font.getBestCmap()
_upm = _font['head'].unitsPerEm
_hmtx = _font['hmtx']
_kern = {}
if 'kern' in _font:
    for t in _font['kern'].kernTables:
        _kern.update(t.kernTable)

def width(s, size):
    sc = size / _upm
    w, prev = 0, None
    for ch in s:
        g = _cmap.get(ord(ch))
        if not g:
            w += size * 0.3; prev = None; continue
        if prev:
            w += _kern.get((prev, g), 0) * sc
        w += _hmtx[g][0] * sc
        prev = g
    return w

def path(s, x, y, size, anchor='middle', track=0.02):
    sc = size / _upm
    tw = width(s, size) + track * size * (len(s) - 1)
    x0 = x - tw / 2 if anchor == 'middle' else (x - tw if anchor == 'end' else x)
    pen = SVGPathPen(_gs)
    cx, prev = x0, None
    for ch in s:
        g = _cmap.get(ord(ch))
        if not g:
            cx += size * 0.3; prev = None; continue
        if prev:
            cx += _kern.get((prev, g), 0) * sc
        tp = TransformPen(pen, (sc, 0, 0, -sc, cx, y))
        _gs[g].draw(tp)
        cx += _hmtx[g][0] * sc + track * size
        prev = g
    return pen.getCommands()

def label(x, y, s, size, fill='#FFFFFF', outline='#0F2E4F', anchor='middle', name=None, rot=0, ow=None):
    """same recipe as the buttons: outline = size/4.5, shadow offset = size/14 + 1"""
    d = path(s, x, y, size, anchor)
    sw = ow or max(4, round(size / 4.5))
    dy = round(size / 14) + 1
    tr = f' transform="rotate({rot} {x:.1f} {y - size * 0.35:.1f})"' if rot else ''
    return (f'<g id="{name or "Text " + s}"{tr}>'
            f'<path d="{d}" transform="translate(0 {dy})" fill="{outline}" stroke="{outline}" stroke-width="{sw}" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="{outline}" stroke="{outline}" stroke-width="{sw}" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="{fill}"/></g>')

def set_font(path):
    """switch the font used by width()/path()/label() (e.g. kit/fonts/FredokaBold.ttf for the Roblox-flat style)"""
    global _font, _gs, _cmap, _upm, _hmtx, _kern
    _font = TTFont(path); _gs = _font.getGlyphSet(); _cmap = _font.getBestCmap()
    _upm = _font['head'].unitsPerEm; _hmtx = _font['hmtx']; _kern = {}
    if 'kern' in _font:
        for t in _font['kern'].kernTables:
            _kern.update(t.kernTable)
