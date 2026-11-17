"""Cartoon item icons drawn in SVG (3 tones + specular + dark outline).
Placeholders / 2D-style games. For real Roblox games render blocky models instead
(references/style-anatomy.md section 8) and drop them in with embed_models.py.
Every function: (d, cx, cy, s) -> svg, s = rough radius in px."""
from uikit import f, PAL, NAVY, glow, sunburst

def _o(s):
    return f(max(3, s * .085))

def chest(d, cx, cy, s, p=PAL['gold']):
    w, h = s * 1.9, s * 1.45
    x, y = cx - w / 2, cy - h * .35
    o = NAVY
    return (f'<g id="Item Chest"><rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h * .75)}" rx="{f(s * .12)}" fill="#9A5A2B" stroke="{o}" stroke-width="{_o(s)}"/>'
            f'<rect x="{f(x)}" y="{f(y + h * .45)}" width="{f(w)}" height="{f(h * .3)}" rx="{f(s * .1)}" fill="#6E3A17"/>'
            f'<path d="M{f(x)} {f(y)} Q{f(cx)} {f(y - h * .75)} {f(x + w)} {f(y)} Z" fill="#B66C33" stroke="{o}" stroke-width="{_o(s)}" stroke-linejoin="round"/>'
            f'<path d="M{f(x + w * .12)} {f(y - h * .06)} Q{f(x + w * .25)} {f(y - h * .5)} {f(cx)} {f(y - h * .5)}" fill="none" stroke="#E7A066" stroke-width="{f(s * .1)}" stroke-linecap="round"/>'
            f'<rect x="{f(x + w * .14)}" y="{f(y - h * .52)}" width="{f(w * .12)}" height="{f(h * 1.27)}" fill="{p["b"]}" stroke="{o}" stroke-width="{_o(s)}"/>'
            f'<rect x="{f(x + w * .74)}" y="{f(y - h * .52)}" width="{f(w * .12)}" height="{f(h * 1.27)}" fill="{p["b"]}" stroke="{o}" stroke-width="{_o(s)}"/>'
            f'<rect x="{f(cx - s * .2)}" y="{f(y - s * .12)}" width="{f(s * .4)}" height="{f(s * .5)}" rx="{f(s * .08)}" fill="{p["a"]}" stroke="{o}" stroke-width="{_o(s)}"/>'
            f'<circle cx="{f(cx)}" cy="{f(y + s * .1)}" r="{f(s * .06)}" fill="{o}"/>'
            f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h * .75)}" rx="{f(s * .12)}" fill="none" stroke="{o}" stroke-width="{_o(s)}"/></g>')

def egg(d, cx, cy, s, base='#FFFFFF', spot='#7DD3FC', shade='#C9D7EA'):
    path = (f'M{f(cx)} {f(cy - s * 1.15)} C{f(cx - s * .62)} {f(cy - s * 1.15)} {f(cx - s * .95)} {f(cy - s * .1)} {f(cx - s * .95)} {f(cy + s * .3)} '
            f'A{f(s * .95)} {f(s * .85)} 0 0 0 {f(cx + s * .95)} {f(cy + s * .3)} C{f(cx + s * .95)} {f(cy - s * .1)} {f(cx + s * .62)} {f(cy - s * 1.15)} {f(cx)} {f(cy - s * 1.15)} Z')
    cp = d.clip(f'<path d="{path}"/>')
    spots = ''.join(f'<ellipse cx="{f(cx + a * s)}" cy="{f(cy + b * s)}" rx="{f(r * s)}" ry="{f(r * s * .8)}" fill="{spot}"/>'
                    for a, b, r in ((-.45, -.35, .22), (.4, -.1, .3), (-.2, .55, .26), (.55, .7, .18), (.05, -.85, .14)))
    return (f'<g id="Item Egg"><path d="{path}" fill="{base}"/><g clip-path="{cp}">{spots}'
            f'<ellipse cx="{f(cx + s * .55)}" cy="{f(cy + s * .4)}" rx="{f(s * .8)}" ry="{f(s * 1.2)}" fill="{shade}" fill-opacity=".55"/></g>'
            f'<path d="{path}" fill="none" stroke="{NAVY}" stroke-width="{_o(s)}"/>'
            f'<path d="M{f(cx - s * .6)} {f(cy - s * .1)} Q{f(cx - s * .55)} {f(cy - s * .7)} {f(cx - s * .2)} {f(cy - s * .9)}" fill="none" stroke="#FFF" stroke-width="{f(s * .13)}" stroke-linecap="round"/></g>')

def potion(d, cx, cy, s, p=PAL['pink']):
    body = f'M{f(cx - s * .25)} {f(cy - s * .55)} V{f(cy - s * .25)} A{f(s * .78)} {f(s * .78)} 0 1 0 {f(cx + s * .25)} {f(cy - s * .25)} V{f(cy - s * .55)} Z'
    cp = d.clip(f'<path d="{body}"/>')
    return (f'<g id="Item Potion"><path d="{body}" fill="#E8F6FF"/>'
            f'<g clip-path="{cp}"><rect x="{f(cx - s)}" y="{f(cy - s * .05)}" width="{f(s * 2)}" height="{f(s * 1.4)}" fill="{p["b"]}"/>'
            f'<rect x="{f(cx - s)}" y="{f(cy - s * .05)}" width="{f(s * 2)}" height="{f(s * .18)}" fill="{p["a"]}"/>'
            f'<circle cx="{f(cx + s * .3)}" cy="{f(cy + s * .4)}" r="{f(s * .1)}" fill="{p["a"]}"/><circle cx="{f(cx - s * .2)}" cy="{f(cy + s * .25)}" r="{f(s * .07)}" fill="{p["a"]}"/></g>'
            f'<path d="{body}" fill="none" stroke="{NAVY}" stroke-width="{_o(s)}" stroke-linejoin="round"/>'
            f'<rect x="{f(cx - s * .34)}" y="{f(cy - s * .82)}" width="{f(s * .68)}" height="{f(s * .32)}" rx="{f(s * .08)}" fill="#A0663A" stroke="{NAVY}" stroke-width="{_o(s)}"/>'
            f'<path d="M{f(cx - s * .5)} {f(cy)} Q{f(cx - s * .55)} {f(cy + s * .4)} {f(cx - s * .3)} {f(cy + s * .55)}" fill="none" stroke="#FFF" stroke-width="{f(s * .11)}" stroke-linecap="round"/></g>')

def sword(d, cx, cy, s, p=PAL['cyan']):
    g = f'<g id="Item Sword" transform="rotate(-40 {f(cx)} {f(cy)})">'
    blade = f'M{f(cx - s * .17)} {f(cy + s * .3)} V{f(cy - s * .95)} L{f(cx)} {f(cy - s * 1.25)} L{f(cx + s * .17)} {f(cy - s * .95)} V{f(cy + s * .3)} Z'
    return (g + f'<path d="{blade}" fill="{p["a"]}" stroke="{NAVY}" stroke-width="{_o(s)}" stroke-linejoin="round"/>'
            f'<path d="M{f(cx + s * .02)} {f(cy + s * .25)} V{f(cy - s * 1.05)} L{f(cx + s * .17)} {f(cy - s * .95)} V{f(cy + s * .3)} Z" fill="{p["b"]}"/>'
            f'<path d="{blade}" fill="none" stroke="{NAVY}" stroke-width="{_o(s)}" stroke-linejoin="round"/>'
            f'<rect x="{f(cx - s * .55)}" y="{f(cy + s * .28)}" width="{f(s * 1.1)}" height="{f(s * .22)}" rx="{f(s * .1)}" fill="{PAL["gold"]["b"]}" stroke="{NAVY}" stroke-width="{_o(s)}"/>'
            f'<rect x="{f(cx - s * .11)}" y="{f(cy + s * .5)}" width="{f(s * .22)}" height="{f(s * .5)}" fill="#7A3E1D" stroke="{NAVY}" stroke-width="{_o(s)}"/>'
            f'<circle cx="{f(cx)}" cy="{f(cy + s * 1.08)}" r="{f(s * .15)}" fill="{PAL["gold"]["b"]}" stroke="{NAVY}" stroke-width="{_o(s)}"/>'
            f'<path d="M{f(cx - s * .07)} {f(cy - s * .1)} V{f(cy - s * .85)}" stroke="#FFF" stroke-width="{f(s * .07)}" stroke-linecap="round"/></g>')

def crown(d, cx, cy, s, p=PAL['gold']):
    pts = f'{f(cx - s)},{f(cy - s * .45)} {f(cx - s * .5)},{f(cy)} {f(cx)},{f(cy - s * .75)} {f(cx + s * .5)},{f(cy)} {f(cx + s)},{f(cy - s * .45)} {f(cx + s * .8)},{f(cy + s * .55)} {f(cx - s * .8)},{f(cy + s * .55)}'
    return (f'<g id="Item Crown"><polygon points="{pts}" fill="{p["b"]}" stroke="{NAVY}" stroke-width="{_o(s)}" stroke-linejoin="round"/>'
            f'<rect x="{f(cx - s * .8)}" y="{f(cy + s * .3)}" width="{f(s * 1.6)}" height="{f(s * .25)}" fill="{p["d"]}"/>'
            f'<polygon points="{pts}" fill="none" stroke="{NAVY}" stroke-width="{_o(s)}" stroke-linejoin="round"/>'
            + ''.join(f'<circle cx="{f(cx + a * s)}" cy="{f(cy + b * s)}" r="{f(s * .13)}" fill="{c}" stroke="{NAVY}" stroke-width="{f(s * .05)}"/>'
                      for a, b, c in ((-1, -.5, '#FF4D6D'), (0, -.82, '#2FA8FF'), (1, -.5, '#3EE07A')))
            + f'<path d="M{f(cx - s * .6)} {f(cy + s * .1)} L{f(cx - s * .45)} {f(cy - s * .1)}" stroke="#FFF" stroke-width="{f(s * .1)}" stroke-linecap="round"/></g>')

def coins(d, cx, cy, s):
    from uikit import coin
    return ('<g id="Item Coins">' + coin(cx - s * .55, cy + s * .35, s * .5) + coin(cx + s * .5, cy + s * .4, s * .48)
            + coin(cx, cy - s * .15, s * .62) + coin(cx + s * .35, cy - s * .75, s * .38) + '</g>')

def gems(d, cx, cy, s):
    from uikit import gem
    return ('<g id="Item Gems">' + gem(cx - s * .5, cy + s * .3, s * .5, PAL['purple']) + gem(cx + s * .55, cy + s * .35, s * .45, PAL['green'])
            + gem(cx, cy - s * .15, s * .7, PAL['cyan']) + '</g>')

def clover(d, cx, cy, s, p=PAL['green']):
    leaf = lambda a: (f'<ellipse cx="{f(cx)}" cy="{f(cy - s * .42)}" rx="{f(s * .38)}" ry="{f(s * .48)}" transform="rotate({a} {f(cx)} {f(cy)})" '
                      f'fill="{p["b"]}" stroke="{NAVY}" stroke-width="{_o(s)}"/>')
    return (f'<g id="Item Clover"><path d="M{f(cx)} {f(cy)} Q{f(cx + s * .2)} {f(cy + s * .7)} {f(cx + s * .55)} {f(cy + s * 1)}" fill="none" stroke="{NAVY}" stroke-width="{f(s * .22)}" stroke-linecap="round"/>'
            f'<path d="M{f(cx)} {f(cy)} Q{f(cx + s * .2)} {f(cy + s * .7)} {f(cx + s * .55)} {f(cy + s * 1)}" fill="none" stroke="{p["d"]}" stroke-width="{f(s * .1)}" stroke-linecap="round"/>'
            + ''.join(leaf(a) for a in (0, 90, 180, 270))
            + ''.join(f'<ellipse cx="{f(cx)}" cy="{f(cy - s * .5)}" rx="{f(s * .14)}" ry="{f(s * .2)}" transform="rotate({a} {f(cx)} {f(cy)})" fill="{p["a"]}"/>' for a in (0, 90, 180, 270))
            + f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(s * .12)}" fill="{p["d"]}"/></g>')

def seed_bag(d, cx, cy, s, p=PAL['orange'], seed='#6BD13A'):
    bag = f'M{f(cx - s * .7)} {f(cy - s * .6)} L{f(cx + s * .7)} {f(cy - s * .6)} L{f(cx + s * .85)} {f(cy + s * .9)} Q{f(cx)} {f(cy + s * 1.05)} {f(cx - s * .85)} {f(cy + s * .9)} Z'
    return (f'<g id="Item Seeds"><path d="{bag}" fill="#E9C79A" stroke="{NAVY}" stroke-width="{_o(s)}" stroke-linejoin="round"/>'
            f'<path d="M{f(cx - s * .7)} {f(cy - s * .6)} L{f(cx - s * .55)} {f(cy - s * .9)} L{f(cx - s * .3)} {f(cy - s * .65)} L{f(cx)} {f(cy - s * .95)} L{f(cx + s * .3)} {f(cy - s * .65)} L{f(cx + s * .55)} {f(cy - s * .9)} L{f(cx + s * .7)} {f(cy - s * .6)} Z" fill="#D5AE7C" stroke="{NAVY}" stroke-width="{_o(s)}" stroke-linejoin="round"/>'
            f'<circle cx="{f(cx)}" cy="{f(cy + s * .2)}" r="{f(s * .42)}" fill="{p["b"]}" stroke="{NAVY}" stroke-width="{_o(s)}"/>'
            f'<path d="M{f(cx)} {f(cy + s * .45)} Q{f(cx - s * .05)} {f(cy + s * .1)} {f(cx)} {f(cy - s * .05)} M{f(cx)} {f(cy + s * .15)} Q{f(cx + s * .25)} {f(cy - s * .05)} {f(cx + s * .22)} {f(cy - s * .2)} Q{f(cx + s * .05)} {f(cy - s * .1)} {f(cx)} {f(cy + s * .15)}" fill="{seed}" stroke="{NAVY}" stroke-width="{f(s * .05)}" stroke-linejoin="round"/>'
            f'<path d="M{f(cx - s * .55)} {f(cy - s * .35)} L{f(cx - s * .65)} {f(cy + s * .6)}" stroke="#FFF" stroke-width="{f(s * .09)}" stroke-linecap="round" stroke-opacity=".8"/></g>')

def shield(d, cx, cy, s, p=PAL['blue']):
    sh = f'M{f(cx)} {f(cy - s)} L{f(cx + s * .85)} {f(cy - s * .65)} Q{f(cx + s * .85)} {f(cy + s * .55)} {f(cx)} {f(cy + s * 1.05)} Q{f(cx - s * .85)} {f(cy + s * .55)} {f(cx - s * .85)} {f(cy - s * .65)} Z'
    cp = d.clip(f'<path d="{sh}"/>')
    return (f'<g id="Item Shield"><path d="{sh}" fill="{p["b"]}"/><g clip-path="{cp}"><rect x="{f(cx)}" y="{f(cy - s)}" width="{f(s)}" height="{f(s * 2.1)}" fill="{p["d"]}"/></g>'
            f'<path d="{sh}" fill="none" stroke="{NAVY}" stroke-width="{_o(s)}" stroke-linejoin="round"/>'
            f'<path d="M{f(cx)} {f(cy - s * .55)} L{f(cx + s * .15)} {f(cy - s * .15)} L{f(cx + s * .5)} {f(cy - s * .1)} L{f(cx + s * .22)} {f(cy + s * .15)} L{f(cx + s * .32)} {f(cy + s * .55)} L{f(cx)} {f(cy + s * .32)} L{f(cx - s * .32)} {f(cy + s * .55)} L{f(cx - s * .22)} {f(cy + s * .15)} L{f(cx - s * .5)} {f(cy - s * .1)} L{f(cx - s * .15)} {f(cy - s * .15)} Z" fill="{PAL["gold"]["a"]}" stroke="{NAVY}" stroke-width="{f(s * .06)}" stroke-linejoin="round"/>'
            f'<path d="M{f(cx - s * .6)} {f(cy - s * .45)} Q{f(cx - s * .6)} {f(cy + s * .2)} {f(cx - s * .3)} {f(cy + s * .55)}" fill="none" stroke="#FFF" stroke-width="{f(s * .1)}" stroke-linecap="round" stroke-opacity=".8"/></g>')

def hero_back(d, cx, cy, r, col='#FFF5A0', rays=True):
    """glow + sunburst that always sits behind a hero item"""
    return glow(d, cx, cy, r, col) + (sunburst(cx, cy, r * 1.05, 14, '#FFFFFF', .28) if rays else '')

ITEMS = dict(chest=chest, egg=egg, potion=potion, sword=sword, crown=crown, coins=coins, gems=gems,
             clover=clover, seeds=seed_bag, shield=shield)

def fruit(d, cx, cy, s, body='#FF8A1F', light='#FFC27A', leaf='#3EC23A', shape='round', stripes=None, spikes=None):
    """garden produce: round / long (carrot) / star. stripes = colour for melon stripes, spikes = colour for dragon-fruit scales"""
    if shape == 'long':
        bp = f'M{f(cx - s * .5)} {f(cy - s * .55)} Q{f(cx)} {f(cy - s * .8)} {f(cx + s * .5)} {f(cy - s * .55)} L{f(cx + s * .08)} {f(cy + s * 1.05)} Q{f(cx)} {f(cy + s * 1.12)} {f(cx - s * .08)} {f(cy + s * 1.05)} Z'
    elif shape == 'star':
        import math
        pts = []
        for k in range(10):
            r = s * (1 if k % 2 == 0 else .52)
            a = math.radians(-90 + k * 36)
            pts.append(f'{f(cx + r * math.cos(a))},{f(cy + .1 * s + r * math.sin(a))}')
        bp = 'M' + ' L'.join(pts) + ' Z'
    else:
        bp = f'M{f(cx - s * .92)} {f(cy)} A{f(s * .92)} {f(s * .86)} 0 1 0 {f(cx + s * .92)} {f(cy)} A{f(s * .92)} {f(s * .86)} 0 1 0 {f(cx - s * .92)} {f(cy)} Z'
    cp = d.clip(f'<path d="{bp}"/>')
    inner = f'<ellipse cx="{f(cx + s * .45)}" cy="{f(cy + s * .45)}" rx="{f(s * .7)}" ry="{f(s * .9)}" fill="#000" fill-opacity=".14"/>'
    if stripes:
        inner += ''.join(f'<path d="M{f(cx + k * s * .38)} {f(cy - s)} Q{f(cx + k * s * .55)} {f(cy)} {f(cx + k * s * .38)} {f(cy + s)}" fill="none" stroke="{stripes}" stroke-width="{f(s * .14)}"/>' for k in (-2, -1, 0, 1, 2))
    if spikes:
        inner += ''.join(f'<path d="M{f(cx + a * s)} {f(cy + b * s)} q{f(s * .12)} {f(-s * .3)} {f(s * .3)} {f(-s * .32)}" fill="none" stroke="{spikes}" stroke-width="{f(s * .12)}" stroke-linecap="round"/>' for a, b in ((-.6, .1), (-.1, -.3), (.35, .2), (-.3, .6), (.2, .7), (.5, -.35)))
    leaves = ''.join(f'<ellipse cx="{f(cx + a * s * .28)}" cy="{f(cy - s * 1.02)}" rx="{f(s * .15)}" ry="{f(s * .36)}" transform="rotate({a * 32:.0f} {f(cx + a * s * .28)} {f(cy - s * 1.02)})" fill="{leaf}" stroke="{NAVY}" stroke-width="{_o(s * .8)}"/>' for a in (-1, 0, 1))
    return (f'<g id="Item Fruit">{leaves}<path d="{bp}" fill="{body}"/><g clip-path="{cp}">{inner}</g>'
            f'<path d="{bp}" fill="none" stroke="{NAVY}" stroke-width="{_o(s)}" stroke-linejoin="round"/>'
            f'<path d="M{f(cx - s * .55)} {f(cy - s * .05)} Q{f(cx - s * .55)} {f(cy - s * .45)} {f(cx - s * .2)} {f(cy - s * .55)}" fill="none" stroke="{light}" stroke-width="{f(s * .14)}" stroke-linecap="round"/>'
            f'<circle cx="{f(cx - s * .1)}" cy="{f(cy - s * .58)}" r="{f(s * .07)}" fill="#FFF"/></g>')
ITEMS['fruit'] = fruit
