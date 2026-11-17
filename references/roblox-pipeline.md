# FigCraft -> Roblox Studio

Load roblox-collaboration-mode + roblox-gui first. Build real instances in StarterGui (not code that builds UI at runtime).

## 1. Slice
- Static background (frame, cards, titles, tags) WITHOUT buttons, models, rays -> one PNG, `size:"1024w"` (Roblox caps images at 1024).
- Every interactive piece (price buttons, tabs, close, gift) -> own PNG at scale 2 (export the Default variant / group).
- Item renders: 512px PNGs with sticker outline. Rays: one white 512px sunburst PNG with radial alpha fade, tint with ImageColor3.
- Keep a table of each piece's design-space box (x, y, w, h) from the SVG / FigCraft.

## 2. Upload
`python -I -m http.server 8765 --bind 127.0.0.1` in the PNG folder (background), then `mcp__Roblox_Studio__upload_image {imagePaths:["http://127.0.0.1:8765/X.png", ...]}` -> map of rbxassetid. All at once.

## 3. Build (execute_luau, Edit)
- ScreenGui `IgnoreGuiInset`, `ResetOnSpawn=false`, Sibling ZIndex.
- Shop = ImageLabel with UIAspectRatioConstraint (designW/designH), Size 0.94x0.9 of screen, UIScale for the open animation.
- Children placed in scale space: AnchorPoint 0.5, Position = (cx/W, cy/H), Size = (w/W, h/H). Store BaseSize/BasePos attributes.
- Folders: Rays (z2), Models (z3), Buttons (z5, ImageButton, AutoButtonColor=false, Kind attribute).
- HUD open button on the left edge, UISizeConstraint, outside the thumbstick zone.
- Popups: ImageLabel + UIScale + transparent TextButtons over the baked BUY/CANCEL areas.

## 4. Motion (one LocalScript)
- Hover: Size x1.07 + lift, Back easing 0.12s. Down: x0.93 0.06s. Up: back to hover/base with Back.
- Open: dim to 0.45, UIScale 0.5 -> 1 Back 0.45s. Close: 0.18s In.
- Float: TweenInfo(0.9-1.5s, Sine, InOut, -1, true) per model, different times.
- Rays: ONE Heartbeat loop rotating all rays only while the shop is visible, alternate direction.
- Purchases: MarketplaceService:PromptProductPurchase with real product ids; demo popup until ids exist.
- Luau gotcha: a line starting with `(` after a statement = "Ambiguous syntax" and the whole script dies. Assign to a local first.

## 5. Verify
Play -> client execute_luau to open the shop + read ray rotation -> screen_capture -> get_console_output must be empty -> stop. Tell the user to save (Ctrl+S).
