# Icons

Icons decide whether a screen looks like a top game. Be honest about quality: icons drawn shape-by-shape in code look "drawn by a program" next to artist-made packs. Use the best source available, in this order:

1. **The game's own art** (renders of the real in-game models). Best match with the world.
2. **A licensed icon pack** the user owns or downloads (many good Roblox-style packs are free or pay-what-you-want). Check the license allows use in games. Never copy pack artwork into another pack, repo or product.
3. **An image generator** (when the user has one): generate a sheet of 16-25 icons on a flat background in one image, slice it, keep only the good ones. Prompt for: chunky cartoon game icon, thick dark outline, soft top-light gradient, small white shine, visible thickness, no text.
4. **3D renders in Blender** (`blender/toon_icon.py`): toon shading (3 hard tones + black inverted-hull outline) or voxel with Roblox studs. Good for coins, gems, potions, eggs, dumbbells and piles.
5. **Simple shapes in code** (`kit/flat.py`: `cash_icon`, `gem_icon`, sparkles, Robux mark): fine for UI marks and simple currency, not for illustrated items.

## What makes good game icons (what to check)
- full, round silhouettes that fill the slot
- visible thickness under the shape (sticker depth)
- light top, deep bottom; one thin rim light; a small streak shine
- each object in its own colours (not one shape recoloured per rarity)
- one consistent dark outline across the whole set

## In the UI
`uikit.item_img(name, cx, cy, size)` embeds a PNG from `pack/` with a dark sticker outline. Items sit in windows or tiles with glow and rays behind them, never floating on a plain card. Piles of many items: `flat.img_pile`.

## Included example assets
`pack/icons-toon` (cash, bolt, gem, coin toon renders), `pack/items-voxel` (studded voxel items), `pack/fruits-voxel`. They exist so the examples run; treat them as samples, not a complete icon library.
