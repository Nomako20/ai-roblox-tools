"""Screen 5 v2 - starter pack popup as a treasure crate: walnut board, iron corners, cloth title banner,
hero chest in a big window, contents in oak windows, green price. Dimmed game behind."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'kit'))
from uikit import *
from materials import *

W, H = 1040, 840
d = Doc(W, H, seed=12)
d.add(stone_wall(d, W, H), f'<rect width="{W}" height="{H}" fill="#000" fill-opacity=".45"/>')
PX, PY, PW, PH = 90, 130, 860, 640
d.add(planks(d, PX, PY, PW, PH, tone=WALNUT, ph=48, r=24, name='Crate', nails=None))
d.add(iron_corners(PX, PY, PW, PH, 52), iron_band(d, PX - 6, PY + PH - 34, PW + 12))
d.add(cloth_banner(d, W / 2, PY - 44, 'STARTER PACK', size=48))
d.add(close_button(d, PX + PW - 44, PY - 30, 70))
d.add(item_window(d, W / 2, PY + 200, 300, 'chest', PAL['gold'], base=('#24150B', '#3E2615'), out=WALNUT['t'], item_scale=.88))
d.add(tag(d, PX + 150, PY + 110, 'x5 VALUE!', PAL['green'], rot=-10, size=32))
d.add(plate(d, PX + PW - 230, PY + 80, 170, 52, tone=BRASS, name='One Time'), T(PX + PW - 145, PY + 116, 'ONE TIME', 24, outline=BRASS['t']))
chips = [('coin', '25K', 'gold'), ('gem', '500', 'cyan'), ('potion', 'x5', 'pink'), ('egg', 'x1', 'blue')]
cw = 160
x0 = W / 2 - (4 * cw + 3 * 16) / 2
for k, (ren, amt, col) in enumerate(chips):
    x = x0 + k * (cw + 16); y = PY + 372
    d.add(oak_card(d, x, y, cw, 150, 'Chip ' + amt))
    d.add(item_window(d, x + cw / 2, y + 62, 96, ren, PAL[col], base=('#24150B', '#3E2615'), out=OAK['t']))
    d.add(T(x + cw / 2, y + 136, amt, 28, outline=OAK['t']))
d.add(price(d, W / 2 - 110, PY + PH - 108, 300, 70, 99, old=499, old_left=True))
d.add(plate(d, W / 2 - 150, PY + PH + 18, 300, 46, name='Timer'), T(W / 2, PY + PH + 50, 'Offer ends 23:59:12', 22, fill='#FFE14A', outline=IRON['t']))
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.')
d.save(f'{out}/offer_starter_v2.svg'); render(f'{out}/offer_starter_v2.svg', f'{out}/offer_starter_v2.png'); print('ok')
