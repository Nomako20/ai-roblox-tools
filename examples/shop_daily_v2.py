"""Screen 3 v2 - daily rotating shop as an ARMORY: stone wall + torch light, walnut board with iron bands,
oak display shelves with iron corners, chained sign. Colour only as accents (gem studs, window glow, prices)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'kit'))
from uikit import *
from materials import *

W, H = 1320, 860
d = Doc(W, H, seed=3)
d.add(stone_wall(d, W, H))
d.add(torch_glow(d, 0, 140, 520), torch_glow(d, W, 140, 520))
d.add(f'<rect width="{W}" height="{H}" fill="{d.lin([(0, "#00000000"), (1, "#000000AA")])}"/>')

BX, BY, BW, BH = 60, 140, 1200, 640
d.add(planks(d, BX, BY, BW, BH, tone=WALNUT, ph=46, r=20, name='Board', nails=None))
d.add(iron_band(d, BX - 6, BY + 14, BW + 12), iron_band(d, BX - 6, BY + BH - 36, BW + 12))
d.add(iron_corners(BX, BY, BW, BH, 46))
d.add(hanging_sign(d, W / 2, BY - 92, 'ARMORY', tone=WALNUT, size=50, chain=True))
d.add(close_button(d, BX + BW - 44, BY - 30, 70))
d.add(plate(d, BX + 40, BY - 62, 300, 50, name='Timer Plate'))
d.add(glyph3d('clock', BX + 72, BY - 38, 1.05, '#FFE14A', IRON['t']))
d.add(T(BX + 200, BY - 27, 'New in 07:42:10', 24, fill='#FFE14A', outline=IRON['t']))
d.add(plate(d, BX + BW - 340, BY - 62, 250, 50, name='Gem Plate'))
d.add(gem(BX + BW - 308, BY - 38, 17, PAL['cyan']))
d.add(T(BX + BW - 200, BY - 25, '2,480', 28, outline=IRON['t']))

tabs = [('Weapons', 'sword', True), ('Armor', 'shield', False), ('Potions', 'heart', False), ('Pets', 'paw', False)]
for i, (lab, ic, act) in enumerate(tabs):
    tx = BX + 330 + i * 160
    d.add(plate(d, tx, BY + BH - 14 - (8 if act else 0), 146, 50, tone=BRASS if act else IRON, name='Tab ' + lab))
    d.add(glyph3d(ic, tx + 30, BY + BH + 9 - (8 if act else 0), 1.4, '#FFFFFF', (BRASS if act else IRON)['t']))
    d.add(T(tx + 88, BY + BH + 20 - (8 if act else 0), lab, 22, outline=(BRASS if act else IRON)['t']))

# featured
fx, fy, fw, fh = BX + 46, BY + 56, 380, 532
d.add(planks(d, fx, fy, fw, fh, tone=OAK, ph=fh / 6, r=16, name='Featured Shelf', nails=None))
d.add(iron_corners(fx, fy, fw, fh, 36))
d.add(item_window(d, fx + fw / 2, fy + 186, 300, 'sword', PAL['gold'], base=('#24150B', '#3E2615'), out=OAK['t'], item_scale=.92))
d.add(gem_stud(fx + 32, fy + 32, PAL['gold'], 14))
d.add(plate(d, fx + 30, fy + 352, fw - 60, 84, tone=BRASS, name='Name Plate'))
d.add(T(fx + fw / 2, fy + 392, 'Starfall Blade', 34, outline=BRASS['t']))
d.add(T(fx + fw / 2, fy + 424, 'Legendary', 22, fill='#FFF3B0', outline=BRASS['t']))
d.add(price(d, fx + 92, fy + fh - 80, fw - 130, 58, '1,200', PAL['purple'], currency='gem', old='1,800', old_left=True))
d.add(cloth_banner(d, fx + fw / 2, fy - 22, 'FEATURED', size=30))
d.add(tag(d, fx + fw - 44, fy + 46, '-33%', PAL['red'], rot=8, size=22))

items = [('Guardian', 'shield', 'Rare', 450, False), ('King Crown', 'crown', 'Mythic', 2500, False), ('Rage Brew', 'potion', 'Epic', 320, True),
         ('Loot Chest', 'chest', 'Legendary', 900, False), ('Pet Egg', 'egg', 'Uncommon', 150, False), ('Gold Coin', 'coin', 'Common', 60, False)]
gx0, gy0 = fx + fw + 26, fy
cw, ch, gap = (BX + BW - 46 - gx0 - 2 * 18) / 3, 258, 16
for k, (name, ren, rar, cost, owned) in enumerate(items):
    x = gx0 + (k % 3) * (cw + gap); y = gy0 + (k // 3) * (ch + gap)
    rp = PAL[RARITY[rar]]
    d.add(planks(d, x, y, cw, ch, tone=OAK, ph=ch / 4, r=14, name='Shelf ' + name, nails=None))
    d.add(iron_corners(x, y, cw, ch, 26))
    d.add(item_window(d, x + cw / 2, y + 76, 124, ren, rp, rar == 'Mythic', base=('#24150B', '#3E2615'), out=OAK['t']))
    d.add(gem_stud(x + 24, y + 24, rp, 10))
    d.add(T(x + cw / 2, y + 166, name, 26, outline=OAK['t']))
    d.add(T(x + cw / 2, y + 190, rar, 18, fill=rainbow(d) if rar == 'Mythic' else rp['a'], outline=rp['t'] if rar != 'Mythic' else NAVY))
    if owned:
        d.add(plate(d, x + 22, y + ch - 50, cw - 44, 38, name='Owned', rivets=False))
        d.add(T(x + cw / 2, y + ch - 22, 'OWNED', 22, fill='#C9D2DE', outline=IRON['t']))
    else:
        d.add(price(d, x + 22, y + ch - 52, cw - 44, 40, cost, PAL['purple'], currency='gem'))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.')
d.save(f'{out}/shop_daily_v2.svg'); render(f'{out}/shop_daily_v2.svg', f'{out}/shop_daily_v2.png'); print('ok')
