# Roblox-flat style (default)

Studied from big simulators (e.g. Throw Food for Animals shop/egg screens). Code: `kit/flat.py`, example `egg_flat.py`.

## Surfaces
- Outline: **black**, 5-7px on panels/buttons/cards, 4-5px on small tiles. Everything has it.
- Fill: flat colour + a lighter **top band** (~40% height) + 1-2 faint diagonal sheen stripes (white 8-16%). Not a glossy swoosh.
- Corners: panel 26-28, cards 22, buttons 14-16, tiles 8.
- Card = black outer frame (4px) + light inner rim (white 55%) + diagonal gradient light->saturated + soft white glow + faint rays behind the item.
- Panel behind a shop: dark charcoal `#262A34`, header bar on top with a warm gradient, close = red square with white X.

## Text
- Font: **Fredoka Bold** (`kit/fonts/FredokaBold.ttf`, `flat.txt`). Outline = size/4.2, black.
- Fill: cream `#FFF8E6` for titles/labels, white for numbers, yellow gradient (`flat.title_fill`) for the big screen title.
- Titles big (60-80px on a 1300px canvas), left-aligned in banners, slight -1..-2 deg tilt.

## Shop layout
- ONE vertical scroll. Order: featured/limited banner -> sections -> gamepasses -> free item.
- Section = dark slate pill `#3B4258` centered with thin grey lines out to both sides.
- Rows of 3 or 4 cards. Card colour = what it sells.
- Price ladder per row: pile grows (1, 3, 6, 10 items), ribbons: none, Good Value (blue), Great Value (orange), Most Value (rainbow). Better Value = pink.
- Inside card from top: ribbon (overlapping the top edge) -> item pile -> dark translucent amount pill (`+$2.4M`, small icon left) -> lime buy button.
- Gamepass = wide card: big title top-left, description right, item in a light translucent circle with a small `x2` pill, buy button bottom-right.

## Egg / gacha
- Panel with themed gradient + faint background scene (silhouettes at 13-18% white) + rays and glow behind the egg on the left.
- Title + `New!`/`LIMITED` tag (rainbow-framed dark pill), `ODDS` dark button top-right.
- Reward tiles in a row, **growing with rarity**, % above in yellow, stat pill inside, rainbow frame on the rarest.
- Buy x1 / x3 / x10 lime buttons with labels above; discount tag on the biggest.

## Buttons
- Buy = lime `#7CFF4A` top band over `#22D10A`, black outline 6, white Robux mark (hexagon + square) + big number.
- Secondary = dark `#2B2F4A`, or blue `#6FD3FF -> #1E8BE0`.

## Don'ts
Navy outlines, gloss swooshes, rays on every card, every card a different rainbow colour, side plank tabs, thin text.
