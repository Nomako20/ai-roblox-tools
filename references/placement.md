# Where UI goes

Sources: Roblox Creator Docs (cross-platform design, mobile input, ScreenGui, GuiService) and DevForum, collected in `research/research_placement.md`. Numbers marked (convention) are ours, not Roblox rules.

## Screen zones (landscape phone first, then check PC + console)
- **Top bar**: Roblox core UI owns the top-left and top-right. Use `ScreenGui.ScreenInsets = CoreUISafeInsets` for HUD so nothing goes under it.
- **Bottom-left**: thumbstick zone (dynamic thumbstick appears where the thumb lands). Nothing interactive here.
- **Bottom-right**: jump button. Put custom action buttons around it (the official sample places one left of jump at 0.8x its size), not fixed pixels.
- **Notches / cutouts**: `DeviceSafeInsets` handles them; keep `ClipToDeviceSafeArea` on.
- Reach: the top 40% of a tablet is hard to reach. Frequent buttons near the thumbs.

## HUD layout (convention)
- Currency pills: top-left under the top bar, stacked.
- Menu buttons (shop, pets, inventory, quests, settings): a column on the left edge, vertically centred, above the thumbstick zone.
- Boost/buff icons with timers: a row under the currencies or top-centre.
- Quest tracker: right side, upper half.
- Notifications/toasts: top-centre, short and stacked.
- Popups and shops: centred, with `UIAspectRatioConstraint`, max ~90% of the screen, a dim layer behind.

## ScreenGui layers (DisplayOrder, convention)
| Layer | DisplayOrder | Notes |
|---|---|---|
| HUD | 0 | ResetOnSpawn = false |
| Menus / shops | 10 | one open at a time |
| Popups / offers / prompts | 20 | dim background |
| Toasts | 30 | never block input |
| Loading / transitions | 100 | |

## Sizing
- Scale for layout, `UIAspectRatioConstraint` on panels, `UISizeConstraint` on HUD buttons so they don't get huge on TV.
- Touch targets at least 44-48 px; 8 px between targets.
- Text: `TextScaled` inside a sized box + `UITextSizeConstraint` (min ~14).
- `UIStroke` is in pixels: scale it with screen size in code or it gets thin on big screens.
- Images: uploads above 1024 px are downscaled. Use 9-slice (`ScaleType = Slice`, `SliceCenter`) for buttons/panels so one image fits every size.

## Console
- Every screen needs a first `GuiService.SelectedObject` and sensible `NextSelection*` links; use `SelectionGroup` so the cursor can't leave an open popup.
- Test in the Studio device emulator: phone, tablet, console.
