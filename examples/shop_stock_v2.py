"""Screen 2 v2 - seed shop as a real market stall: canvas awning, posts, hanging plank sign,
plank-textured counter, produce sitting in soil crates. Item art = Blender voxel renders."""
import os, sys, base64, io
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'kit'))
from uikit import *
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
REN = os.path.join(HERE, '..', 'pack', 'fruits-voxel')
WOOD = dict(a='#C98A52', b='#A86A36', d='#7A4520', t='#3B1E0C')
OUT = WOOD['t']

def outlined(name, col=(43, 22, 9, 255), px=9):
    im = Image.open(os.path.join(REN, name + '.png')).convert('RGBA')
    a = im.split()[3].point(lambda v: 255 if v > 40 else 0)
    ol = Image.new('RGBA', im.size, col); ol.putalpha(a.filter(ImageFilter.MaxFilter(px)))
    im = Image.alpha_composite(ol, im); im = im.crop(im.getbbox())
    b = io.BytesIO(); im.save(b, 'PNG')
    return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode(), im.size

def img(name, cx, cy, size):
    uri, (w, h) = outlined(name)
    k = size / max(w, h)
    return f'<image href="{uri}" x="{f(cx - w * k / 2)}" y="{f(cy - h * k / 2)}" width="{f(w * k)}" height="{f(h * k)}"/>'

def planks(d, x, y, w, h, tone=WOOD, ph=34, r=18, name='Planks', nails='ends'):
    """horizontal planks: per-plank tint, dark gaps, grain strokes, knots, nail heads"""
    cp = d.clip(rr(x, y, w, h, r))
    o = [f'<g id="{name}"><rect x="{f(x)}" y="{f(y + 8)}" width="{f(w)}" height="{f(h)}" rx="{r}" fill="{OUT}" fill-opacity=".5"/>',
         f'<g clip-path="{cp}"><rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="{tone["b"]}"/>']
    k, py = 0, y
    while py < y + h:
        tint = (tone['a'], tone['b'], '#B87A44')[k % 3]
        o.append(f'<rect x="{f(x)}" y="{f(py)}" width="{f(w)}" height="{f(ph)}" fill="{tint}"/>')
        o.append(f'<rect x="{f(x)}" y="{f(py)}" width="{f(w)}" height="4" fill="#FFFFFF" fill-opacity=".18"/>')
        for g in range(3):
            gx = x + d.rng.uniform(0, w * .7); gl = d.rng.uniform(w * .12, w * .3); gy = py + d.rng.uniform(9, ph - 8)
            o.append(f'<path d="M{f(gx)} {f(gy)} q{f(gl / 2)} {f(d.rng.uniform(-3, 3))} {f(gl)} 0" fill="none" stroke="{tone["d"]}" stroke-opacity=".45" stroke-width="2.2" stroke-linecap="round"/>')
        if d.rng.random() < .4:
            kx = x + d.rng.uniform(30, w - 30)
            o.append(f'<ellipse cx="{f(kx)}" cy="{f(py + ph / 2)}" rx="7" ry="4" fill="none" stroke="{tone["d"]}" stroke-opacity=".6" stroke-width="2.4"/>')
        seam = x + d.rng.uniform(w * .25, w * .75)
        o.append(f'<path d="M{f(seam)} {f(py)} v{ph}" stroke="{tone["t"]}" stroke-opacity=".55" stroke-width="3"/>')
        o.append(f'<rect x="{f(x)}" y="{f(py + ph - 3)}" width="{f(w)}" height="3" fill="{tone["t"]}" fill-opacity=".6"/>')
        for nx in ((x + 16, x + w - 16) if nails == 'ends' else ()):
            o.append(f'<circle cx="{f(nx)}" cy="{f(py + ph / 2)}" r="3" fill="#D8D0C4" stroke="{tone["t"]}" stroke-width="1.6"/>')
        py += ph; k += 1
    o.append(f'</g><rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{r}" fill="none" stroke="{OUT}" stroke-width="6"/></g>')
    return ''.join(o)

def awning(d, x, y, w, h, n=9, c1='#2F9E44', c2='#F4F1E6'):
    """canvas awning: alternating stripes, scalloped bottom, fold shading, wooden bar on top"""
    sw = w / n
    o = ['<g id="Awning">']
    for i in range(n):
        sx = x + i * sw
        col = c1 if i % 2 == 0 else c2
        sh = '#1F7A33' if i % 2 == 0 else '#D9D3C0'
        scal = f'M{f(sx)} {f(y)} H{f(sx + sw)} V{f(y + h)} Q{f(sx + sw / 2)} {f(y + h + sw * .55)} {f(sx)} {f(y + h)} Z'
        o.append(f'<path d="{scal}" transform="translate(0 7)" fill="{OUT}" fill-opacity=".35"/>')
        o.append(f'<path d="{scal}" fill="{col}" stroke="{OUT}" stroke-width="4" stroke-linejoin="round"/>')
        o.append(f'<path d="M{f(sx + sw * .72)} {f(y + 4)} V{f(y + h + sw * .1)}" stroke="{sh}" stroke-width="{f(sw * .22)}" stroke-opacity=".8"/>')
        o.append(f'<path d="M{f(sx + sw * .2)} {f(y + 8)} V{f(y + h * .55)}" stroke="#FFFFFF" stroke-width="4" stroke-opacity=".35" stroke-linecap="round"/>')
    o.append(planks(d, x - 26, y - 34, w + 52, 40, ph=40, r=12, name='Awning Bar'))
    o.append('</g>')
    return ''.join(o)

def post(d, x, y, h):
    return planks(d, x, y, 34, h, tone=dict(a='#B07440', b='#94592A', d='#6B3A17', t=OUT), ph=h, r=8, name='Post')

def hanging_sign(d, cx, y, title):
    size = 44
    w = text_w(title, size) + 70; h = 76
    o = [f'<g id="Sign {title}">',
         f'<path d="M{f(cx - w * .32)} {f(y - 40)} L{f(cx - w * .32)} {f(y + 8)} M{f(cx + w * .32)} {f(y - 40)} L{f(cx + w * .32)} {f(y + 8)}" stroke="#7A5A34" stroke-width="5" stroke-linecap="round"/>',
         f'<g transform="rotate(-1.5 {f(cx)} {f(y + h / 2)})">',
         planks(d, cx - w / 2, y, w, h, tone=dict(a='#E0A365', b='#C98A52', d='#8E5428', t=OUT), ph=38, r=14, name='Sign Board'),
         T(cx, y + h / 2 + size * .34, title, size, fill=d.lin([(0, '#FFFFFF'), (1, '#FFE7B0')]), outline=OUT), '</g></g>']
    return ''.join(o)

def slot(d, cx, cy, s, name, rp, mythic=False):
    """item window cut INTO the plank: recessed dark wood, inner shadow, rarity glow + rays behind,
    contact shadow under the item, item breaks the top edge a little"""
    x, y, r = cx - s / 2, cy - s / 2, 18
    shape = rr(x, y, s, s, r)
    cp = d.clip(shape)
    glow_c = '#FFE14A' if mythic else rp['a']
    o = ['<g id="Item Slot">',
         f'<rect x="{f(x)}" y="{f(y)}" width="{f(s)}" height="{f(s)}" rx="{r}" fill="{d.lin([(0, "#3A1F0E"), (1, "#5E3519")])}"/>',
         f'<g clip-path="{cp}">',
         f'<circle cx="{f(cx)}" cy="{f(cy + s * .05)}" r="{f(s * .62)}" fill="{d.rad([(0, glow_c + "C0"), (.6, rp["b"] + "55"), (1, rp["b"] + "00")])}"/>',
         sunburst(cx, cy + s * .05, s * .8, 12, '#FFFFFF', .12),
         f'<rect x="{f(x - 6)}" y="{f(y - 6)}" width="{f(s + 12)}" height="{f(s + 12)}" rx="{r + 4}" fill="none" stroke="#000" stroke-opacity=".45" stroke-width="16" transform="translate(0 5)"/>',
         '</g>',
         f'<ellipse cx="{f(cx)}" cy="{f(y + s * .86)}" rx="{f(s * .3)}" ry="{f(s * .07)}" fill="#000" fill-opacity=".38"/>',
         img(name, cx, cy - s * .04, s * .9),
         f'<rect x="{f(x)}" y="{f(y)}" width="{f(s)}" height="{f(s)}" rx="{r}" fill="none" stroke="{OUT}" stroke-width="5"/>',
         f'<path d="M{f(x + r)} {f(y + s + 3)} H{f(x + s - r)}" stroke="#FFF3DC" stroke-opacity=".7" stroke-width="3" stroke-linecap="round"/>',
         '</g>']
    return ''.join(o)

W, H = 1120, 980
d = Doc(W, H, bg=('#9FD7F2', '#5DAE58'), seed=5)
FX, FY, FW, FH = 70, 150, 980, 790
d.add(post(d, FX - 8, FY - 40, FH + 40), post(d, FX + FW - 26, FY - 40, FH + 40))
d.add(planks(d, FX + 14, FY + 30, FW - 28, FH - 30, name='Stall Back'))
d.add(f'<rect x="{FX + 34}" y="{FY + 110}" width="{FW - 68}" height="{FH - 220}" rx="18" fill="#2A1508" fill-opacity=".28"/>')
d.add(awning(d, FX - 30, FY - 46, FW + 60, 70))
d.add(hanging_sign(d, W / 2, FY + 46, 'SEED SHOP'))
d.add(close_button(d, FX + FW - 40, FY - 76, 70))
d.add(timer(d, FX + 175, FY + 84, 'Restock 02:41', dict(a='#5A3A22', b='#3B2414', d='#24150B', t='#120A04'), size=21))

rows = [('Carrot', 'carrot', 'Common', 14, '120', 19), ('Moon Melon', 'melon', 'Rare', 5, '4,500', 79),
        ('Dragon Fruit', 'dragonfruit', 'Legendary', 2, '75K', 249), ('Star Berry', 'starberry', 'Mythic', 0, '1.2M', 599)]
RX, RW, RH = FX + 46, FW - 92, 128
for k, (name, ren, rar, stock, cc, rbx) in enumerate(rows):
    y = FY + 134 + k * (RH + 10)
    rp = PAL[RARITY[rar]]
    sold = stock == 0
    d.add(planks(d, RX, y, RW, RH, tone=dict(a='#F2D3A2', b='#E2BC84', d='#B88A52', t=OUT), ph=RH / 2, r=16, name='Row ' + name, nails=None))
    d.add(f'<rect x="{RX + 3}" y="{y + 3}" width="14" height="{RH - 6}" rx="7" fill="{rainbow(d) if rar == "Mythic" else rp["b"]}"/>')
    d.add(slot(d, RX + 92, y + RH / 2, 104, ren, rp, rar == 'Mythic'))
    d.add(T(RX + 170, y + 54, name, 32, outline=OUT, anchor='start'))
    d.add(T(RX + 170, y + 92, rar, 23, fill=rainbow(d) if rar == 'Mythic' else rp['a'], outline=rp['t'] if rar != 'Mythic' else NAVY, anchor='start'))
    d.add(T(RX + 490, y + 46, 'SOLD OUT' if sold else f'x{stock} in stock', 21, fill='#FF7070' if sold else '#FFFFFF', outline='#5E0A17' if sold else OUT))
    bx = RX + RW - 466
    d.add(price(d, bx, y + 60, 188, 52, cc, PAL['grey'] if sold else PAL['green'], currency='coin'))
    d.add(price(d, bx + 198, y + 60, 166, 52, rbx, PAL['purple']))
    d.add(icon_button(d, bx + 376, y + 54, 60, PAL['purple'], 'gift'))
    if sold:
        d.add(f'<rect x="{RX}" y="{y}" width="{RW}" height="{RH}" rx="16" fill="#1B0E05" fill-opacity=".22"/>')

by = FY + FH - 96
d.add(stat_pill(d, FX + 64, by + 14, 260, 56, coin(FX + 70, by + 42, 30), '82,450'))
d.add(button(d, FX + FW - 410, by + 2, 340, 76, PAL['purple'], 'Restock Now', icon='clock'))

out = os.path.join(HERE, '.')
d.save(f'{out}/shop_stock_v2.svg'); render(f'{out}/shop_stock_v2.svg', f'{out}/shop_stock_v2.png'); print('ok')
