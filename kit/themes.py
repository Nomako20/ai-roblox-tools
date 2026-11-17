"""World themes for frames. A theme = colours + an 'edge' painter (objects around the border)
+ a 'top' painter (decoration hugging the top edge). Add a new world by copying one entry.
Rule: decoration scales with the element and is never identical on two elements."""
import math
from uikit import f, PAL, gem

def _stones(d, x, y, w, h):
    """stone blocks of different sizes along the border, gems stuck between some of them"""
    o, rng = [], d.rng
    def block(bx, by, bw, bh):
        o.append(f'<rect x="{f(bx)}" y="{f(by + 4)}" width="{f(bw)}" height="{f(bh)}" rx="9" fill="#2E2A33"/>'
                 f'<rect x="{f(bx)}" y="{f(by)}" width="{f(bw)}" height="{f(bh)}" rx="9" fill="#8C8794" stroke="#2E2A33" stroke-width="4"/>'
                 f'<rect x="{f(bx + 4)}" y="{f(by + 4)}" width="{f(bw - 8)}" height="{f(bh * .35)}" rx="6" fill="#B9B4C0"/>'
                 f'<path d="M{f(bx + 6)} {f(by + bh - 7)} H{f(bx + bw - 8)}" stroke="#625D6B" stroke-width="5" stroke-linecap="round"/>')
    for edge in ('top', 'bottom', 'left', 'right'):
        pos = 0
        L = w if edge in ('top', 'bottom') else h
        while pos < L - 20:
            ln = min(rng.uniform(60, 120), L - pos)
            th = rng.uniform(26, 34)
            if edge == 'top': block(x + pos, y - th * .45, ln - 4, th)
            elif edge == 'bottom': block(x + pos, y + h - th * .55, ln - 4, th)
            elif edge == 'left': block(x - th * .45, y + pos, th, ln - 4)
            else: block(x + w - th * .55, y + pos, th, ln - 4)
            pos += ln
    gems_at = [(x + 6, y + h * .3, 'cyan'), (x + w - 4, y + h * .62, 'purple'), (x + w * .08, y + h - 4, 'orange'),
               (x + w * .9, y + 2, 'green'), (x - 2, y + h * .78, 'pink')]
    for gx, gy, c in gems_at:
        o.append(f'<g transform="rotate({rng.uniform(-25, 25):.0f} {f(gx)} {f(gy)})">{gem(gx, gy, rng.uniform(22, 30), PAL[c])}</g>')
    return ''.join(o)

def _planks(d, x, y, w, h):
    o = []
    for i in range(1, int(w / 140)):
        px = x + i * 140 + d.rng.uniform(-20, 20)
        o.append(f'<path d="M{f(px)} {f(y + 3)} V{f(y + 17)} M{f(px)} {f(y + h - 17)} V{f(y + h - 3)}" stroke="#4A2410" stroke-width="3"/>')
    for cx, cy in ((x + 12, y + 12), (x + w - 12, y + 12), (x + 12, y + h - 12), (x + w - 12, y + h - 12)):
        o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="5" fill="#C9C2B8" stroke="#3A1D0C" stroke-width="2.5"/>')
    return ''.join(o)

def _leaves(d, x, y, w):
    o, rng = [], d.rng
    for cx in (x + 40, x + w * .33, x + w * .72, x + w - 50):
        n = rng.randint(3, 5)
        for k in range(n):
            a = -90 + (k - n / 2) * 28 + rng.uniform(-8, 8)
            L = rng.uniform(22, 34)
            ex, ey = cx + math.cos(math.radians(a)) * L, y + 4 + math.sin(math.radians(a)) * L
            o.append(f'<path d="M{f(cx)} {f(y + 6)} Q{f((cx + ex) / 2 - 9)} {f((y + ey) / 2)} {f(ex)} {f(ey)} Q{f((cx + ex) / 2 + 9)} {f((y + ey) / 2)} {f(cx)} {f(y + 6)} Z" '
                     f'fill="{"#4FD13B" if k % 2 else "#2FA52B"}" stroke="#123F12" stroke-width="3" stroke-linejoin="round"/>')
    return ''.join(o)

def _frosting(d, x, y, w):
    """one shape glued to the top edge, few round drips of different length"""
    pts, rng = [f'M{f(x + 30)} {f(y - 4)}'], d.rng
    cx = x + 30
    while cx < x + w - 60:
        step = rng.uniform(46, 80)
        drip = rng.random() < .35
        dy = rng.uniform(26, 44) if drip else rng.uniform(10, 16)
        pts.append(f'Q{f(cx + step * .5)} {f(y + dy)} {f(cx + step)} {f(y + 6)}')
        cx += step
    pts.append(f'L{f(x + w - 30)} {f(y - 4)} Q{f(x + w / 2)} {f(y - 14)} {f(x + 30)} {f(y - 4)} Z')
    p = ' '.join(pts)
    return (f'<path d="{p}" transform="translate(0 5)" fill="#7A1650" fill-opacity=".4"/><path d="{p}" fill="#FFF0FA" stroke="#5C0B3D" stroke-width="5" stroke-linejoin="round"/>'
            + ''.join(f'<rect x="{f(x + rng.uniform(60, w - 60))}" y="{f(y + rng.uniform(-6, 4))}" width="10" height="4" rx="2" fill="{c}" transform="rotate({rng.randint(-40, 40)} {f(x + w / 2)} {f(y)})"/>'
                      for c in ('#FF4D6D', '#2FA8FF', '#FFD12E', '#3EE07A', '#B24DFF', '#FF4D6D', '#2FA8FF')))

def _neon_edge(d, x, y, w, h):
    o = [f'<rect x="{f(x + 10)}" y="{f(y + 10)}" width="{f(w - 20)}" height="{f(h - 20)}" rx="32" fill="none" stroke="#3CF2FF" stroke-width="3" stroke-opacity=".9"/>',
         f'<rect x="{f(x + 10)}" y="{f(y + 10)}" width="{f(w - 20)}" height="{f(h - 20)}" rx="32" fill="none" stroke="#3CF2FF" stroke-width="12" stroke-opacity=".18"/>']
    for cx, cy in ((x + 26, y + 26), (x + w - 26, y + 26), (x + 26, y + h - 26), (x + w - 26, y + h - 26)):
        o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="6" fill="#6B7390" stroke="#05060C" stroke-width="3"/>')
    return ''.join(o)

THEMES = {
    'stone':  dict(out='#2E2A33', rim=('#B9B4C0', '#77727F'), panel=('#3FB4FF', '#1C6FD1'), accent='orange', edge=_stones),
    'wood':   dict(out='#3A1D0C', rim=('#D08A4E', '#8E4F22'), panel=('#FFF1D2', '#F5D59A'), accent='green', edge=_planks, top=_leaves),
    'candy':  dict(out='#5C0B3D', rim=('#FFD3F0', '#FF8BD0'), panel=('#FFE3F5', '#FFB8E2'), accent='pink', top=_frosting),
    'neon':   dict(out='#05060C', rim=('#3A3F58', '#171A29'), panel=('#1D1240', '#0B0820'), accent='purple', edge=_neon_edge),
}

def _royal_edge(d, x, y, w, h):
    o = [f'<rect x="{f(x + 11)}" y="{f(y + 11)}" width="{f(w - 22)}" height="{f(h - 22)}" rx="31" fill="none" stroke="#FFD34D" stroke-width="3"/>']
    for k in range(int(w / 90)):
        cx = x + 45 + k * 90
        for cy in (y + 10, y + h - 10):
            o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="5" fill="#FFE27A" stroke="#5A3300" stroke-width="2.5"/>')
    for cx, cy in ((x + 8, y + 8), (x + w - 8, y + 8), (x + 8, y + h - 8), (x + w - 8, y + h - 8)):
        o.append(f'<path d="M{f(cx - 22)} {f(cy)} L{f(cx)} {f(cy - 22)} L{f(cx + 22)} {f(cy)} L{f(cx)} {f(cy + 22)} Z" fill="#FFC21A" stroke="#5A3300" stroke-width="4" stroke-linejoin="round"/>'
                 f'<circle cx="{f(cx)}" cy="{f(cy)}" r="6" fill="#FF3B5C" stroke="#5A3300" stroke-width="2.5"/>')
    return ''.join(o)

THEMES['royal'] = dict(out='#140C2E', rim=('#3A3D8F', '#1B1C52'), panel=('#2D5FD6', '#16307A'), accent='gold', edge=_royal_edge)
