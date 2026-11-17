"""World materials: wood planks, iron plates, canvas awning, hanging signs, stone walls.
The rule that made the seed shop work: build the screen OUT OF a material, keep the palette
restrained, use colour only as accents (rarity stripe / gem stud / glow inside the item window)."""
from uikit import f, rr, T, text_w, gem, PAL, sunburst

WOOD = dict(a='#C98A52', b='#A86A36', d='#7A4520', t='#3B1E0C')        # pine, seed stall
OAK = dict(a='#F2D3A2', b='#E2BC84', d='#B88A52', t='#3B1E0C')         # light shelf boards
WALNUT = dict(a='#8A5634', b='#6E4227', d='#4A2A16', t='#1E0F07')      # dark armory wood
IRON = dict(a='#7C8597', b='#555D6E', d='#363C49', t='#12151C')
BRASS = dict(a='#F3D27A', b='#C99A3A', d='#8A6420', t='#3A2608')

def planks(d, x, y, w, h, tone=WOOD, ph=34, r=18, name='Planks', nails='ends', shadow=True):
    """horizontal planks: per-plank tint, dark gaps, grain strokes, knots, optional nail heads"""
    out = tone['t']
    cp = d.clip(rr(x, y, w, h, r))
    o = [f'<g id="{name}">']
    if shadow:
        o.append(f'<rect x="{f(x)}" y="{f(y + 8)}" width="{f(w)}" height="{f(h)}" rx="{r}" fill="{out}" fill-opacity=".5"/>')
    o.append(f'<g clip-path="{cp}"><rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="{tone["b"]}"/>')
    k, py = 0, y
    mid = '#' + ''.join(f'{(int(tone["a"][i:i + 2], 16) + int(tone["b"][i:i + 2], 16)) // 2:02X}' for i in (1, 3, 5))
    while py < y + h:
        o.append(f'<rect x="{f(x)}" y="{f(py)}" width="{f(w)}" height="{f(ph)}" fill="{(tone["a"], tone["b"], mid)[k % 3]}"/>')
        o.append(f'<rect x="{f(x)}" y="{f(py)}" width="{f(w)}" height="4" fill="#FFFFFF" fill-opacity=".16"/>')
        for _ in range(3):
            gx = x + d.rng.uniform(0, w * .7); gl = d.rng.uniform(w * .12, w * .3); gy = py + d.rng.uniform(8, max(9, ph - 8))
            o.append(f'<path d="M{f(gx)} {f(gy)} q{f(gl / 2)} {f(d.rng.uniform(-3, 3))} {f(gl)} 0" fill="none" stroke="{tone["d"]}" stroke-opacity=".45" stroke-width="2.2" stroke-linecap="round"/>')
        if d.rng.random() < .35 and w > 80:
            o.append(f'<ellipse cx="{f(x + d.rng.uniform(30, w - 30))}" cy="{f(py + ph / 2)}" rx="7" ry="4" fill="none" stroke="{tone["d"]}" stroke-opacity=".6" stroke-width="2.4"/>')
        if w > 160:
            seam = x + d.rng.uniform(w * .25, w * .75)
            o.append(f'<path d="M{f(seam)} {f(py)} v{f(ph)}" stroke="{out}" stroke-opacity=".5" stroke-width="3"/>')
        o.append(f'<rect x="{f(x)}" y="{f(py + ph - 3)}" width="{f(w)}" height="3" fill="{out}" fill-opacity=".55"/>')
        if nails == 'ends':
            for nx in (x + 16, x + w - 16):
                o.append(f'<circle cx="{f(nx)}" cy="{f(py + ph / 2)}" r="3" fill="#D8D0C4" stroke="{out}" stroke-width="1.6"/>')
        py += ph; k += 1
    o.append(f'</g><rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{r}" fill="none" stroke="{out}" stroke-width="6"/></g>')
    return ''.join(o)

def rivet(cx, cy, r=5, tone=IRON):
    return (f'<circle cx="{f(cx)}" cy="{f(cy + 1.5)}" r="{f(r)}" fill="{tone["t"]}"/>'
            f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{tone["a"]}" stroke="{tone["t"]}" stroke-width="2"/>'
            f'<circle cx="{f(cx - r * .3)}" cy="{f(cy - r * .3)}" r="{f(r * .3)}" fill="#FFFFFF" fill-opacity=".8"/>')

def plate(d, x, y, w, h, tone=IRON, r=12, rivets=True, name='Plate', sw=5):
    """metal plate: vertical gradient, top bevel light, bottom shade, rivets in corners, a couple of scratches"""
    g = d.lin([(0, tone['a']), (.5, tone['b']), (1, tone['d'])])
    o = [f'<g id="{name}"><rect x="{f(x)}" y="{f(y + 6)}" width="{f(w)}" height="{f(h)}" rx="{r}" fill="{tone["t"]}" fill-opacity=".5"/>',
         f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{r}" fill="{g}" stroke="{tone["t"]}" stroke-width="{sw}"/>',
         f'<path d="M{f(x + r)} {f(y + 4)} H{f(x + w - r)}" stroke="#FFFFFF" stroke-opacity=".45" stroke-width="3" stroke-linecap="round"/>',
         f'<path d="M{f(x + r)} {f(y + h - 4)} H{f(x + w - r)}" stroke="#000" stroke-opacity=".25" stroke-width="3" stroke-linecap="round"/>']
    for _ in range(2 if w > 120 else 0):
        sx, sy = x + d.rng.uniform(20, w - 60), y + d.rng.uniform(10, max(11, h - 10))
        o.append(f'<path d="M{f(sx)} {f(sy)} l{f(d.rng.uniform(18, 40))} {f(d.rng.uniform(-4, 4))}" stroke="#FFFFFF" stroke-opacity=".18" stroke-width="1.6" stroke-linecap="round"/>')
    if rivets and h > 34:
        q = min(14, h * .25)
        for cx, cy in ((x + q, y + q), (x + w - q, y + q), (x + q, y + h - q), (x + w - q, y + h - q)):
            o.append(rivet(cx, cy, 4.5 if h > 60 else 3.5, tone))
    o.append('</g>')
    return ''.join(o)

def iron_corners(x, y, w, h, s=34, tone=IRON):
    """L-shaped iron brackets on the four corners of a board"""
    o = []
    for cx, cy, sx, sy in ((x, y, 1, 1), (x + w, y, -1, 1), (x, y + h, 1, -1), (x + w, y + h, -1, -1)):
        p = f'M{f(cx)} {f(cy)} h{f(sx * s)} v{f(sy * 12)} h{f(-sx * (s - 12))} v{f(sy * (s - 12))} h{f(-sx * 12)} Z'
        o.append(f'<path d="{p}" fill="{tone["b"]}" stroke="{tone["t"]}" stroke-width="3.5" stroke-linejoin="round"/>')
        o.append(rivet(cx + sx * 7, cy + sy * 7, 3.5, tone))
    return ''.join(o)

def iron_band(d, x, y, w, h=22, tone=IRON):
    o = [plate(d, x, y, w, h, tone, r=6, rivets=False, name='Band', sw=4)]
    n = max(2, int(w / 90))
    for i in range(n):
        o.append(rivet(x + 20 + i * (w - 40) / (n - 1), y + h / 2, 4, tone))
    return ''.join(o)

def hanging_sign(d, cx, y, title, tone=WOOD, size=44, chain=False):
    w = text_w(title, size) + 70; h = size * 1.75
    out = tone['t']
    if chain:
        links = ''.join(f'<ellipse cx="{f(sx)}" cy="{f(y - 40 + i * 12)}" rx="4" ry="7" fill="none" stroke="{IRON["a"]}" stroke-width="3.5"/>'
                        for sx in (cx - w * .32, cx + w * .32) for i in range(4))
    else:
        links = f'<path d="M{f(cx - w * .32)} {f(y - 40)} V{f(y + 8)} M{f(cx + w * .32)} {f(y - 40)} V{f(y + 8)}" stroke="#7A5A34" stroke-width="5" stroke-linecap="round"/>'
    return (f'<g id="Sign {title}">{links}<g transform="rotate(-1.5 {f(cx)} {f(y + h / 2)})">'
            + planks(d, cx - w / 2, y, w, h, tone=tone, ph=h / 2, r=14, name='Sign Board')
            + T(cx, y + h / 2 + size * .34, title, size, fill=d.lin([(0, '#FFFFFF'), (1, '#FFE7B0')]), outline=out) + '</g></g>')

def awning(d, x, y, w, h, n=9, c1='#2F9E44', c2='#F4F1E6', s1='#1F7A33', s2='#D9D3C0', out='#3B1E0C'):
    sw = w / n
    o = ['<g id="Awning">']
    for i in range(n):
        sx = x + i * sw
        col, sh = (c1, s1) if i % 2 == 0 else (c2, s2)
        scal = f'M{f(sx)} {f(y)} H{f(sx + sw)} V{f(y + h)} Q{f(sx + sw / 2)} {f(y + h + sw * .55)} {f(sx)} {f(y + h)} Z'
        o.append(f'<path d="{scal}" transform="translate(0 7)" fill="{out}" fill-opacity=".35"/>')
        o.append(f'<path d="{scal}" fill="{col}" stroke="{out}" stroke-width="4" stroke-linejoin="round"/>')
        o.append(f'<path d="M{f(sx + sw * .72)} {f(y + 4)} V{f(y + h + sw * .1)}" stroke="{sh}" stroke-width="{f(sw * .22)}" stroke-opacity=".8"/>')
        o.append(f'<path d="M{f(sx + sw * .2)} {f(y + 8)} V{f(y + h * .55)}" stroke="#FFFFFF" stroke-width="4" stroke-opacity=".35" stroke-linecap="round"/>')
    o.append(planks(d, x - 26, y - 34, w + 52, 40, ph=40, r=12, name='Awning Bar'))
    o.append('</g>')
    return ''.join(o)

def stone_wall(d, W, H, base='#2B2F3A', light='#3A3F4D', line='#14161C', bh=58):
    """dark castle wall backdrop: offset blocks, each slightly different"""
    o = [f'<rect width="{W}" height="{H}" fill="{base}"/>']
    row = 0
    for y in range(-10, H, bh):
        x = -((row % 2) * 60)
        while x < W:
            bw = d.rng.uniform(100, 150)
            sh = d.rng.choice((base, light, '#33384A'))
            o.append(f'<rect x="{f(x + 2)}" y="{f(y + 2)}" width="{f(bw - 4)}" height="{bh - 4}" rx="6" fill="{sh}" stroke="{line}" stroke-width="3"/>')
            o.append(f'<path d="M{f(x + 8)} {f(y + 6)} H{f(x + bw - 10)}" stroke="#FFFFFF" stroke-opacity=".06" stroke-width="3"/>')
            x += bw
        row += 1
    return ''.join(o)

def torch_glow(d, cx, cy, r=380, col='#FF9A3C', op=.45):
    g = d.rad([(0, col + f'{int(op * 255):02X}'), (1, col + '00')])
    return f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{g}"/>'

def gem_stud(cx, cy, rp, r=13):
    """small rarity gem set in a brass bezel - the rarity accent on a material card"""
    return (f'<circle cx="{f(cx)}" cy="{f(cy + 2)}" r="{f(r + 5)}" fill="{BRASS["t"]}"/>'
            f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r + 5)}" fill="{BRASS["b"]}" stroke="{BRASS["t"]}" stroke-width="3"/>'
            + gem(cx, cy + 1, r, rp))

def cloth_banner(d, cx, y, title, cloth=('#D9343F', '#A81E2B', '#5E0A17'), size=40, rot=-1.5):
    """fabric ribbon with folded tails and a stitched edge - for titles/FEATURED"""
    w = text_w(title, size) + size * 1.6; h = size * 1.55
    a, b, t = cloth
    x = cx - w / 2
    tails = (f'<path d="M{f(x + 10)} {f(y + 12)} H{f(x - 38)} L{f(x - 18)} {f(y + h / 2 + 12)} L{f(x - 38)} {f(y + h + 12)} H{f(x + 10)} Z" fill="{b}" stroke="{t}" stroke-width="4" stroke-linejoin="round"/>'
             f'<path d="M{f(x + w - 10)} {f(y + 12)} H{f(x + w + 38)} L{f(x + w + 18)} {f(y + h / 2 + 12)} L{f(x + w + 38)} {f(y + h + 12)} H{f(x + w - 10)} Z" fill="{b}" stroke="{t}" stroke-width="4" stroke-linejoin="round"/>')
    body = f'M{f(x)} {f(y)} Q{f(cx)} {f(y - 10)} {f(x + w)} {f(y)} V{f(y + h)} Q{f(cx)} {f(y + h - 10)} {f(x)} {f(y + h)} Z'
    g = d.lin([(0, a), (.55, a), (.55, b), (1, b)])
    return (f'<g id="Banner {title}" transform="rotate({rot} {f(cx)} {f(y + h / 2)})">{tails}'
            f'<path d="{body}" transform="translate(0 6)" fill="{t}" fill-opacity=".45"/>'
            f'<path d="{body}" fill="{g}" stroke="{t}" stroke-width="4.5" stroke-linejoin="round"/>'
            f'<path d="M{f(x + 8)} {f(y + 7)} Q{f(cx)} {f(y - 3)} {f(x + w - 8)} {f(y + 7)}" fill="none" stroke="#FFFFFF" stroke-opacity=".45" stroke-width="2.5" stroke-dasharray="7 6"/>'
            f'<path d="M{f(x + 8)} {f(y + h - 7)} Q{f(cx)} {f(y + h - 17)} {f(x + w - 8)} {f(y + h - 7)}" fill="none" stroke="{t}" stroke-opacity=".5" stroke-width="2.5" stroke-dasharray="7 6"/>'
            + T(cx, y + h / 2 + size * .33, title, size, outline=t) + '</g>')

def oak_card(d, x, y, w, h, name='Card', corners=True, tone=None):
    tone = tone or OAK
    return planks(d, x, y, w, h, tone=tone, ph=h / max(2, round(h / 70)), r=14, name=name, nails=None) + (iron_corners(x, y, w, h, 26) if corners else '')
