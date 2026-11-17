"""Screen 6 v2 - daily rewards as a calendar pinned on a wooden board: oak day tiles,
claimed = darker + stamped tick, today = brass frame + CLAIM ribbon, day 7 big gold tile."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'kit'))
from uikit import *
from materials import *

W, H = 1240, 840
d = Doc(W, H, bg=('#9FD7F2', '#5DAE58'), seed=21)
BX, BY, BW, BH = 60, 150, 1120, 640
d.add(planks(d, BX, BY, BW, BH, tone=WOOD, ph=44, r=22, name='Board', nails='ends'))
d.add(hanging_sign(d, W / 2, BY - 96, 'DAILY REWARDS', tone=WALNUT, size=44))
d.add(close_button(d, BX + BW - 44, BY - 30, 70))
d.add(plate(d, BX + 40, BY + 26, 420, 56, tone=WALNUT and IRON, name='Streak'))
d.add(T(BX + 110, BY + 64, 'Streak', 26, outline=IRON['t']))
d.add(pill_bar(d, BX + 180, BY + 34, 260, 40, 3 / 7, PAL['orange'], '3 / 7'))
rew = [('coin', '500', 'gold'), ('gem', '25', 'cyan'), ('potion', 'x2', 'pink'), ('coin', '2,500', 'gold'), ('egg', 'x1', 'blue'), ('gem', '100', 'cyan')]
today, cw, ch, gap = 3, 206, 238, 18
for k, (ren, amt, col) in enumerate(rew):
    x = BX + 40 + (k % 3) * (cw + gap); y = BY + 110 + (k // 3) * (ch + gap)
    claimed, now = k < today, k == today
    tone = dict(OAK, a='#D8B98C', b='#C9A576') if claimed else OAK
    d.add(oak_card(d, x, y, cw, ch, f'Day {k + 1}', tone=tone))
    if now:
        d.add(f'<rect x="{x - 6}" y="{y - 6}" width="{cw + 12}" height="{ch + 12}" rx="18" fill="none" stroke="{BRASS["b"]}" stroke-width="7"/>'
              f'<rect x="{x - 6}" y="{y - 6}" width="{cw + 12}" height="{ch + 12}" rx="18" fill="none" stroke="{BRASS["t"]}" stroke-width="2.5"/>')
        d.add(cloth_banner(d, x + cw / 2, y - 26, 'CLAIM', cloth=('#4CCB4A', '#2E9A33', '#13401A'), size=22))
    d.add(T(x + cw / 2, y + 42, f'Day {k + 1}', 28, outline=OAK['t'], rot=(-2, 1, -1, 2, -2, 1)[k]))
    d.add(item_window(d, x + cw / 2, y + 120, 112, ren, PAL[col], base=('#24150B', '#3E2615'), out=OAK['t']))
    d.add(T(x + cw / 2, y + 212, amt, 28, outline=OAK['t']))
    if claimed:
        d.add(f'<g transform="rotate(-14 {x + cw / 2} {y + 120})"><rect x="{x + cw / 2 - 66}" y="{y + 96}" width="132" height="48" rx="8" fill="none" stroke="#C8102E" stroke-width="5" stroke-opacity=".85"/>'
              + T(x + cw / 2, y + 131, 'CLAIMED', 26, fill='#E0283E', outline='#FFFFFF', ow=4) + '</g>')
x = BX + 40 + 3 * (cw + gap) + 6
y, w, h = BY + 110, BX + BW - 40 - x, 2 * ch + gap
d.add(oak_card(d, x, y, w, h, 'Day 7', tone=dict(OAK, a='#F6DFB4', b='#E9C88F')))
d.add(f'<rect x="{x + 4}" y="{y + 4}" width="{w - 8}" height="{h - 8}" rx="11" fill="none" stroke="{BRASS["b"]}" stroke-width="6"/>')
d.add(T(x + w / 2, y + 56, 'Day 7', 44, fill=d.lin([(0, '#FFFFFF'), (1, '#FFE7B0')]), outline=OAK['t'], rot=-2))
d.add(item_window(d, x + w / 2, y + 220, 230, 'crown', PAL['gold'], True, base=('#24150B', '#3E2615'), out=OAK['t']))
d.add(T(x + w / 2, y + 384, 'Royal Crown', 32, outline=OAK['t']))
d.add(T(x + w / 2, y + 418, 'MYTHIC', 24, fill=rainbow(d), outline=NAVY))
d.add(plate(d, x + 30, y + h - 64, w - 60, 44, name='Next'), T(x + w / 2, y + h - 33, 'Next 14:22:05', 21, fill='#FFE14A', outline=IRON['t']))
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.')
d.save(f'{out}/daily_rewards_v2.svg'); render(f'{out}/daily_rewards_v2.svg', f'{out}/daily_rewards_v2.png'); print('ok')
