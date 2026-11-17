"""Screen 7 v2 - egg hatchery: stone frame (ref_1 language), egg on a stone pedestal with one light beam,
chance list on oak boards with gem studs (odds are required for paid random items), hatch buttons."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'kit'))
from uikit import *
from materials import *
from themes import THEMES

W, H = 1260, 800
d = Doc(W, H, bg=('#7FD3FF', '#3D8F4A'), seed=31)
FX, FY, FW, FH = 70, 110, 1120, 640
d.add(frame(d, FX, FY, FW, FH, THEMES['stone'], title=None))
d.add(hanging_sign(d, W / 2, FY - 70, 'MYSTIC EGG', tone=WALNUT, size=42))
ex, ey = FX + 290, FY + 290
cp = d.clip(rr(FX + 22, FY + 22, 520, FH - 44, 26))
d.add(f'<g clip-path="{cp}"><path d="M{ex - 70} {FY} L{ex + 70} {FY} L{ex + 190} {ey + 200} L{ex - 190} {ey + 200} Z" fill="#FFFFFF" fill-opacity=".14"/>'
      f'<circle cx="{ex}" cy="{ey}" r="210" fill="{d.rad([(0, "#FFFFFF80"), (1, "#FFFFFF00")])}"/></g>')
d.add(plate(d, ex - 130, ey + 140, 260, 64, tone=dict(a='#B9B4C0', b='#8C8794', d='#625D6B', t='#2E2A33'), r=14, name='Pedestal'))
d.add(item_img('egg', ex, ey + 25, 270))
d.add(plate(d, FX + 50, FY + 46, 240, 52, name='Coins'), coin(FX + 82, FY + 72, 20), T(FX + 190, FY + 84, '82,450', 26, outline=IRON['t']))
lx, lw = FX + 580, FW - 620
d.add(plate(d, lx, FY + 46, lw, 54, tone=WALNUT and BRASS, name='Chances'), T(lx + lw / 2, FY + 84, 'Chances', 30, outline=BRASS['t']))
odds = [('coin', 'Gold Coin', 'Common', '60%'), ('shield', 'Guardian', 'Rare', '25%'), ('potion', 'Rage Brew', 'Epic', '10%'),
        ('sword', 'Starfall', 'Legendary', '4.9%'), ('crown', 'Royal Crown', 'Mythic', '0.1%')]
for k, (ren, name, rar, pct) in enumerate(odds):
    y = FY + 116 + k * 76
    rp = PAL[RARITY[rar]]
    d.add(planks(d, lx, y, lw, 66, tone=OAK, ph=33, r=12, name='Odds ' + name, nails=None))
    d.add(item_window(d, lx + 40, y + 33, 52, ren, rp, rar == 'Mythic', base=('#24150B', '#3E2615'), out=OAK['t'], r=10))
    d.add(T(lx + 80, y + 42, name, 24, outline=OAK['t'], anchor='start'))
    d.add(gem_stud(lx + 290, y + 33, rp, 9))
    d.add(T(lx + 310, y + 41, rar, 19, fill=rainbow(d) if rar == 'Mythic' else rp['a'], outline=rp['t'] if rar != 'Mythic' else NAVY, anchor='start'))
    d.add(T(lx + lw - 22, y + 44, pct, 28, fill='#FFF04A', outline=OAK['t'], anchor='end'))
by = FY + FH - 146
bw = (lw - 2 * 14) / 3
for k, (lab, cost, col, ic) in enumerate((('Hatch 1', '1K', 'green', 'egg'), ('Hatch 3', '2.7K', 'blue', 'egg'), ('Auto', None, 'purple', 'gear'))):
    x = lx + k * (bw + 14)
    d.add(button(d, x, by, bw, 74, PAL[col], lab, icon=ic))
    d.add(price(d, x + 22, by + 84, bw - 44, 38, cost or 299, PAL['gold'] if cost else PAL['purple'], currency='coin' if cost else 'robux'))
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.')
d.save(f'{out}/egg_hatch_v2.svg'); render(f'{out}/egg_hatch_v2.svg', f'{out}/egg_hatch_v2.png'); print('ok')
