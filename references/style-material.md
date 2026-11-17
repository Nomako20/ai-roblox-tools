# Material style (wood / iron / cloth / stone)

For games with a physical world theme: farm market stall, armory, castle, quest board. Code: `kit/materials.py`, examples `shop_stock_v2.py` (seed stall), `shop_daily_v2.py` (armory), `battle_pass_v2.py`, `offer_starter_v2.py`, `daily_rewards_v2.py`, `egg_hatch_v2.py`.

## Rule
Build the screen OUT OF a material. Keep the palette restrained (browns, iron greys, brass). Colour only as accents:
- rarity: small gem stud in a brass bezel (`gem_stud`) + coloured rarity name + glow inside the item window
- prices: green (coins/Robux) and purple (premium) buttons
- one cloth banner per screen for the title or FEATURED

## Pieces
- `planks(tone, ph)`: horizontal planks with per-plank tint, grain strokes, knots, seams, optional nails. Tones: `WOOD` pine, `OAK` light shelves, `WALNUT` dark boards.
- `plate(tone=IRON|BRASS)`: metal plate with bevel light, scratches, rivets. Timers, currency counters, tabs, name plates.
- `iron_corners`, `iron_band`: brackets and straps on boards.
- `hanging_sign(chain=True)`: plank sign on ropes/chains for the screen title.
- `awning`: striped canvas with scalloped edge (market stall).
- `cloth_banner`: fabric ribbon with folded tails and stitching.
- `stone_wall`, `torch_glow`: dark backdrop for indoor screens.
- `uikit.item_window`: the item sits INSIDE a recessed window (inner shadow, rarity glow, contact shadow). Never paste an item on top of a card.

## Don'ts
Candy-coloured cards, cute floating leaves/sparkles everywhere, nails on every plank (noise).
