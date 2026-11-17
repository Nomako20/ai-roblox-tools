# Screen catalog

For each: parts in order, states, and the example to start from. Positions: `placement.md`.

| Screen | Parts | States | Start from |
|---|---|---|---|
| Main shop (scroll) | header (title, Gifts, close) / featured banner / sections (boosts, currency packs) / gamepasses / free item | owned, sale, limited timer | `shop_daily_v2.py` (layout), `references/style-flat.md` (look) |
| Restock shop (garden) | sign + restock timer / rows: item window, name, rarity, stock count, coin price, Robux price, gift / restock-all button + coin counter | in stock, low, sold out (dim + RESTOCK SOON) | `shop_stock_v2.py` |
| Daily rotating shop | timer + currency / featured big slot / grid of offers / category tabs | owned, discount | `shop_daily_v2.py` |
| Egg / gacha | title + tag + ODDS / egg on rays / reward tiles growing with rarity + % / buy x1 x3 x10 | auto-hatch, discount | `egg_flat.py`, `egg_hatch_v2.py` |
| Odds list | header + close / rows: icon, name in rarity colour, % right | - | inside `egg_hatch_v2.py` |
| Season / battle pass | level + XP bar + buy premium / free row + premium row on a tier rail / current tier raised + CLAIM | claimed (dim + tick), locked (padlock), current | `battle_pass_v2.py` |
| Starter / limited offer popup | title banner + close / hero item / contents with amounts / VALUE tag / crossed price + price / timer | one-time | `offer_starter_v2.py` |
| Daily rewards | streak bar / 6 day tiles + big day 7 / next timer | claimed stamp, today (CLAIM), locked | `daily_rewards_v2.py` |
| Tabs | only when a screen really has categories; big-game shops use one scroll with section pills instead | active, notification dot | category tabs in `shop_daily_v2.py` |
| HUD | currency pills top-left, menu icons left column (shop, pets, inventory, quests, settings), boosts strip, action buttons around jump on mobile | notification dots | see `placement.md` |

## Genre notes (from research, see `research/`)
- Simulators: shop + egg + boosts + rebirth + leaderboards; currency top-left; menu column left.
- Tycoon: most buying happens on 3D pads in the world; the 2D shop is gamepasses + codes.
- Obby: stage counter top, skip-stage button (developer product), checkpoints.
- Tower defense: unit hotbar bottom, wave counter top, upgrade panel on the selected unit.
- Combat: abilities bottom-right around jump (mobile), health top-left/bottom-center, kill feed top-right.
- Horror: almost no UI, in-world cues; red only for danger.
- Casual mobile patterns copied on Roblox: daily calendar, spin wheel, piggy bank, timed offer popups. Use with care: no fake urgency, no dark patterns.
