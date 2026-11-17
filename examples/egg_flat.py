"""Colourful Roblox-flat egg shop (language studied from Throw Food for Animals): thick black outlines,
flat panel with a faint background scene, rays behind the egg, tiles that GROW with rarity, % above,
stat pill inside, rainbow border on the rarest, lime buy buttons x1/x3/x10, hand-placed 4-point sparkles."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'kit'))
from uikit import Doc, render, item_img, rainbow, rr, f, sunburst, glow
from flat import *
import text_paths as TP

W, H = 1500, 660
d = Doc(W, H, seed=50)
PX, PY, PW, PH = 10, 10, W - 20, H - 20
cp = d.clip(rr(PX, PY, PW, PH, 26))
bg = d.lin([(0, '#5FD4FF'), (1, '#1E7BE0')])
scene = [f'<rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" fill="{bg}"/>']
# faint background world: ice peaks + floating island silhouettes, low contrast
for k, (cx, w_, h_) in enumerate(((980, 300, 260), (1200, 380, 330), (1400, 260, 220), (760, 220, 170))):
    scene.append(f'<path d="M{cx - w_ / 2} {PY + PH} L{cx} {PY + PH - h_} L{cx + w_ / 2} {PY + PH} Z" fill="#FFFFFF" fill-opacity=".13"/>')
    scene.append(f'<path d="M{cx - w_ * .12} {PY + PH - h_ * .76} L{cx} {PY + PH - h_} L{cx + w_ * .12} {PY + PH - h_ * .76} L{cx + w_ * .04} {PY + PH - h_ * .7} L{cx - w_ * .05} {PY + PH - h_ * .78} Z" fill="#FFFFFF" fill-opacity=".18"/>')
for cx, cy, r in ((1180, 120, 46), (1250, 100, 36), (1120, 110, 30), (640, 90, 34), (690, 76, 26)):
    scene.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#FFFFFF" fill-opacity=".14"/>')
scene.append(sunburst(250, 330, 520, 16, '#FFFFFF', .16))
scene.append(glow(d, 250, 330, 230, '#FFFFFF', .55))
d.add(f'<g clip-path="{cp}">{"".join(scene)}</g>')
d.add(f'<rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" rx="26" fill="none" stroke="{K}" stroke-width="7"/>')

# title + New! + odds
d.add(txt(40, 98, 'FROST EGG', 76, fill=title_fill(d), anchor='start', rot=-1))
nx = 40 + TP.width('FROST EGG', 76) + 0.02 * 76 * 8 + 22
d.add(f'<rect x="{nx}" y="40" width="150" height="66" rx="16" fill="#1A1A2E" stroke="{rainbow(d)}" stroke-width="8"/>'
      f'<rect x="{nx - 4}" y="36" width="158" height="74" rx="19" fill="none" stroke="{K}" stroke-width="3"/>')
d.add(txt(nx + 75, 86, 'New!', 38))
d.add(box(d, W - 300, 30, 262, 74, '#2B2F4A', '#1C1F33', r=18, sw=5, sheen=False, name='Odds'))
d.add(txt(W - 169, 80, 'ODDS', 36))

# egg
d.add(item_img('egg', 250, 340, 330, outline=(0, 0, 0, 255), px=11))
# crystal cluster bottom-left (2D, black outline)
for cx, h_, wd, col in ((70, 120, 40, '#9BEAFF'), (110, 160, 46, '#CFF6FF'), (150, 100, 38, '#7FD8FF'), (40, 80, 30, '#BFF2FF')):
    by = PY + PH - 6
    d.add(f'<path d="M{cx - wd / 2} {by} L{cx - wd / 2} {by - h_ * .7} L{cx} {by - h_} L{cx + wd / 2} {by - h_ * .7} L{cx + wd / 2} {by} Z" fill="{col}" stroke="{K}" stroke-width="5" stroke-linejoin="round"/>'
          f'<path d="M{cx} {by - h_} L{cx} {by}" stroke="#FFFFFF" stroke-opacity=".7" stroke-width="5"/>')

# tiles that grow with rarity
pets = [('coin', '45%', 'x1.1', 120), ('shield', '30%', 'x1.5', 126), ('potion', '15%', 'x2.5', 134),
        ('gem', '7%', 'x4', 146), ('sword', '2.9%', 'x7', 160), ('crown', '0.1%', 'x15', 182)]
x = 520
base_y = 450
for k, (ren, pct, mult, s) in enumerate(pets):
    y = base_y - s
    last = k == len(pets) - 1
    d.add(tile(d, x, y, s, base='#0D3E86', rainbow=rainbow(d) if last else None, name='Pet ' + ren))
    d.add(item_img(ren, x + s / 2, y + s * .42, s * .8, outline=(0, 0, 0, 255), px=9))
    d.add(pill(d, x + s / 2, y + s - 26, s - 22, 34))
    d.add(txt(x + s / 2, y + s - 15, mult, 26 if s < 150 else 30, fill='#FFE21A'))
    d.add(txt(x + s / 2, y - 12, pct, 30 if not last else 38, fill='#FFE21A'))
    x += s + 14

# buy buttons
bw, bh, gap = 300, 116, 22
bx0 = 520
for k, (lab, cost) in enumerate((('Buy x1', '79'), ('Buy x3', '199'), ('Buy x10', '649'))):
    bx = bx0 + k * (bw + gap)
    d.add(txt(bx + bw / 2, 504, lab, 32))
    d.add(lime(d, bx, 520, bw, bh, 'Buy ' + lab))
    d.add(robux_w(bx + 46, 548, 2.5))
    d.add(txt(bx + 190, 604, cost, 66))
    if k == 2:
        d.add(f'<g transform="rotate(10 {bx + bw - 10} 520)">{box(d, bx + bw - 90, 492, 104, 44, "#FF6B6B", "#E01E37", r=12, sw=4, sheen=False)}</g>')
        d.add(txt(bx + bw - 38, 524, '-25%', 26, rot=10))

# hand-placed sparkles (sizes and spots vary on purpose)
for cx, cy, s, c in ((470, 190, 40, '#FFE21A'), (90, 170, 30, '#FFFFFF'), (1000, 160, 28, '#FFE21A'), (1440, 170, 24, '#FFFFFF'),
                     (880, 60, 18, '#FFFFFF'), (420, 420, 22, '#FFE21A'), (1300, 250, 16, '#FFFFFF')):
    d.add(star4(cx, cy, s, c))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.')
d.save(f'{out}/egg_flat.svg'); render(f'{out}/egg_flat.svg', f'{out}/egg_flat.png'); print('ok')
