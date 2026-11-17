# Guide

## 1. Setup (5 minutes)
1. Clone into your skills folder: `~/.claude/skills/ai-roblox-tools` (Windows: `C:\Users\<you>\.claude\skills\ai-roblox-tools`).
2. `pip install fonttools pillow playwright`. Edge or Chrome must be installed (used for rendering).
3. Test: `cd examples && python egg_flat.py`. It writes `egg_flat.png`.

## 2. Make your first screen
1. Tell the agent your game and screen: "lava world simulator, egg screen".
2. Give it 2-4 screenshots of big games in your genre. It writes a short style brief.
3. It copies the closest example (`examples/egg_flat.py`), changes title, colours, items and prices, renders, compares with your screenshots, and shows you the PNG.
4. Point at what's wrong ("the buttons are too small", "icons look fake"). It changes only that.

## 3. Change things yourself
- Colours and text: top of every example file.
- Items: `item_img('toon/cash', x, y, size)` uses `pack/`. Drop your own transparent PNG in `pack/icons-toon/` and use its name.
- Card colours: `card(d, x, y, w, h, light, dark)` in `kit/flat.py`.

## 4. Make new icons in Blender
Open Blender, run `blender/toon_icon.py` in the Text editor, then build a model with `box/cylinder/extrude`, `finish(...)` with `toon(...)` colours, and `render_icon(root, path)`. The docstring at the top has a full cash-bundle example. `blender/icons.blend` has every model from the pack.

## 5. Put it in Roblox
Follow `references/roblox-pipeline.md`:
1. Export the background without buttons, plus each button and icon as its own PNG (max 1024 px).
2. Upload, then build a ScreenGui with real ImageLabels/ImageButtons placed in scale.
3. Add hover/press/open tweens with TweenService.
4. Purchases go through MarketplaceService, granted on the server.

Placement rules (where the shop button goes, safe areas): `references/placement.md`.

## 6. AnimKit (experimental)
`animkit/README.md`: describe poses as data ("right elbow flex 90"); it validates joints, clamps angles and builds a real KeyframeSequence. Not yet tested inside Studio.
