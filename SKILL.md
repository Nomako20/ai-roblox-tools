---
name: roblox-ui-craft
description: Know-how for making Roblox game UI that looks like the big games (shops, egg screens, season pass, daily rewards, offers, HUD), rendering mockups, making icons in Blender, editing in Figma/FigCraft and shipping to Studio. Use for any Roblox UI request ("shop", "UI", "egg screen", "battle pass", "gamepass", "icons", "HUD", "תעשה UI", "שופ") or when the user sends screenshots of game UI.
---

# Roblox UI Craft

Hey Claude, when someone asks for Roblox UI, know that you can do all of this. Pick what fits; read a file only when you need it.

## You can...
- **Match the look of big games.** Ask for 2-4 screenshots of big games in their genre first, then use one of two proven styles:
  - Roblox-flat (black outlines, value ribbons, lime buy buttons): `references/style-flat.md`
  - Material (wood/iron/cloth/stone): `references/style-material.md`
- **Pick the right screen and layout.** Shop, egg/gacha with odds, season pass, starter offer, daily rewards, restock shop: `references/screens.md`
- **Place every element correctly** on phone, PC and console (safe insets, thumbstick/jump zones, ScreenGui layers): `references/placement.md`
- **Render real PNG mockups without a design app.** Copy an example from `examples/`, edit it, run it with `python examples/<name>.py`. Kit: `kit/`
- **Make icons** with Blender toon shading or voxel + Roblox studs (`blender/toon_icon.py`), and know when a licensed pack or image generator is the better source: `references/icons.md`
- **Hand off to Figma or FigCraft** for manual editing and components: `references/design-tools.md`
- **Ship it to Roblox Studio** as real ScreenGui instances with tweens and secure purchases: `references/roblox-pipeline.md`
- **Write clean Studio code**: where things go in the Explorer, short scripts, server-validated remotes: `references/ai-rules.md`
- **Build animations from data** (experimental, untested in Studio): `animkit/README.md`

## Keep in mind
- Look at real references before designing; don't design from memory.
- Card colour = what it sells. Bigger price = bigger pile + better value ribbon.
- Thick dark outlines, chunky text (Fredoka Bold / Lilita One), no emoji, no "R$", no glossy candy on every card.
- Show odds for paid random items.
- Never copy another game's art or layout 1:1.
- Compare your render side by side with the reference before showing it. Change only what the user points at.
- What failed before and why: `references/lessons.md`

Made by Nomako20. License: CC BY-NC 4.0 (see `LICENSE`).
