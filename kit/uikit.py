"""uikit - the shared drawing kit for every screen in this skill.

One Doc collects <defs> and parts; every primitive returns an SVG string.
Everything follows references/style-anatomy.md: dark outline, rim, 3D bottom edge,
hard two-tone face, gloss swooshes, text with outline + hard shadow.

    from uikit import *
    d = Doc(1280, 720, bg=('#2B1650', '#120726'))
    d.add(button(d, 100, 100, 320, 92, PAL['green'], 'PLAY', icon='play'))
    d.save('out.svg'); render('out.svg', 'out.png')
"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import text_paths as TP

def f(v):
    return f'{v:.1f}'.rstrip('0').rstrip('.')

# role palettes: a = light top, b = saturated bottom, d = 3D edge, t = outline / text outline
PAL = {
    'green':  dict(a='#9BFF5A', b='#33D12B', d='#1F9A1E', t='#13541A'),
    'red':    dict(a='#FF8A8A', b='#F2363F', d='#B5182A', t='#5E0A17'),
    'blue':   dict(a='#8FE0FF', b='#2C9BF5', d='#1A68C2', t='#0B356E'),
    'purple': dict(a='#E19BFF', b='#A23CF0', d='#7020B8', t='#33105E'),
    'gold':   dict(a='#FFF27A', b='#FFB800', d='#D97A00', t='#6B3300'),
    'orange': dict(a='#FFC56B', b='#FF7A1A', d='#D2500B', t='#5E2100'),
    'pink':   dict(a='#FFB3E6', b='#FF4FB8', d='#CF2A8C', t='#5C0B3D'),
    'cyan':   dict(a='#9FFFF4', b='#18D8D0', d='#0E9E9F', t='#064A4E'),
    'grey':   dict(a='#E9EEF5', b='#AEB9C9', d='#7A879B', t='#2A3344'),
    'dark':   dict(a='#4A4F6B', b='#2A2D45', d='#181A2C', t='#07080F'),
}
# rarity -> palette key (common..mythic). Rainbow handled by rainbow_fill().
RARITY = {'Common': 'grey', 'Uncommon': 'green', 'Rare': 'blue', 'Epic': 'purple',
          'Legendary': 'gold', 'Mythic': 'red', 'Secret': 'dark'}
NAVY = '#14213D'

class Doc:
    def __init__(self, W, H, bg=None, seed=7):
        self.W, self.H, self.defs, self.parts, self._n = W, H, [], [], 0
        self.rng = random.Random(seed)
        if bg:
            g = self.lin([(0, bg[0]), (1, bg[1])])
            self.parts.append(f'<rect width="{W}" height="{H}" fill="{g}"/>')

    def uid(self, p='g'):
        self._n += 1
        return f'{p}{self._n}'

    def lin(self, stops, x2=0, y2=1, x1=0, y1=0):
        i = self.uid('L')
        s = ''.join(f'<stop offset="{o}" stop-color="{c}"/>' if len(c) <= 7 else
                    f'<stop offset="{o}" stop-color="{c[:7]}" stop-opacity="{int(c[7:9], 16) / 255:.2f}"/>' for o, c in stops)
        self.defs.append(f'<linearGradient id="{i}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{s}</linearGradient>')
        return f'url(#{i})'

    def rad(self, stops, cx=.5, cy=.5, r=.5):
        i = self.uid('R')
        s = ''.join(f'<stop offset="{o}" stop-color="{c[:7]}" stop-opacity="{(int(c[7:9], 16) / 255 if len(c) > 7 else 1):.2f}"/>' for o, c in stops)
        self.defs.append(f'<radialGradient id="{i}" cx="{cx}" cy="{cy}" r="{r}">{s}</radialGradient>')
        return f'url(#{i})'

    def clip(self, shape):
        i = self.uid('C')
        self.defs.append(f'<clipPath id="{i}">{shape}</clipPath>')
        return f'url(#{i})'

    def two_tone(self, p, split=.54):
        return self.lin([(0, p['a']), (split, p['a']), (split, p['b']), (1, p['b'])])

    def add(self, *s):
        self.parts.extend(s)

    def svg(self):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.W}" height="{self.H}" viewBox="0 0 {self.W} {self.H}">'
                f'<defs>{"".join(self.defs)}</defs>{"".join(self.parts)}</svg>')

    def save(self, path):
        open(path, 'w', encoding='utf-8').write(self.svg())
        return path

def render(svg_path, png_path, scale=1):
    """SVG -> PNG with the installed Edge/Chrome through Playwright (no extra downloads)."""
    from playwright.sync_api import sync_playwright
    src = open(svg_path, encoding='utf-8').read()
    import re
    W, H = (int(float(v)) for v in re.search(r'width="([\d.]+)" height="([\d.]+)"', src).groups())
    with sync_playwright() as p:
        for ch in ('msedge', 'chrome', None):
            try:
                b = p.chromium.launch(channel=ch) if ch else p.chromium.launch()
                break
            except Exception:
                continue
        pg = b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=scale)
        pg.set_content(f'<html><body style="margin:0;background:transparent">{src}</body></html>')
        pg.screenshot(path=png_path, omit_background=True)
        b.close()
    return png_path

# ---------- text ----------
def T(x, y, s, size, fill='#FFFFFF', outline=NAVY, anchor='middle', rot=0, name=None, ow=None):
    return TP.label(x, y, s, size, fill=fill, outline=outline, anchor=anchor, name=name, rot=rot, ow=ow)

def text_w(s, size):
    return TP.width(s, size) + 0.02 * size * (len(s) - 1)

def fit(s, size, maxw):
    """largest size <= size that fits maxw"""
    while size > 10 and text_w(s, size) > maxw:
        size -= 1
    return size

# ---------- surfaces ----------
def rr(x, y, w, h, r):
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(r)}"/>'

def surface(d, x, y, w, h, p, r=None, rim=5, edge=None, rim_cols=('#FFFFFF', None), texture=None,
            gloss=True, sw=5, shadow=True, name='Surface'):
    """The stack every button / card / plaque uses. texture: None|'dots'|'stripes'|'rays'."""
    r = min(h * .3, 28) if r is None else r
    edge = max(4, round(h * .075)) if edge is None else edge
    rim_g = d.lin([(0, rim_cols[0]), (1, rim_cols[1] or p['a'])])
    fx, fy, fw, fh = x + rim, y + rim, w - 2 * rim, h - 2 * rim
    fr = max(4, r - rim)
    o = [f'<g id="{name}">']
    if shadow:
        o.append(f'<rect x="{f(x)}" y="{f(y + 8)}" width="{f(w)}" height="{f(h)}" rx="{f(r)}" fill="{p["t"]}" fill-opacity=".45"/>')
    o.append(f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(r)}" fill="{rim_g}" stroke="{p["t"]}" stroke-width="{sw}"/>')
    o.append(f'<rect x="{f(fx)}" y="{f(fy)}" width="{f(fw)}" height="{f(fh)}" rx="{f(fr)}" fill="{p["d"]}"/>')
    o.append(f'<rect x="{f(fx)}" y="{f(fy)}" width="{f(fw)}" height="{f(fh - edge)}" rx="{f(fr)}" fill="{d.two_tone(p)}"/>')
    if texture:
        cp = d.clip(rr(fx, fy, fw, fh - edge, fr))
        o.append(f'<g clip-path="{cp}">{_texture(d, texture, fx, fy, fw, fh - edge)}</g>')
    o.append(f'<rect x="{f(fx)}" y="{f(fy)}" width="{f(fw)}" height="{f(fh)}" rx="{f(fr)}" fill="none" stroke="{p["t"]}" stroke-opacity=".35" stroke-width="2"/>')
    if gloss:
        o.append(gloss_marks(fx, fy, fw, fh - edge, fr))
    o.append('</g>')
    return ''.join(o)

def gloss_marks(x, y, w, h, r):
    k = min(r, h * .45)
    a = (f'<path d="M{f(x + 7)} {f(y + h * .55)} Q{f(x + 7)} {f(y + 7)} {f(x + min(w * .3, k * 2.4))} {f(y + 7)}" '
         f'fill="none" stroke="#FFFFFF" stroke-width="{f(min(7, max(3, h * .07)))}" stroke-linecap="round" stroke-opacity=".9"/>')
    b = (f'<path d="M{f(x + w - 8)} {f(y + h * .62)} Q{f(x + w - 8)} {f(y + h - 7)} {f(x + w - min(w * .16, k * 1.4))} {f(y + h - 7)}" '
         f'fill="none" stroke="#FFFFFF" stroke-width="{f(min(5.5, max(2.5, h * .055)))}" stroke-linecap="round" stroke-opacity=".7"/>')
    dot = f'<circle cx="{f(x + min(w * .3, k * 2.4) + 9)}" cy="{f(y + 7)}" r="{f(min(4.5, max(2, h * .035)))}" fill="#FFFFFF" fill-opacity=".9"/>'
    return a + b + dot

def _texture(d, kind, x, y, w, h):
    o = []
    if kind == 'dots':
        step = 13
        for i in range(int(w / step) + 2):
            for j in range(int(h / step) + 2):
                cx, cy = x + w - i * step, y + j * step
                t = 1 - (i * step / w * .8 + j * step / h * .6)
                if t > 0:
                    o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(4.2 * t)}" fill="#FFFFFF" fill-opacity=".22"/>')
    elif kind == 'stripes':
        for i in range(-int(h / 26) - 2, int(w / 26) + 2):
            sx = x + i * 26
            o.append(f'<path d="M{f(sx)} {f(y + h)} L{f(sx + h)} {f(y)} L{f(sx + h + 12)} {f(y)} L{f(sx + 12)} {f(y + h)} Z" fill="#FFFFFF" fill-opacity=".14"/>')
    elif kind == 'rays':
        o.append(sunburst(x + w / 2, y + h * .45, max(w, h), 18, '#FFFFFF', .2))
    return ''.join(o)

def rainbow(d):
    return d.lin([(0, '#FF4D6D'), (.2, '#FFB020'), (.4, '#FFF04A'), (.6, '#3EE07A'), (.8, '#2FA8FF'), (1, '#B24DFF')], x2=1, y2=0)

# ---------- glyphs (24x24 grid) ----------
GLY = {
    'star': 'M12 2 L14.9 8.6 L22 9.3 L16.6 14 L18.2 21 L12 17.3 L5.8 21 L7.4 14 L2 9.3 L9.1 8.6 Z',
    'bolt': 'M13 2 L4 14 H11 L10 22 L20 9 H13 Z',
    'play': 'M7 4 L20 12 L7 20 Z',
    'plus': 'M9.5 3 H14.5 V9.5 H21 V14.5 H14.5 V21 H9.5 V14.5 H3 V9.5 H9.5 Z',
    'x': 'M5 8.5 L8.5 5 L12 8.5 L15.5 5 L19 8.5 L15.5 12 L19 15.5 L15.5 19 L12 15.5 L8.5 19 L5 15.5 L8.5 12 Z',
    'check': 'M3 12.5 L6.5 9 L10 12.5 L17.5 5 L21 8.5 L10 19.5 Z',
    'gift': 'M3 9 H21 V13 H3 Z M4.5 13 H19.5 V21 H4.5 Z M10.5 9 H13.5 V21 H10.5 Z M12 9 C9 3 4.5 5 7 8.5 Z M12 9 C15 3 19.5 5 17 8.5 Z',
    'cart': 'M2 4 H5.5 L8 15 H18.5 L21 7 H7 M9 19 A1.8 1.8 0 1 0 9 19.1 M17 19 A1.8 1.8 0 1 0 17 19.1',
    'crown': 'M3 8 L8 12 L12 4 L16 12 L21 8 L19 19 H5 Z',
    'clock': 'M12 2.5 A9.5 9.5 0 1 0 12 21.5 A9.5 9.5 0 1 0 12 2.5 Z M11 6 H13 V11.2 L16.5 13.5 L15.4 15.2 L11 12.4 Z',
    'gear': 'M10 2 H14 L14.6 5 L17.3 6.2 L19.8 4.4 L21.6 7.5 L19.4 9.6 V14.4 L21.6 16.5 L19.8 19.6 L17.3 17.8 L14.6 19 L14 22 H10 L9.4 19 L6.7 17.8 L4.2 19.6 L2.4 16.5 L4.6 14.4 V9.6 L2.4 7.5 L4.2 4.4 L6.7 6.2 L9.4 5 Z M12 8.5 A3.5 3.5 0 1 0 12 15.5 A3.5 3.5 0 1 0 12 8.5 Z',
    'bag': 'M5 8 H19 L20 21 H4 Z M8.5 8 V6.5 A3.5 3.5 0 0 1 15.5 6.5 V8',
    'trophy': 'M7 3 H17 V9 A5 5 0 0 1 7 9 Z M7 5 H3.5 A3.5 3.5 0 0 0 7 10.5 M17 5 H20.5 A3.5 3.5 0 0 1 17 10.5 M10.5 13.5 H13.5 V17 H10.5 Z M7.5 17 H16.5 V21 H7.5 Z',
    'lock': 'M5 10.5 H19 V21 H5 Z M8 10.5 V7.5 A4 4 0 0 1 16 7.5 V10.5',
    'paw': 'M12 12 C8 12 5.5 15.5 6.5 18.5 C7.4 21 10 20.5 12 20.5 C14 20.5 16.6 21 17.5 18.5 C18.5 15.5 16 12 12 12 Z M5.5 8 A2.2 2.6 0 1 0 5.5 13.2 A2.2 2.6 0 1 0 5.5 8 Z M18.5 8 A2.2 2.6 0 1 0 18.5 13.2 A2.2 2.6 0 1 0 18.5 8 Z M9.2 3.5 A2.3 2.7 0 1 0 9.2 8.9 A2.3 2.7 0 1 0 9.2 3.5 Z M14.8 3.5 A2.3 2.7 0 1 0 14.8 8.9 A2.3 2.7 0 1 0 14.8 3.5 Z',
    'sword': 'M19.5 2.5 L21.5 4.5 L10 16 L8 14 Z M5 13 L11 19 L9.5 20.5 L7.5 18.5 L4.5 21.5 L2.5 19.5 L5.5 16.5 L3.5 14.5 Z',
    'heart': 'M12 21 L3.5 12.5 A5 5 0 0 1 12 6 A5 5 0 0 1 20.5 12.5 Z',
    'trade': 'M3 8 H16 V4.5 L21 9.5 L16 14.5 V11 H3 Z M21 16 H8 V19.5 L3 14.5 L8 9.5 V13 H21 Z',
    'map': 'M2 5 L8 3 L16 6 L22 4 V19 L16 21 L8 18 L2 20 Z',
    'calendar': 'M3 5 H21 V21 H3 Z M3 5 H21 V9.5 H3 Z M7 2.5 V7 M17 2.5 V7',
    'egg': 'M12 2.5 C7.5 2.5 4.5 10 4.5 14.5 A7.5 7.5 0 0 0 19.5 14.5 C19.5 10 16.5 2.5 12 2.5 Z',
    'shield': 'M12 2 L20 5 V11 C20 16.5 16.5 20 12 22 C7.5 20 4 16.5 4 11 V5 Z',
    'potion': 'M9.5 2.5 H14.5 V5 H13.5 V8.5 A7 7 0 1 1 10.5 8.5 V5 H9.5 Z',
    'quest': 'M5 3 H17 A2 2 0 0 1 19 5 V21 H7 A2 2 0 0 1 5 19 Z M9 8 H15 M9 12 H15 M9 16 H13',
}

def glyph(name, cx, cy, s, fill='#FFFFFF', stroke=NAVY, sw=3.2):
    return (f'<g transform="translate({f(cx - 12 * s)} {f(cy - 12 * s)}) scale({f(s)})">'
            f'<path d="{GLY[name]}" fill="{fill}" stroke="{stroke}" stroke-width="{f(sw / s * s / s if False else sw / s)}" stroke-linejoin="round" stroke-linecap="round"/></g>')

def glyph3d(name, cx, cy, s, fill='#FFFFFF', stroke=NAVY):
    """glyph with a hard drop shadow in the outline colour - reads as an object, not a line icon"""
    return glyph(name, cx, cy + 2.5 * s / 1.6, s, stroke, stroke, 4.4) + glyph(name, cx, cy, s, fill, stroke, 3.6)

# ---------- composite widgets ----------
def button(d, x, y, w, h, p, label, icon=None, size=None, texture=None, rot=0, **kw):
    o = [surface(d, x, y, w, h, p, texture=texture, name='Button ' + label, **kw)]
    edge = max(4, round(h * .075))
    cy = y + (h - edge) / 2
    lx0 = x + 14
    if icon:
        br = h * .27
        bx = x + 14 + br + 4
        o.append(f'<circle cx="{f(bx)}" cy="{f(cy)}" r="{f(br)}" fill="{p["d"]}" stroke="{p["t"]}" stroke-width="3.5"/>')
        o.append(glyph3d(icon, bx, cy, br / 15, '#FFFFFF', p['t']))
        lx0 = bx + br + 4
    size = size or fit(label, h * .44, x + w - 18 - lx0)
    o.append(T((lx0 + x + w - 14) / 2, cy + size * .36, label, size, outline=p['t'], rot=rot))
    return ''.join(o)

def icon_button(d, x, y, s, p, icon, badge=None):
    o = [surface(d, x, y, s, s, p, r=s * .26, rim=4, name='IconButton ' + icon)]
    edge = max(4, round(s * .075))
    o.append(glyph3d(icon, x + s / 2, y + (s - edge) / 2, s / 42, '#FFFFFF', p['t']))
    if badge:
        o.append(notif_dot(x + s - 6, y + 6, badge))
    return ''.join(o)

def notif_dot(cx, cy, txt, p=None):
    p = p or PAL['red']
    return (f'<circle cx="{f(cx)}" cy="{f(cy)}" r="15" fill="{p["b"]}" stroke="{p["t"]}" stroke-width="3.5"/>'
            + T(cx, cy + 6.5, str(txt), 18, outline=p['t']))

def robux(x, y, s=1.0, col='#FFFFFF', stroke=NAVY):
    def hexp(r):
        return ' '.join(('M' if k == 0 else 'L') + f'{12 + r * math.cos(math.radians(-90 + 60 * k)):.2f} {12 + r * math.sin(math.radians(-90 + 60 * k)):.2f}' for k in range(6)) + ' Z'
    return (f'<g id="Robux" transform="translate({f(x)} {f(y)}) scale({f(s)})">'
            f'<path d="{hexp(11.2)} {hexp(6.6)}" fill="{col}" fill-rule="evenodd" stroke="{stroke}" stroke-width="2.6" stroke-linejoin="round"/>'
            f'<rect x="9.4" y="9.4" width="5.2" height="5.2" rx="1" fill="{col}" stroke="{stroke}" stroke-width="2.2"/></g>')

def price(d, x, y, w, h, amount, p=None, old=None, currency='robux', old_left=False):
    """price pill: green two-tone, Robux mark + value; old = crossed-out price above it"""
    p = p or PAL['green']
    o = [surface(d, x, y, w, h, p, r=h * .34, rim=3.5, edge=max(3, h * .1), sw=4, name='Price ' + str(amount))]
    size = fit(str(amount), h * .5, w - h * 1.3)
    tw = text_w(str(amount), size)
    gx = x + w / 2 - (tw + h * .62) / 2
    cy = y + (h - max(3, h * .1)) / 2
    if currency == 'robux':
        o.append(robux(gx, cy - h * .3, h * .025 * 1.05, '#FFFFFF', p['t']))
    elif currency == 'gem':
        o.append(gem(gx + h * .3, cy + h * .03, h * .28))
    else:
        o.append(coin(gx + h * .3, cy, h * .27))
    o.append(T(gx + h * .62 + tw / 2, cy + size * .36, str(amount), size, outline=p['t']))
    if old:
        s2 = h * .4
        ox, oy = (x - text_w(str(old), s2) / 2 - 12, y + h * .62) if old_left else (x + w / 2, y - 8)
        o.append(T(ox, oy, str(old), s2, outline='#3A1A1A'))
        ow = text_w(str(old), s2) / 2 + 6
        o.append(f'<path d="M{f(ox - ow)} {f(oy - s2 * .05)} L{f(ox + ow)} {f(oy - s2 * .55)}" stroke="#FF2E3B" stroke-width="4.5" stroke-linecap="round"/>')
    return ''.join(o)

def coin(cx, cy, r, p=None):
    p = p or PAL['gold']
    return (f'<g id="Coin"><circle cx="{f(cx)}" cy="{f(cy + r * .16)}" r="{f(r)}" fill="{p["d"]}" stroke="{p["t"]}" stroke-width="{f(max(2.5, r * .16))}"/>'
            f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{p["b"]}" stroke="{p["t"]}" stroke-width="{f(max(2.5, r * .16))}"/>'
            f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r * .66)}" fill="none" stroke="{p["a"]}" stroke-width="{f(r * .14)}"/>'
            f'<path d="M{f(cx - r * .55)} {f(cy - r * .1)} Q{f(cx - r * .5)} {f(cy - r * .58)} {f(cx - r * .05)} {f(cy - r * .62)}" fill="none" stroke="#FFF" stroke-width="{f(r * .14)}" stroke-linecap="round"/></g>')

def gem(cx, cy, r, p=None):
    p = p or PAL['cyan']
    pts = [(cx - r, cy - r * .3), (cx - r * .55, cy - r * .85), (cx + r * .55, cy - r * .85), (cx + r, cy - r * .3), (cx, cy + r)]
    poly = ' '.join(f'{f(a)},{f(b)}' for a, b in pts)
    return (f'<g id="Gem"><polygon points="{poly}" fill="{p["b"]}" stroke="{p["t"]}" stroke-width="{f(max(2.5, r * .14))}" stroke-linejoin="round"/>'
            f'<polygon points="{f(cx - r)},{f(cy - r * .3)} {f(cx + r)},{f(cy - r * .3)} {f(cx + r * .55)},{f(cy - r * .85)} {f(cx - r * .55)},{f(cy - r * .85)}" fill="{p["a"]}"/>'
            f'<polygon points="{f(cx - r * .35)},{f(cy - r * .3)} {f(cx + r * .35)},{f(cy - r * .3)} {f(cx)},{f(cy + r)}" fill="{p["a"]}" fill-opacity=".55"/>'
            f'<polygon points="{poly}" fill="none" stroke="{p["t"]}" stroke-width="{f(max(2.5, r * .14))}" stroke-linejoin="round"/>'
            f'<circle cx="{f(cx - r * .45)}" cy="{f(cy - r * .55)}" r="{f(r * .12)}" fill="#FFF"/></g>')

def tag(d, cx, cy, txt, p=None, rot=-8, size=22):
    """tilted shout tag (NEW!, BEST DEAL!, x2!)"""
    p = p or PAL['gold']
    w = text_w(txt, size) + size * 1.1
    h = size * 1.55
    return (f'<g id="Tag {txt}" transform="rotate({rot} {f(cx)} {f(cy)})">'
            + surface(d, cx - w / 2, cy - h / 2, w, h, p, r=h * .32, rim=0, edge=4, sw=3.5, gloss=False)
            + T(cx, cy + size * .3 - 2, txt, size, outline=p['t']) + '</g>')

def sunburst(cx, cy, R, n=16, col='#FFFFFF', op=.3, rot=0):
    o = []
    for i in range(n):
        a0 = math.radians(rot + i * 360 / n - 360 / n / 4)
        a1 = math.radians(rot + i * 360 / n + 360 / n / 4)
        o.append(f'M{f(cx)} {f(cy)} L{f(cx + R * math.cos(a0))} {f(cy + R * math.sin(a0))} L{f(cx + R * math.cos(a1))} {f(cy + R * math.sin(a1))} Z')
    return f'<path d="{" ".join(o)}" fill="{col}" fill-opacity="{op}"/>'

def glow(d, cx, cy, r, col='#FFF5A0', op=.85):
    g = d.rad([(0, col + f'{int(op * 255):02X}'), (1, col + '00')])
    return f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{g}"/>'

def sparkle(cx, cy, s, col='#FFFFFF', stroke=NAVY):
    k = s * .16
    return (f'<path d="M{f(cx)} {f(cy - s)} Q{f(cx + k)} {f(cy - k)} {f(cx + s)} {f(cy)} Q{f(cx + k)} {f(cy + k)} {f(cx)} {f(cy + s)} '
            f'Q{f(cx - k)} {f(cy + k)} {f(cx - s)} {f(cy)} Q{f(cx - k)} {f(cy - k)} {f(cx)} {f(cy - s)}Z" fill="{col}" stroke="{stroke}" stroke-width="{f(max(1.5, s * .14))}" stroke-linejoin="round"/>')

def sparkles(d, x, y, w, h, n=6, smin=7, smax=15):
    return ''.join(sparkle(x + d.rng.uniform(0, w), y + d.rng.uniform(0, h), d.rng.uniform(smin, smax)) for _ in range(n))

def header_bar(d, x, y, w, h, p, title, size=None, rot=0):
    """full-width section header with diagonal stripes, gradient title (ref_1 language)"""
    cp = d.clip(rr(x, y, w, h, 14))
    stripes = ''.join(f'<path d="M{f(x + i * 52)} {f(y + h)} L{f(x + i * 52 + h)} {f(y)} L{f(x + i * 52 + h + 26)} {f(y)} L{f(x + i * 52 + 26)} {f(y + h)} Z" fill="{p["d"]}" fill-opacity=".55"/>'
                      for i in range(-2, int(w / 52) + 2))
    size = size or h * .62
    tg = d.lin([(0, '#FFFFFF'), (1, '#FFE58A')])
    return (f'<g id="Header {title}"><rect x="{f(x)}" y="{f(y + 6)}" width="{f(w)}" height="{f(h)}" rx="14" fill="{p["t"]}" fill-opacity=".45"/>'
            f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="14" fill="{p["b"]}"/>'
            f'<g clip-path="{cp}">{stripes}<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h * .45)}" fill="#FFF" fill-opacity=".18"/></g>'
            f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="14" fill="none" stroke="{p["t"]}" stroke-width="4"/>'
            + T(x + w / 2, y + h / 2 + size * .36, title, size, fill=tg, outline=p['t'], rot=rot) + '</g>')

def plaque(d, cx, y, title, p, size=46, rot=-2):
    """title plaque that overlaps the top edge of a frame"""
    w = text_w(title, size) + size * 1.6
    h = size * 1.7
    return (f'<g id="Plaque {title}" transform="rotate({rot} {f(cx)} {f(y + h / 2)})">'
            + surface(d, cx - w / 2, y, w, h, p, r=h * .34, rim=6, texture='stripes')
            + T(cx, y + h * .5 + size * .3, title, size, fill=d.lin([(0, '#FFFFFF'), (1, '#FFF0A8')]), outline=p['t']) + '</g>')

def badge(d, cx, cy, r, p, inner='', corner=None, hexagon=False, rays=True):
    """gamepass / rarity badge: circle or hexagon, sunburst, white rim, big corner text"""
    if hexagon:
        pts = ' '.join(f'{f(cx + r * math.cos(math.radians(-90 + 60 * k)))},{f(cy + r * math.sin(math.radians(-90 + 60 * k)))}' for k in range(6))
        shape = f'<polygon points="{pts}"/>'
        outer = lambda fill, extra='': f'<polygon points="{pts}" fill="{fill}" {extra}/>'
    else:
        shape = f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}"/>'
        outer = lambda fill, extra='': f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{fill}" {extra}/>'
    bg = d.rad([(0, p['a']), (.7, p['b']), (1, p['d'])])
    cp = d.clip(shape)
    o = [f'<g id="Badge"><g transform="translate(0 7)">{outer(p["t"], "fill-opacity=\".45\"")}</g>',
         outer(bg), f'<g clip-path="{cp}">{sunburst(cx, cy, r * 1.4, 16, "#FFFFFF", .3) if rays else ""}</g>',
         outer('none', f'stroke="#FFFFFF" stroke-width="{f(r * .1)}"'),
         outer('none', f'stroke="{p["t"]}" stroke-width="{f(max(3, r * .05))}"'), inner]
    if corner:
        s = r * .5
        o.append(T(cx + r * .52, cy + r * .9, corner, s, fill=d.lin([(0, '#FFFFFF'), (1, '#FFE14A')]), outline=p['t'], rot=-8))
    o.append('</g>')
    return ''.join(o)

def pill_bar(d, x, y, w, h, frac, p, label=None):
    """progress bar: dark track + two-tone fill + label"""
    o = [f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(h / 2)}" fill="#0B0F20" fill-opacity=".55" stroke="{NAVY}" stroke-width="3.5"/>']
    fw = max(h, (w - 8) * frac)
    o.append(f'<rect x="{f(x + 4)}" y="{f(y + 4)}" width="{f(fw)}" height="{f(h - 8)}" rx="{f((h - 8) / 2)}" fill="{d.two_tone(p, .5)}"/>')
    o.append(f'<path d="M{f(x + 4 + h * .4)} {f(y + 4 + h * .2)} H{f(x + 4 + fw - h * .4)}" stroke="#FFF" stroke-opacity=".7" stroke-width="{f(h * .12)}" stroke-linecap="round"/>')
    if label:
        o.append(T(x + w / 2, y + h / 2 + h * .2, label, h * .58))
    return ''.join(o)

def stat_pill(d, x, y, w, h, icon_svg, value, plus=True, p=None):
    """HUD counter: dark translucent pill, big icon overlapping left end, value, small + square"""
    p = p or PAL['green']
    o = [f'<rect x="{f(x)}" y="{f(y + 4)}" width="{f(w)}" height="{f(h)}" rx="{f(h / 2)}" fill="#000" fill-opacity=".3"/>',
         f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(h / 2)}" fill="#0E1430" fill-opacity=".72" stroke="{NAVY}" stroke-width="3.5"/>',
         icon_svg, T(x + w / 2 + h * .2, y + h / 2 + h * .2, value, h * .55)]
    if plus:
        s = h * .82
        o.append(surface(d, x + w - s - 3, y + (h - s) / 2, s, s, p, r=s * .3, rim=0, edge=3, sw=3, shadow=False, gloss=False))
        o.append(glyph('plus', x + w - s / 2 - 3, y + h / 2 - 1.5, s / 34, '#FFF', p['t'], 2.6))
    return ''.join(o)

def close_button(d, x, y, s=64):
    return icon_button(d, x, y, s, PAL['red'], 'x')

def timer(d, cx, cy, txt, p=None, size=24):
    p = p or PAL['dark']
    w = text_w(txt, size) + size * 2.4
    h = size * 1.6
    return (f'<g id="Timer">{surface(d, cx - w / 2, cy - h / 2, w, h, p, r=h / 2, rim=0, edge=3, sw=3.5, gloss=False, shadow=False)}'
            + glyph3d('clock', cx - w / 2 + h * .55, cy - 1.5, h / 34, '#FFE14A', p['t'])
            + T(cx + h * .3, cy + size * .3, txt, size, fill='#FFE14A', outline=p['t']) + '</g>')

def frame(d, x, y, w, h, theme, title=None, close=True):
    """themed outer frame + inner panel; returns svg. theme from themes.THEMES"""
    o = [f'<g id="Frame"><rect x="{f(x)}" y="{f(y + 12)}" width="{f(w)}" height="{f(h)}" rx="40" fill="{theme["out"]}" fill-opacity=".55"/>',
         f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="40" fill="{d.lin([(0, theme["rim"][0]), (1, theme["rim"][1])])}" stroke="{theme["out"]}" stroke-width="6"/>',
         theme['edge'](d, x, y, w, h) if theme.get('edge') else '',
         f'<rect x="{f(x + 20)}" y="{f(y + 20)}" width="{f(w - 40)}" height="{f(h - 40)}" rx="26" fill="{d.lin([(0, theme["panel"][0]), (1, theme["panel"][1])])}" stroke="{theme["out"]}" stroke-width="5"/>',
         '' if theme.get('edge') else f'<path d="M{f(x + 13)} {f(y + 80)} Q{f(x + 13)} {f(y + 13)} {f(x + 80)} {f(y + 13)}" fill="none" stroke="#FFF" stroke-width="7" stroke-linecap="round" stroke-opacity=".8"/>',
         theme['top'](d, x, y, w) if theme.get('top') else '', '</g>']
    if title:
        o.append(plaque(d, x + w / 2, y - 46, title, PAL[theme['accent']]))
    if close:
        o.append(close_button(d, x + w - 52, y - 20, 72))
    return ''.join(o)

# ---------- rendered item images (Blender PNGs) ----------
REN_DIRS = [os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'renders'),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pack', 'items-voxel'),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pack', 'fruits-voxel'),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pack', 'icons-toon')]
_img_cache = {}

def item_img(name, cx, cy, size, outline=(20, 14, 30, 255), px=9):
    """embed a render with a dark sticker outline, fitted into a size x size box centred at cx, cy"""
    from PIL import Image, ImageFilter
    import base64, io
    key = (name, outline, px)
    if key not in _img_cache:
        nm, sub = (name.split('/', 1)[1], name.split('/', 1)[0]) if '/' in name else (name, None)
        dirs = [d for d in REN_DIRS if (sub is None or d.endswith(sub) or (sub == 'toon' and d.endswith('icons-toon')))]
        path = next(os.path.join(d, nm + '.png') for d in dirs if os.path.exists(os.path.join(d, nm + '.png')))
        im = Image.open(path).convert('RGBA')
        a = im.split()[3].point(lambda v: 255 if v > 40 else 0)
        ol = Image.new('RGBA', im.size, outline); ol.putalpha(a.filter(ImageFilter.MaxFilter(px)))
        im = Image.alpha_composite(ol, im); im = im.crop(im.getbbox())
        b = io.BytesIO(); im.save(b, 'PNG')
        _img_cache[key] = ('data:image/png;base64,' + base64.b64encode(b.getvalue()).decode(), im.size)
    uri, (w, h) = _img_cache[key]
    k = size / max(w, h)
    return f'<image href="{uri}" x="{f(cx - w * k / 2)}" y="{f(cy - h * k / 2)}" width="{f(w * k)}" height="{f(h * k)}"/>'

def item_window(d, cx, cy, s, name, rp, mythic=False, base=('#1A1030', '#2C1A4A'), out=NAVY, r=18, item_scale=.9):
    """item set INTO a surface: recessed window, rarity glow + rays, contact shadow, outline"""
    x, y = cx - s / 2, cy - s / 2
    cp = d.clip(rr(x, y, s, s, r))
    gc = '#FFE14A' if mythic else rp['a']
    return ''.join(['<g id="Item Window">',
        f'<rect x="{f(x)}" y="{f(y)}" width="{f(s)}" height="{f(s)}" rx="{r}" fill="{d.lin([(0, base[0]), (1, base[1])])}"/>',
        f'<g clip-path="{cp}"><circle cx="{f(cx)}" cy="{f(cy + s * .05)}" r="{f(s * .62)}" fill="{d.rad([(0, gc + "C0"), (.6, rp["b"] + "55"), (1, rp["b"] + "00")])}"/>',
        sunburst(cx, cy + s * .05, s * .8, 12, '#FFFFFF', .12),
        f'<rect x="{f(x - 6)}" y="{f(y - 6)}" width="{f(s + 12)}" height="{f(s + 12)}" rx="{r + 4}" fill="none" stroke="#000" stroke-opacity=".45" stroke-width="16" transform="translate(0 5)"/></g>',
        f'<ellipse cx="{f(cx)}" cy="{f(y + s * .86)}" rx="{f(s * .3)}" ry="{f(s * .07)}" fill="#000" fill-opacity=".38"/>',
        item_img(name, cx, cy - s * .04, s * item_scale),
        f'<rect x="{f(x)}" y="{f(y)}" width="{f(s)}" height="{f(s)}" rx="{r}" fill="none" stroke="{out}" stroke-width="5"/></g>'])
