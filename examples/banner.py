"""README hero banner: title + three best screens fanned out."""
import os, sys, base64, io
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'kit'))
from uikit import Doc, render, sunburst, glow
from PIL import Image
import flat

HERE = os.path.dirname(os.path.abspath(__file__))

def shot(name, cx, cy, w, rot):
    im = Image.open(os.path.join(HERE, name + '.png')).convert('RGBA')
    im.thumbnail((900, 900))
    b = io.BytesIO(); im.save(b, 'PNG')
    uri = 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()
    h = w * im.height / im.width
    return (f'<g transform="rotate({rot} {cx} {cy})">'
            f'<rect x="{cx - w / 2 + 10}" y="{cy - h / 2 + 18}" width="{w}" height="{h}" rx="18" fill="#000" fill-opacity=".45"/>'
            f'<image href="{uri}" x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}"/>'
            f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="6" fill="none" stroke="#000" stroke-width="5"/></g>')

W, H = 1600, 760
d = Doc(W, H, bg=('#2A1A6E', '#0D0A24'))
d.add(sunburst(W / 2, 760, 1400, 26, '#7A5CFF', .09), glow(d, W / 2, 520, 620, '#7A5CFF', .35))
d.add(shot('egg_hatch_v2', 330, 500, 560, -7), shot('shop_daily_v2', 1270, 500, 560, 7), shot('shop_stock_v2', W / 2, 470, 600, 0))
d.add(flat.txt(W / 2, 118, 'AI Roblox Tools', 96, fill=flat.title_fill(d)))
d.add(flat.txt(W / 2, 178, 'Roblox UI that looks like the big games', 38, fill='#FFF8E6'))
for cx, cy, s, c in ((210, 90, 26, '#FFE21A'), (1390, 70, 20, '#FFFFFF'), (1480, 200, 14, '#FFE21A'), (120, 220, 14, '#FFFFFF')):
    d.add(flat.star4(cx, cy, s, c))
d.save(os.path.join(HERE, 'banner.svg')); render(os.path.join(HERE, 'banner.svg'), os.path.join(HERE, 'banner.png')); os.remove(os.path.join(HERE, 'banner.svg'))
print('ok')
