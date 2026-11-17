"""Roblox-flat style (what big games like Throw Food for Animals use): thick BLACK outline on everything,
flat strong colours with a lighter top band, dark translucent item tiles with rays, lime buy buttons,
big yellow titles, 4-point sparkles. Text = Fredoka Bold, white/yellow, thick black outline, small drop."""
import os
import text_paths as TP
from uikit import f, rr, sunburst, robux, text_w, NAVY
TP.set_font(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts', 'FredokaBold.ttf'))
K = '#000000'

def txt(x, y, s, size, fill='#FFFFFF', anchor='middle', rot=0, ow=None):
    return TP.label(x, y, s, size, fill=fill, outline=K, anchor=anchor, rot=rot, ow=ow or max(4, round(size / 4.2)))

def title_fill(d):
    return d.lin([(0, '#FFF86A'), (.55, '#FFE21A'), (1, '#FFB300')])

def box(d, x, y, w, h, top, bot, r=14, sw=6, band=.42, sheen=True, name='Box'):
    """flat surface: base colour + lighter top band + 2 diagonal sheen stripes + thick black outline"""
    cp = d.clip(rr(x, y, w, h, r))
    o = [f'<g id="{name}"><rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{r}" fill="{bot}"/>',
         f'<g clip-path="{cp}"><rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h * band)}" fill="{top}"/>']
    if sheen:
        for k, (px, pw) in enumerate(((.62, .07), (.72, .03))):
            sx = x + w * px
            o.append(f'<path d="M{f(sx)} {f(y + h)} L{f(sx + h * .6)} {f(y)} L{f(sx + h * .6 + w * pw)} {f(y)} L{f(sx + w * pw)} {f(y + h)} Z" fill="#FFFFFF" fill-opacity=".16"/>')
    o.append(f'</g><rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{r}" fill="none" stroke="{K}" stroke-width="{sw}"/></g>')
    return ''.join(o)

def lime(d, x, y, w, h, name='Buy'):
    return box(d, x, y, w, h, '#7CFF4A', '#22D10A', r=16, sw=6, name=name)

def tile(d, x, y, s, base='#3A1466', rays='#FFFFFF', rainbow=None, name='Tile'):
    """dark translucent square tile with soft rays inside; rainbow = gradient url for the mythic border"""
    cp = d.clip(rr(x, y, s, s, 8))
    o = [f'<g id="{name}"><rect x="{f(x)}" y="{f(y)}" width="{f(s)}" height="{f(s)}" rx="8" fill="{base}" fill-opacity=".78"/>',
         f'<g clip-path="{cp}">{sunburst(x + s / 2, y + s * .45, s * .9, 14, rays, .13)}</g>']
    if rainbow:
        o.append(f'<rect x="{f(x - 4)}" y="{f(y - 4)}" width="{f(s + 8)}" height="{f(s + 8)}" rx="11" fill="none" stroke="{rainbow}" stroke-width="7"/>')
    o.append(f'<rect x="{f(x)}" y="{f(y)}" width="{f(s)}" height="{f(s)}" rx="8" fill="none" stroke="{K}" stroke-width="5"/></g>')
    return ''.join(o)

def pill(d, cx, cy, w, h, fill='#000000', op=.45):
    return f'<rect x="{f(cx - w / 2)}" y="{f(cy - h / 2)}" width="{f(w)}" height="{f(h)}" rx="{f(h / 2)}" fill="{fill}" fill-opacity="{op}"/>'

def star4(cx, cy, s, fill='#FFFFFF', stroke='#000000', sw=None):
    k = s * .22
    return (f'<path d="M{f(cx)} {f(cy - s)} Q{f(cx + k)} {f(cy - k)} {f(cx + s)} {f(cy)} Q{f(cx + k)} {f(cy + k)} {f(cx)} {f(cy + s)} '
            f'Q{f(cx - k)} {f(cy + k)} {f(cx - s)} {f(cy)} Q{f(cx - k)} {f(cy - k)} {f(cx)} {f(cy - s)}Z" fill="{fill}" stroke="{stroke}" stroke-width="{f(sw or max(2, s * .09))}" stroke-linejoin="round"/>')

def robux_w(x, y, s):
    """white Robux mark with black outline, s = scale (24px base)"""
    return robux(x, y, s, '#FFFFFF', K)

# ---------- 2D flat icons (black outline, 3 tones, one highlight) ----------
def cash_stack(cx, cy, s, rot=0):
    """isometric bundle of cash: light top, mid left, dark right, yellow band"""
    w, h, t = s, s * .5, s * .32
    top = f'M{f(cx)} {f(cy - h / 2)} L{f(cx + w / 2)} {f(cy)} L{f(cx)} {f(cy + h / 2)} L{f(cx - w / 2)} {f(cy)} Z'
    left = f'M{f(cx - w / 2)} {f(cy)} L{f(cx)} {f(cy + h / 2)} L{f(cx)} {f(cy + h / 2 + t)} L{f(cx - w / 2)} {f(cy + t)} Z'
    right = f'M{f(cx + w / 2)} {f(cy)} L{f(cx)} {f(cy + h / 2)} L{f(cx)} {f(cy + h / 2 + t)} L{f(cx + w / 2)} {f(cy + t)} Z'
    bt = f'M{f(cx - w * .08)} {f(cy - h * .42)} L{f(cx + w * .34)} {f(cy - h * .08)} L{f(cx + w * .16)} {f(cy + h * .17)} L{f(cx - w * .26)} {f(cy - h * .17)} Z'
    bl = f'M{f(cx + w * .16)} {f(cy + h * .17)} L{f(cx + w * .34)} {f(cy - h * .08)} L{f(cx + w * .34)} {f(cy - h * .08 + t)} L{f(cx + w * .16)} {f(cy + h * .17 + t)} Z'
    lines = ''.join(f'<path d="M{f(cx - w / 2)} {f(cy + t * k / 3)} L{f(cx)} {f(cy + h / 2 + t * k / 3)}" stroke="#0E5A1E" stroke-width="{f(s * .02)}"/>' for k in (1, 2))
    sw = f(max(2.5, s * .055))
    return (f'<g transform="rotate({rot} {f(cx)} {f(cy)})"><path d="{left}" fill="#2BB24A"/><path d="{right}" fill="#178A35"/><path d="{top}" fill="#5EE36F"/>{lines}'
            f'<path d="{bt}" fill="#FFD21F"/><path d="{bl}" fill="#E8A20C"/>'
            f'<path d="M{f(cx - w / 2)} {f(cy)} L{f(cx)} {f(cy - h / 2)} L{f(cx + w / 2)} {f(cy)} L{f(cx + w / 2)} {f(cy + t)} L{f(cx)} {f(cy + h / 2 + t)} L{f(cx - w / 2)} {f(cy + t)} Z" fill="none" stroke="#000" stroke-width="{sw}" stroke-linejoin="round"/>'
            f'<path d="M{f(cx - w / 2)} {f(cy)} L{f(cx)} {f(cy + h / 2)} L{f(cx + w / 2)} {f(cy)} M{f(cx)} {f(cy + h / 2)} V{f(cy + h / 2 + t)}" fill="none" stroke="#000" stroke-width="{f(max(1.5, s * .035))}" stroke-linejoin="round"/>'
            f'<path d="M{f(cx - w * .3)} {f(cy - h * .05)} L{f(cx - w * .12)} {f(cy - h * .3)}" stroke="#FFFFFF" stroke-opacity=".75" stroke-width="{f(s * .04)}" stroke-linecap="round"/></g>')

def bolt(cx, cy, s, rot=0):
    p = [(.1, -1), (-.5, .1), (-.05, .1), (-.2, 1), (.55, -.2), (.08, -.2), (.3, -1)]
    pts = ' '.join(f'{f(cx + x * s * .85)},{f(cy + y * s * .6)}' for x, y in p)
    half = ' '.join(f'{f(cx + x * s * .85)},{f(cy + y * s * .6)}' for x, y in [(.1, -1), (-.5, .1), (-.05, .1), (.08, -.2), (.3, -1)])
    return (f'<g transform="rotate({rot} {f(cx)} {f(cy)})"><polygon points="{pts}" fill="#FFB400"/><polygon points="{half}" fill="#FFE24A"/>'
            f'<polygon points="{pts}" fill="none" stroke="#000" stroke-width="{f(max(2.5, s * .07))}" stroke-linejoin="round"/>'
            f'<path d="M{f(cx + .02 * s)} {f(cy - .45 * s)} L{f(cx - .14 * s)} {f(cy - .08 * s)}" stroke="#FFF" stroke-width="{f(s * .05)}" stroke-linecap="round"/></g>')

def gem2d(cx, cy, s, a='#B98CFF', b='#7A3CF0', c='#5320B8', rot=0):
    r = s / 2
    outer = f'{f(cx - r)},{f(cy - r * .25)} {f(cx - r * .5)},{f(cy - r * .8)} {f(cx + r * .5)},{f(cy - r * .8)} {f(cx + r)},{f(cy - r * .25)} {f(cx)},{f(cy + r)}'
    return (f'<g transform="rotate({rot} {f(cx)} {f(cy)})"><polygon points="{outer}" fill="{b}"/>'
            f'<polygon points="{f(cx - r)},{f(cy - r * .25)} {f(cx + r)},{f(cy - r * .25)} {f(cx + r * .5)},{f(cy - r * .8)} {f(cx - r * .5)},{f(cy - r * .8)}" fill="{a}"/>'
            f'<polygon points="{f(cx)},{f(cy - r * .25)} {f(cx + r)},{f(cy - r * .25)} {f(cx)},{f(cy + r)}" fill="{c}"/>'
            f'<polygon points="{outer}" fill="none" stroke="#000" stroke-width="{f(max(2.5, s * .07))}" stroke-linejoin="round"/>'
            f'<path d="M{f(cx - r * .55)} {f(cy - r * .5)} L{f(cx - r * .25)} {f(cy - r * .65)}" stroke="#FFF" stroke-width="{f(s * .06)}" stroke-linecap="round"/></g>')

def pile(fn, cx, cy, s, n, seed=1):
    """pile of n icons: bigger price -> bigger pile. Back rows first, slight random tilt and size."""
    import random
    r = random.Random(seed); out = []
    rows = max(1, int((n + 1) ** .5))
    spots = []
    for i in range(n):
        row = i % rows; col = i // rows
        spots.append((cx + (col - n / rows / 2 + .5) * s * .55 + r.uniform(-6, 6), cy - row * s * .3 + r.uniform(-4, 4), s * r.uniform(.85, 1.05), r.uniform(-14, 14)))
    for x, y, sz, rot in sorted(spots, key=lambda p: p[1]):
        out.append(fn(x, y, sz, rot))
    return ''.join(out)

def value_ribbon(d, cx, cy, txt_, kind, rot=0, size=30):
    fills = {'good': ('#4FC3FF', '#1E7BE0'), 'better': ('#FF7EC8', '#E9327E'), 'great': ('#FFC94A', '#FF8A00'), 'most': None}
    w = TP.width(txt_, size) + size * 1.6; h = size * 1.45
    g = d.lin([(0, '#FF4D6D'), (.25, '#FFB020'), (.5, '#3EE07A'), (.75, '#2FA8FF'), (1, '#E13CFF')], x2=1, y2=0) if kind == 'most' else d.lin([(0, fills[kind][0]), (1, fills[kind][1])])
    return (f'<g transform="rotate({rot} {f(cx)} {f(cy)})"><rect x="{f(cx - w / 2)}" y="{f(cy - h / 2)}" width="{f(w)}" height="{f(h)}" rx="{f(h / 2)}" fill="{g}" stroke="#000" stroke-width="5"/>'
            f'<rect x="{f(cx - w / 2 + 8)}" y="{f(cy - h / 2 + 5)}" width="{f(w - 16)}" height="{f(h * .32)}" rx="{f(h * .16)}" fill="#FFF" fill-opacity=".28"/>'
            + txt(cx, cy + size * .34, txt_, size, fill='#FFF8E6') + '</g>')

def card(d, x, y, w, h, c1, c2, rim='#FFFFFF', r=22, name='Card'):
    """black outer frame + light inner rim + diagonal gradient + glow behind the item area"""
    g = d.lin([(0, c1), (1, c2)], x2=1, y2=1)
    cp = d.clip(rr(x + 9, y + 9, w - 18, h - 18, r - 6))
    return (f'<g id="{name}"><rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{r}" fill="#111" stroke="#000" stroke-width="4"/>'
            f'<rect x="{f(x + 6)}" y="{f(y + 6)}" width="{f(w - 12)}" height="{f(h - 12)}" rx="{r - 3}" fill="{rim}" fill-opacity=".55"/>'
            f'<rect x="{f(x + 9)}" y="{f(y + 9)}" width="{f(w - 18)}" height="{f(h - 18)}" rx="{r - 6}" fill="{g}"/>'
            f'<g clip-path="{cp}"><circle cx="{f(x + w / 2)}" cy="{f(y + h * .4)}" r="{f(w * .5)}" fill="{d.rad([(0, "#FFFFFF90"), (1, "#FFFFFF00")])}"/>'
            f'{sunburst(x + w / 2, y + h * .4, w * .7, 12, "#FFFFFF", .1)}'
            f'<path d="M{f(x + w * .55)} {f(y + h)} L{f(x + w * .55 + h * .5)} {f(y)} L{f(x + w * .62 + h * .5)} {f(y)} L{f(x + w * .62)} {f(y + h)} Z" fill="#FFF" fill-opacity=".08"/></g></g>')

def section(cx, y, title, W, size=40):
    w = TP.width(title, size) + size * 2.4
    return (f'<path d="M{f(cx - W / 2 + 40)} {f(y)} H{f(cx - w / 2 - 30)} M{f(cx + w / 2 + 30)} {f(y)} H{f(cx + W / 2 - 40)}" stroke="#8A93AA" stroke-width="3"/>'
            f'<rect x="{f(cx - w / 2)}" y="{f(y - size * .8)}" width="{f(w)}" height="{f(size * 1.6)}" rx="{f(size * .8)}" fill="#3B4258" stroke="#000" stroke-width="5"/>'
            + txt(cx, y + size * .35, title, size, fill='#FFF8E6'))

def buy(d, x, y, w, h, cost):
    s = h * .62 / 24
    tw = TP.width(str(cost), h * .62)
    gx = x + w / 2 - (tw + 24 * s + 12) / 2
    return lime(d, x, y, w, h) + robux_w(gx, y + h / 2 - 12 * s - 2, s) + txt(gx + 24 * s + 12 + tw / 2, y + h / 2 + h * .22, str(cost), h * .62)


def img_pile(name, cx, cy, s, n, seed=1):
    """pile of n toon renders (renders/toon/<name>.png); more = bigger pile, back rows first"""
    from uikit import item_img
    def one(x, y, sz, rot):
        return f'<g transform="rotate({rot:.1f} {x:.1f} {y:.1f})">' + item_img('toon/' + name, x, y, sz, outline=(0, 0, 0, 255), px=3) + '</g>'
    return pile(one, cx, cy, s, n, seed)

# ---------- 2.5D single icons: clean shapes, soft gradients for volume, thick black outline, one highlight ----------
def cash_icon(d, cx, cy, s):
    """isometric cash bundle like the big games draw it: 3 faces with soft gradients + yellow band, no line clutter"""
    w, h, t = s, s * .52, s * .34
    P = lambda pts: ' '.join(f'{f(cx + x * w)},{f(cy + y * w)}' for x, y in pts)
    top = P([(0, -.26), (.5, 0), (0, .26), (-.5, 0)])
    left = P([(-.5, 0), (0, .26), (0, .26 + .34), (-.5, .34)])
    right = P([(.5, 0), (0, .26), (0, .6), (.5, .34)])
    bt = P([(.06, -.23), (.27, -.12), (-.21, .13), (-.42, .02)])
    bl = P([(-.21, .13), (-.42, .02), (-.42, .36), (-.21, .47)])
    sil = P([(-.5, 0), (0, -.26), (.5, 0), (.5, .34), (0, .6), (-.5, .34)])
    gt = d.lin([(0, '#8BFF8F'), (1, '#3FD65A')], x2=1, y2=1)
    gl = d.lin([(0, '#33C24E'), (1, '#1E9A3A')])
    gr = d.lin([(0, '#22A23F'), (1, '#127A2C')])
    gb = d.lin([(0, '#FFE866'), (1, '#FFB300')], x2=1, y2=1)
    gbl = d.lin([(0, '#FFB300'), (1, '#E08A00')])
    sw = f(s * .075)
    return (f'<g id="Cash Icon"><polygon points="{sil}" fill="#000" stroke="#000" stroke-width="{sw}" stroke-linejoin="round" transform="translate(0 {f(s * .03)})"/>'
            f'<polygon points="{left}" fill="{gl}"/><polygon points="{right}" fill="{gr}"/><polygon points="{top}" fill="{gt}"/>'
            f'<polygon points="{bl}" fill="{gbl}"/><polygon points="{bt}" fill="{gb}"/>'
            f'<polygon points="{sil}" fill="none" stroke="#000" stroke-width="{sw}" stroke-linejoin="round"/>'
            f'<ellipse cx="{f(cx + w * .12)}" cy="{f(cy - w * .02)}" rx="{f(w * .13)}" ry="{f(w * .07)}" fill="#FFFFFF" fill-opacity=".35"/>'
            f'<path d="M{f(cx - w * .36)} {f(cy - w * .02)} L{f(cx - w * .1)} {f(cy - w * .16)}" stroke="#FFFFFF" stroke-width="{f(s * .045)}" stroke-linecap="round" stroke-opacity=".9"/></g>')

def gem_icon(d, cx, cy, s, a='#E2C8FF', b='#A266FF', c='#6A2BE0', k='#4A16B0'):
    """faceted gem with gradient facets (reads 3D, stays 2D), thick black outline, sparkle highlight"""
    r = s / 2
    P = lambda pts: ' '.join(f'{f(cx + x * r)},{f(cy + y * r)}' for x, y in pts)
    sil = P([(-1, -.3), (-.55, -.85), (.55, -.85), (1, -.3), (0, 1)])
    facets = [([(-.55, -.85), (-.2, -.85), (-.35, -.3), (-1, -.3)], d.lin([(0, a), (1, b)])),
              ([(-.2, -.85), (.2, -.85), (.35, -.3), (-.35, -.3)], d.lin([(0, '#FFFFFF'), (1, a)])),
              ([(.2, -.85), (.55, -.85), (1, -.3), (.35, -.3)], d.lin([(0, b), (1, c)])),
              ([(-1, -.3), (-.35, -.3), (0, 1)], d.lin([(0, b), (1, c)])),
              ([(-.35, -.3), (.35, -.3), (0, 1)], d.lin([(0, a), (1, b)])),
              ([(.35, -.3), (1, -.3), (0, 1)], d.lin([(0, c), (1, k)]))]
    sw = f(s * .07)
    o = [f'<g id="Gem Icon"><polygon points="{sil}" fill="#000" stroke="#000" stroke-width="{sw}" stroke-linejoin="round" transform="translate(0 {f(s * .03)})"/>']
    o += [f'<polygon points="{P(pts)}" fill="{g}"/>' for pts, g in facets]
    o.append(f'<path d="M{P([(-1, -.3)]).replace(",", " ")} L{P([(1, -.3)]).replace(",", " ")}" stroke="{k}" stroke-opacity=".35" stroke-width="{f(s * .02)}"/>')
    o.append(f'<polygon points="{sil}" fill="none" stroke="#000" stroke-width="{sw}" stroke-linejoin="round"/>')
    o.append(star4(cx - r * .45, cy - r * .55, r * .2, '#FFFFFF', 'none', 0))
    o.append('</g>')
    return ''.join(o)

def cash_icon(d, cx, cy, s, L=1.0, S=.56, T=.3):
    """proper isometric bundle: long side L, short side S, thickness T; band crosses the top and the front face"""
    import math
    u = (math.cos(math.radians(30)) * L, math.sin(math.radians(30)) * L)
    v = (-math.cos(math.radians(30)) * S, math.sin(math.radians(30)) * S)
    def P(a, b, c):
        return (a * u[0] + b * v[0], a * u[1] + b * v[1] - c * T)
    corners = [P(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)]
    mx = (min(p[0] for p in corners) + max(p[0] for p in corners)) / 2
    my = (min(p[1] for p in corners) + max(p[1] for p in corners)) / 2
    k = s / (max(p[0] for p in corners) - min(p[0] for p in corners))
    def Q(*pts):
        return ' '.join(f'{f(cx + (P(*p)[0] - mx) * k)},{f(cy + (P(*p)[1] - my) * k)}' for p in pts)
    top = Q((0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1))
    front = Q((0, 1, 1), (1, 1, 1), (1, 1, 0), (0, 1, 0))
    side = Q((1, 0, 1), (1, 1, 1), (1, 1, 0), (1, 0, 0))
    sil = Q((0, 0, 1), (1, 0, 1), (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 1, 1))
    a0, a1 = .62, .78
    bt = Q((a0, 0, 1), (a1, 0, 1), (a1, 1, 1), (a0, 1, 1))
    bf = Q((a0, 1, 1), (a1, 1, 1), (a1, 1, 0), (a0, 1, 0))
    gt = d.lin([(0, '#8BFF8F'), (1, '#44D85E')], x2=1, y2=1)
    gf = d.lin([(0, '#2FBE4C'), (1, '#1C9A39')])
    gs = d.lin([(0, '#1F9E3D'), (1, '#127A2C')])
    gb = d.lin([(0, '#FFEA70'), (1, '#FFC21A')], x2=1, y2=1)
    gbf = d.lin([(0, '#FFB300'), (1, '#E38A00')])
    sw = f(s * .07)
    lines = ''.join(f'<polyline points="{Q((0, 1, c), (1, 1, c), (1, 0, c))}" fill="none" stroke="#0E6A26" stroke-opacity=".55" stroke-width="{f(s * .018)}"/>' for c in (.36, .68))
    hl = Q((.08, .12, 1), (.42, .12, 1))
    return (f'<g id="Cash Icon"><polygon points="{sil}" fill="#000" stroke="#000" stroke-width="{sw}" stroke-linejoin="round" transform="translate(0 {f(s * .035)})"/>'
            f'<polygon points="{front}" fill="{gf}"/><polygon points="{side}" fill="{gs}"/><polygon points="{top}" fill="{gt}"/>{lines}'
            f'<polygon points="{bf}" fill="{gbf}"/><polygon points="{bt}" fill="{gb}"/>'
            f'<polygon points="{sil}" fill="none" stroke="#000" stroke-width="{sw}" stroke-linejoin="round"/>'
            f'<polyline points="{Q((0, 1, 1), (1, 1, 1), (1, 0, 1))}" fill="none" stroke="#000" stroke-width="{f(s * .03)}" stroke-linejoin="round"/>'
            f'<polyline points="{hl}" fill="none" stroke="#FFFFFF" stroke-width="{f(s * .045)}" stroke-linecap="round" stroke-opacity=".9"/></g>')
