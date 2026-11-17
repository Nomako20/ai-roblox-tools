"""Screen 1 v2 - simulator mega shop in the material language: stone + gem frame, walnut inside,
side plank tabs, cloth section banners, oak offer boards, gamepasses in item windows with brass value plates."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'kit'))
from uikit import *
from materials import *
from themes import THEMES

W, H = 1300, 820
d = Doc(W, H, bg=('#7FD3FF', '#5FBF5A'), seed=14)
th = dict(THEMES['stone'], panel=('#6E4227', '#4A2A16'))
FX, FY, FW, FH = 70, 110, 1160, 670
d.add(frame(d, FX, FY, FW, FH, th, title=None))
d.add(hanging_sign(d, W / 2, FY - 76, 'SHOP', tone=WALNUT, size=50))

# side plank tabs (style 1)
tabs = [('Featured', 'star'), ('Passes', 'crown'), ('Boosts', 'bolt'), ('Coins', 'bag')]
for i, (lab, ic) in enumerate(tabs):
    act = i == 0
    w = 200 if act else 172
    x, y = FX + 30 + (0 if act else 12), FY + 52 + i * 84
    tone = BRASS if act else OAK
    d.add(planks(d, x, y, w, 68, tone=tone, ph=34, r=12, nails=None, name='Tab ' + lab))
    d.add(glyph3d(ic, x + 34, y + 32, 1.5, '#FFFFFF', tone['t']))
    d.add(T(x + 118, y + 44, lab, 25 if act else 22, outline=tone['t']))
    if lab == 'Boosts':
        d.add(notif_dot(x + w - 4, y + 4, 2))

CX, CW = FX + 262, FW - 300
clip = d.clip(rr(CX - 12, FY + 22, CW + 24, FH - 44, 22))
c = [f'<g clip-path="{clip}">']
# hero: server luck boost on a walnut board, one window
hx, hy, hw, hh = CX, FY + 40, CW * .54, 212
c.append(oak_card(d, hx, hy, hw, hh, 'Hero Luck', tone=dict(OAK, a='#F6DFB4', b='#E9C88F')))
c.append(item_window(d, hx + 104, hy + hh / 2, 168, 'gem', PAL['green'], base=('#24150B', '#3E2615'), out=OAK['t']))
c.append(T(hx + 200, hy + 56, 'Server Luck', 34, outline=OAK['t'], anchor='start', rot=-1))
c.append(T(hx + 200, hy + 106, '1x', 40, outline=OAK['t'], anchor='start'))
c.append(glyph3d('play', hx + 276, hy + 93, 1.2, '#FFFFFF', OAK['t']))
c.append(T(hx + 306, hy + 110, '2x', 56, fill='#7BE04A', outline='#13401A', anchor='start', rot=-4))
c.append(plate(d, hx + 200, hy + 136, 150, 46, name='Timer'))
c.append(T(hx + 275, hy + 168, '15:00', 24, fill='#FFE14A', outline=IRON['t']))
c.append(price(d, hx + hw - 170, hy + hh - 74, 150, 54, 999))

# bundle
bx, by, bw, bh = hx + hw + 16, hy, CW - hw - 16, 212
c.append(oak_card(d, bx, by, bw, bh, 'Bundle'))
c.append(T(bx + bw / 2, by + 46, 'Starter Bundle', 30, outline=OAK['t'], rot=-1))
for k, ren in enumerate(('sword', 'potion', 'chest')):
    ix = bx + 70 + k * (bw - 140) / 2
    c.append(item_window(d, ix, by + 112, 84, ren, PAL['blue'], base=('#24150B', '#3E2615'), out=OAK['t']))
    if k < 2:
        c.append(T(ix + (bw - 140) / 4, by + 124, '+', 34, outline=OAK['t']))
c.append(price(d, bx + bw - 170, by + bh - 62, 150, 48, 399, old=1200, old_left=True))

# gamepasses
y = hy + hh + 44
c.append(cloth_banner(d, CX + CW / 2, y - 22, 'Gamepasses', size=32))
y += 48
passes = [('VIP', 'crown', 'VIP', 799), ('2x Coins', 'coin', '2X', 299), ('Lucky', 'gem', '+50%', 449), ('+3 Pets', 'egg', '+3', 199)]
pw = (CW - 3 * 14) / 4
for k, (name, ren, val, cost) in enumerate(passes):
    x = CX + k * (pw + 14)
    c.append(oak_card(d, x, y, pw, 236, 'Pass ' + name))
    c.append(item_window(d, x + pw / 2, y + 82, 132, ren, PAL['purple'], base=('#24150B', '#3E2615'), out=OAK['t']))
    c.append(plate(d, x + pw - 74, y + 112, 66, 40, tone=BRASS, r=10, rivets=False, name='Value'))
    c.append(T(x + pw - 41, y + 141, val, 24 if len(val) < 4 else 19, outline=BRASS['t'], rot=-4))
    c.append(T(x + pw / 2, y + 180, name, 26, outline=OAK['t'], rot=(-2, 1, -1, 2)[k]))
    c.append(price(d, x + 18, y + 190, pw - 36, 36, cost))
y += 270
c.append(cloth_banner(d, CX + CW / 2, y - 22, 'Coins', cloth=('#E0A43A', '#B87A1E', '#3A2608'), size=32))
c.append('</g>')
d.add(''.join(c))
d.add(plate(d, FX + FW - 48, FY + 40, 16, FH - 80, r=8, rivets=False, name='Scroll Track'))
d.add(plate(d, FX + FW - 50, FY + 40, 20, (FH - 80) * .55, tone=BRASS, r=10, rivets=False, name='Scroll Thumb'))
d.add(close_button(d, FX + FW - 46, FY - 26, 70))
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.')
d.save(f'{out}/shop_stone_v2.svg'); render(f'{out}/shop_stone_v2.svg', f'{out}/shop_stone_v2.png'); print('ok')
