---
name: roblox-ui-craft
description: Make Roblox game UI that looks like the big games (shops, egg/gacha screens, season pass, daily rewards, offers, tabs, HUD) and the icons that go in it, then ship it to Roblox Studio. Two proven styles (Roblox-flat from top simulators, and a wood/iron "material" style), a Python SVG kit that renders real PNG mockups, a Blender toon-icon recipe, Figma/FigCraft workflows, and where every UI goes on screen. Use for ANY Roblox UI request - "shop", "UI", "egg screen", "battle pass", "gamepass", "icons", "HUD", "tabs", "make it look like Pet Sim / Grow a Garden", "תעשה UI", "שופ", "כפתורים", "אייקונים", or when the user sends screenshots of game UI.
---

# Roblox UI Craft

Made by Nomako20 with Claude. Credits: `CREDITS.md`. License: `LICENSE` (all rights reserved).

Goal: UI a player would believe came from a top Roblox game. Not "AI UI": no glossy candy everywhere, no soft generic gradients, no thin text, no emoji, no "R$".

## Workflow (in order)

1. **Look at real big games first.** Ask the user for 2-4 screenshots of big games in the genre (or use ones they sent). Small-game portfolios are NOT the bar. Write a 5-line brief: outline, colours, text, card shape, what is special. Say which reference you match.
2. **Pick the style** (one per game, never mix):
   - `references/style-flat.md`: **Roblox-flat**, the default for simulators/tycoons/casual. Thick black outlines, flat strong colours, one scrolling shop, value ribbons, lime buy buttons.
   - `references/style-material.md`: **Material**, for worlds with a physical theme (farm stall, armory, castle). Wood/iron/cloth/stone, colour only as accent.
3. **Pick the screen** from `references/screens.md` (shop, egg, pass, rewards, offer, odds, tabs, HUD) and where it sits from `references/placement.md`.
4. **Icons** (`references/icons.md`): piles of many things = 3D render (toon or voxel) piled in 2D. A single hero icon = clean 2.5D SVG (`flat.cash_icon`, `flat.gem_icon`) or a toon render. Never smooth realistic 3D.
5. **Build a mockup**: copy the closest file in `examples/`, change content, run it (`python examples/egg_flat.py` writes PNG next to it). Kit: `kit/uikit.py` (Doc, render, price, item_img), `kit/flat.py`, `kit/materials.py`.
6. **Compare side by side** with the reference before showing (`python examples/_strip.py name a b`). If it looks generic, it is. Fix, then show.
7. **Iterate only on what the user points at.** Don't redo approved parts.
8. **Ship to Studio** when asked: `references/roblox-pipeline.md` (slice PNGs, upload, ScreenGui, tweens). Code rules: `references/ai-rules.md`.

## Hard rules (learned the hard way, see `references/lessons.md`)

- Look before designing. Never work from memory of "what Roblox UI looks like".
- Card colour = what it sells (cash green, power orange, gems purple, passes blue/purple).
- Bigger price = bigger pile + better value ribbon (Good blue, Better pink, Great orange, Most rainbow).
- Rarity tiles grow with rarity; the rarest gets a rainbow frame.
- Text: Fredoka Bold (flat) or Lilita One (material), white/cream/yellow, thick dark outline. Never thin.
- No side tabs in the flat style: one scroll with section pills. Tabs only when the screen really has categories.
- Show odds for every paid random item (Roblox policy).
- Never copy a game's layout or art 1:1. Take the language, make your own composition and items.
- Answer the user in their language. Send pictures often.

## Files

| Path | What |
|---|---|
| `references/style-flat.md` | Roblox-flat recipe with numbers |
| `references/style-material.md` | wood/iron/cloth/stone recipe |
| `references/screens.md` | every screen type: parts, order, states, genre notes |
| `references/placement.md` | where UI goes on phone/PC/console, safe areas, ScreenGui layers |
| `references/icons.md` | icon decision + toon/voxel/2.5D recipes |
| `references/ai-rules.md` | Studio basics + code rules for agents (short scripts, structure) |
| `references/roblox-pipeline.md` | mockup -> PNG slices -> ScreenGui + TweenService |
| `references/lessons.md` | what was rejected and why |
| `references/research/` | raw research notes with sources |
| `kit/` | Python SVG kit + fonts (Fredoka, Lilita One, OFL) |
| `examples/` | 7 finished screens (code + PNG) |
| `pack/` | sample renders used by the examples (toon, voxel items, fruits) |
| `references/design-tools.md` | Figma and FigCraft workflows |
| `blender/` | `toon_icon.py` recipe + `icons.blend` with every model |
| `animkit/` | AnimKit: declarative animation builder for Studio (experimental, untested in Studio) |
