"""Screen 4 v2 - season pass as a QUEST BOARD: stone wall, walnut board, oak reward plaques,
iron rail with brass level plates, premium row trimmed in brass. Colour only as accents."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'kit'))
from uikit import *
from materials import *

W, H = 1380, 860
d = Doc(W, H, seed=8)
d.add(stone_wall(d, W, H), torch_glow(d, 0, 120, 520), torch_glow(d, W, 120, 520))
d.add(f'<rect width="{W}" height="{H}" fill="{d.lin([(0, "#00000000"), (1, "#000000AA")])}"/>')
BX, BY, BW, BH = 50, 150, 1280, 660
d.add(planks(d, BX, BY, BW, BH, tone=WALNUT, ph=46, r=20, name='Board', nails=None))
d.add(iron_band(d, BX - 6, BY + 14, BW + 12), iron_band(d, BX - 6, BY + BH - 36, BW + 12), iron_corners(BX, BY, BW, BH, 46))
d.add(hanging_sign(d, W / 2, BY - 96, 'SEASON PASS', tone=WALNUT, size=46, chain=True))
d.add(close_button(d, BX + BW - 44, BY - 30, 70))
d.add(plate(d, BX + 40, BY - 62, 270, 50, name='Timer'), glyph3d('clock', BX + 72, BY - 38, 1.05, '#FFE14A', IRON['t']),
      T(BX + 185, BY - 27, 'Ends in 12d 4h', 24, fill='#FFE14A', outline=IRON['t']))

# level panel
lx, ly, lw, lh = BX + 44, BY + 60, 290, 540
d.add(oak_card(d, lx, ly, lw, lh, 'Level Panel'))
d.add(plate(d, lx + lw / 2 - 80, ly + 30, 160, 150, tone=BRASS, name='Level Plate'))
d.add(T(lx + lw / 2, ly + 132, '24', 84, fill=d.lin([(0, '#FFFFFF'), (1, '#FFE7B0')]), outline=BRASS['t']))
d.add(T(lx + lw / 2, ly + 224, 'LEVEL', 30, outline=OAK['t']))
d.add(pill_bar(d, lx + 24, ly + 248, lw - 48, 40, .72, PAL['green'], '1,450 / 2,000 XP'))
d.add(button(d, lx + 20, ly + 320, lw - 40, 84, PAL['purple'], 'PREMIUM', icon='crown'))
d.add(price(d, lx + 60, ly + 420, lw - 120, 54, 499))
d.add(T(lx + lw / 2, ly + 510, '+10 levels  299', 22, outline=OAK['t']))

tx0 = lx + lw + 34
tw = BX + BW - 46 - tx0
cw = (tw - 5 * 14) / 6
rail_y = BY + 352
free = [('coin', '5K'), ('potion', 'x3'), ('gem', '250'), ('egg', 'x1'), ('coin', '5K'), ('shield', 'NEW')]
prem = [('chest', 'x2'), ('crown', 'RARE'), ('sword', 'SKIN'), ('gem', '250'), ('chest', 'x2'), ('crown', 'RARE')]
d.add(plate(d, tx0, rail_y - 14, tw, 28, name='Rail', rivets=False))
cur = 24
for i, t in enumerate(range(21, 27)):
    x = tx0 + i * (cw + 14)
    claimed, now = t < cur, t == cur
    for row, (ren, amt) in ((0, free[i]), (1, prem[i])):
        y = BY + 74 if row == 0 else rail_y + 40
        h = 236
        d.add(oak_card(d, x, y, cw, h, f'Tier {t} {row}', tone=OAK if row == 0 else dict(OAK, a='#F6DFB4', b='#E9C88F')))
        if row == 1:
            d.add(f'<rect x="{f(x + 4)}" y="{f(y + 4)}" width="{f(cw - 8)}" height="{h - 8}" rx="11" fill="none" stroke="{BRASS["b"]}" stroke-width="5"/>')
        d.add(item_window(d, x + cw / 2, y + 92, cw - 30, ren, PAL['gold'] if row else PAL['blue'], base=('#24150B', '#3E2615'), out=OAK['t'], item_scale=.84))
        d.add(T(x + cw / 2, y + 196, amt, 28, outline=OAK['t']))
        if claimed:
            d.add(f'<rect x="{f(x)}" y="{f(y)}" width="{f(cw)}" height="{h}" rx="14" fill="#1E0F07" fill-opacity=".35"/>')
            d.add(plate(d, x + cw / 2 - 26, y + h / 2 - 34, 52, 46, tone=dict(a='#7BE05A', b='#3FB23A', d='#2A7F26', t='#13401A'), r=10, rivets=False, name='Tick'))
            d.add(glyph('check', x + cw / 2, y + h / 2 - 12, 1.15, '#FFF', '#13401A', 2.6))
        elif row == 1:
            d.add(plate(d, x + cw - 40, y + 10, 32, 32, r=8, rivets=False, name='Lock'))
            d.add(glyph('lock', x + cw - 24, y + 26, .8, '#E6ECF5', IRON['t'], 2.2))
    tone = BRASS if now else IRON
    d.add(plate(d, x + cw / 2 - 30, rail_y - 26, 60, 50, tone=tone, r=10, rivets=False, name=f'Node {t}'))
    d.add(T(x + cw / 2, rail_y + 9, str(t), 26, outline=tone['t']))
    if now:
        d.add(cloth_banner(d, x + cw / 2, BY + 44, 'CLAIM', cloth=('#4CCB4A', '#2E9A33', '#13401A'), size=24))
for lab, y in (('FREE', BY + 74), ('PREMIUM', rail_y + 40)):
    d.add(tag(d, tx0 + 40, y - 2, lab, PAL['blue'] if lab == 'FREE' else PAL['gold'], rot=-10, size=18))
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.')
d.save(f'{out}/battle_pass_v2.svg'); render(f'{out}/battle_pass_v2.svg', f'{out}/battle_pass_v2.png'); print('ok')
