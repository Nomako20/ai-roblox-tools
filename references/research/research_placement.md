# Roblox UI placement and engineering research

Research date: 2026-11-17. Sources are Creator Docs (create.roblox.com) and DevForum. Claims marked **(community)** come from DevForum or third-party pages. Claims marked **(unverified)** could not be confirmed in this run.

## Part A: Placement and engineering facts

### A1. Safe areas and top bar
- [ ] ScreenInsets enum values: None=0, DeviceSafeInsets=1, CoreUISafeInsets=2, TopbarSafeInsets=3. Source: https://create.roblox.com/docs/reference/engine/enums/ScreenInsets.md
- [ ] DeviceSafeInsets avoids camera cutouts/notches but adds no Roblox core UI inset. CoreUISafeInsets adds core UI (top bar) insets on top of device insets. TopbarSafeInsets adds the top bar's free space. Source: https://create.roblox.com/docs/reference/engine/classes/ScreenGui.md
- [ ] Default ScreenInsets is **conflicting**: the ScreenGui page lists CoreUISafeInsets in one place and FullscreenExtension as the SafeAreaCompatibility default in another. Verify in Studio before relying on it. Source: https://robloxapi.github.io/ref-temp/class/ScreenGui.html
- [ ] If IgnoreGuiInset is set to true while ScreenInsets is CoreUISafeInsets, ScreenInsets is switched to DeviceSafeInsets. Source: https://create.roblox.com/docs/reference/engine/classes/ScreenGui.md
- [ ] ClipToDeviceSafeArea defaults to true (clips GuiObject descendants to the device safe area). Source: https://create.roblox.com/docs/reference/engine/classes/ScreenGui.md
- [ ] Code path for top bar rect: GuiService.TopbarInset, with GetPropertyChangedSignal("TopbarInset"). Source (community): https://devforum.roblox.com/t/how-to-produce-a-topbar-based-on-topbarsafeinsets/2914413
- [ ] Known bug: TopbarSafeInsets sizes content to part of the screen on consoles. Source: https://devforum.roblox.com/t/screenguiscreeninsets-topbarsafeinsets-is-incorrect-on-consoles/4111410
- [ ] Rule for the skill: put HUD corners (top-left, top-right) on a ScreenGui with CoreUISafeInsets, and check on a phone and console in the Device Emulator. Source for emulator: https://devforum.roblox.com/t/3074034 (community)

### A2. Mobile placement and touch
- [ ] Default mobile controls occupy the bottom-left and bottom-right corners. Keep key info and virtual buttons out of those corners. No pixel values are given. Source: https://create.roblox.com/docs/ui/cross-platform-design
- [ ] Thumbstick zone: DynamicThumbstick appears where the thumb lands in the lower-left region; static Thumbstick is fixed lower-left; jump button is lower-right. Source: https://create.roblox.com/docs/scripting/input/mobile-input
- [ ] Custom action buttons: anchor them relative to the jump button, not to fixed pixels. The official sample places a button 20 px left of the jump button at 0.8x its size. Source: https://create.roblox.com/docs/ui/cross-platform-design
- [ ] Touch target minimum (no Roblox number found): Apple HIG 44x44 pt, Material 48x48 dp. Use 44 px minimum, 48 px preferred for mobile. Primary pages to check: https://developer.apple.com/design/human-interface-guidelines and https://m3.material.io. Secondary source: https://frontendchecklist.io/rules/accessibility/touch-targets
- [ ] Keep at least 8 px between adjacent touch targets. Source: secondary guide surfaced in search (not identified exactly); treat as a rule of thumb.
- [ ] Reach rule: frequently used buttons sit near the thumb zones; the page cites 40% from top as hard to reach on tablets. Source: https://create.roblox.com/docs/ui/cross-platform-design

### A3. Console and gamepad
- [ ] GuiService.SelectedObject sets the object the gamepad navigator has selected. Turn off auto-select, then set it yourself to start navigation. Source: https://developer.roblox.com/api-reference/class/GuiService
- [ ] SelectionGroup = true on a GuiBase2d limits gamepad navigation to that group. Source: https://create.roblox.com/docs/en-us/reference/engine/classes/GuiObject
- [ ] SelectionBehavior: Escape (default, prefers objects inside the group before leaving) or Stop (stays in group). Source: https://create.roblox.com/docs/en-us/reference/engine/enums/SelectionBehavior.md
- [ ] Set NextSelectionUp/Down/Left/Right on each GuiObject to build an explicit grid. Source: https://create.roblox.com/docs/en-us/reference/engine/classes/GuiObject
- [ ] Jumps between ScreenGui, SurfaceGui and BillboardGui: older threads say manual links are needed; newer posts say it works automatically. Verify in Studio. Source (community): https://devforum.roblox.com/t/ui-selection-between-screensurfacebillboardguis/2490753
- [ ] 10-foot UI guideline (text size, distance from TV): **(unverified)**, no official page found in this run.

### A4. Sizing and layout
- [ ] Position and Size are UDim2: Scale is a fraction of the parent, Offset is pixels, per axis. Source: https://create.roblox.com/docs/ui/position-and-size
- [ ] Scale-first for multi-platform layouts, mixed with Offset for fixed-size things. Community note: a UI made only of Scale can become unreadable on phones. Source (community): https://devforum.roblox.com/t/specific-details-about-ui-scaling-best-practices/3888004
- [ ] Community note: UIStroke takes Offset only, not Scale. Source: a DevForum thread from the same search, not identified exactly; re-check in the UIStroke reference before using.
- [ ] UIScale multiplies the parent's AbsoluteSize. Use it for hover/press tweens. Source: https://create.roblox.com/docs/en-us/ui/size-modifiers
- [ ] UISizeConstraint sets min/max size. UITextSizeConstraint sets min/max font size (with TextScaled). Constraints must be children of the object they constrain. Source: https://create.roblox.com/docs/en-us/ui/size-modifiers
- [ ] UIAspectRatioConstraint exists for aspect control; no detailed guidance found. **(unverified)** Source: https://create.roblox.com/docs/en-us/ui/size-modifiers
- [ ] UIListLayout: one row or column, keeps each child's size. UIGridLayout: uniform cells (CellSize, CellPadding, StartCorner, FillDirectionMaxCells). UIFlexItem: FlexMode, GrowRatio, ShrinkRatio. Source: https://create.roblox.com/docs/en-us/ui/styling/compatibility and https://developer.roblox.com/articles/applying-strokes
- [ ] UIStroke, UICorner (TopLeftRadius etc., UDim), UIGradient (Color, Offset, Rotation, Transparency). Source: https://create.roblox.com/docs/en-us/ui/styling/compatibility
- [ ] ApplyStrokeMode: **(unverified)**, not confirmed in this run.

### A5. Images
- [ ] 9-slice: set ScaleType = Slice and SliceCenter, e.g. Rect.new(30, 30, 34, 34). Source: https://create.roblox.com/docs/en-us/reference/engine/classes/ImageLabel
- [ ] Sprite sheets: ImageRectOffset + ImageRectSize; a size of 0 shows the whole image. Source: https://create.roblox.com/docs/reference/engine/classes/ImageLabel/ImageRectOffset
- [ ] Transparent pixels can turn black on upload (mirror of the reference); use alpha blending on edges. Source (mirror): https://robloxapi.github.io/ref-temp/class/ImageLabel.html
- [ ] Max upload 1024x1024: DevForum says larger images are downscaled to 1024x1024. No official confirmation found. Sources: https://devforum.roblox.com/t/why-is-the-max-image-resolution-1024x1024/1679078 and https://devforum.roblox.com/t/dramatically-increase-the-maximum-image-decal-texture-upload-size/649052
- [ ] Image moderation: **(unverified)**, no page fetched. Texture specs page, not fetched: https://create.roblox.com/docs/en-us/art/modeling/texture-specifications.md
- [ ] Preload: only essential UI (loading screen, menu, spawn-area assets). Call PreloadAsync on a UI container; it recurses. Loading the whole Workspace is called bad practice. Source: https://create.roblox.com/docs/projects/performance-optimization/load-times
- [ ] Known issue: PreloadAsync doesn't always show ImageLabels in time. Source (community): https://devforum.roblox.com/t/contentprovider-doesnt-preload-imagelabels/4039525
- [ ] Wrap outside/network calls in pcall. Source (community): https://devforum.roblox.com/t/how-to-properly-use-contentproviderpreloadasync/707832

### A6. Where UI instances live
- [ ] LayerCollector.ResetOnSpawn defaults to true: the container is cloned into PlayerGui on each respawn. False + direct child of StarterGui = cloned once, survives respawn. Source: https://create.roblox.com/docs/en-us/reference/engine/classes/LayerCollector.md
- [ ] ZIndexBehavior: Sibling (default; ZIndex orders siblings only) or Global (sorts all descendants by ZIndex). Source: https://create.roblox.com/docs/en-us/reference/engine/classes/LayerCollector.md
- [ ] DisplayOrder controls which ScreenGui draws on top. Detail not retrieved; check https://create.roblox.com/docs/reference/engine/classes/ScreenGui.md
- [ ] On-screen containers overview: https://create.roblox.com/docs/en-us/ui/on-screen-containers
- [ ] Templates: build screens in StarterGui (or ReplicatedStorage templates), clone at runtime. **(unverified in this run)**

### A7. Code structure for UI scripts (AI-agent rules)
- [ ] No official Roblox page on UI code organisation was found. DevForum agrees on: one bootstrap LocalScript, one ModuleScript per screen or controller, modules return tables, no circular requires. Sources (community): https://devforum.roblox.com/t/how-to-split-a-single-localscript-to-gui-into-many/914871 ; https://devforum.roblox.com/t/how-should-gui-data-and-functions-be-structured/3630812 ; https://devforum.roblox.com/t/help-with-modularisation-and-one-script-architecture/283811
- [ ] Clone from templates; do not build whole screens in code. (Practice from the threads above, community.)
- [ ] Connection cleanup: store every connection; disconnect when the screen closes or on Destroying. The engine does not garbage-collect active connections. Source: https://create.roblox.com/docs/performance-optimization/improve.md ; https://devforum.roblox.com/t/does-roblox-clean-up-event-listeners-for-me/602482
- [ ] Use TweenService for UI motion. Avoid RenderStepped for UI; reserve it for camera or per-frame visuals. Source (community): https://devforum.roblox.com/t/properly-using-runservice-along-with-preventing-memory-leaks/1183703
- [ ] Libraries: Fusion is called beginner-friendly but not fully stable (2024 thread); React-Lua is called mature. Source: https://devforum.roblox.com/t/fusion-vs-react-lua-which-one-to-use-for-long-term-development/2781328
- [ ] Roact is deprecated; use React-Lua. Source: https://devforum.roblox.com/t/roact-ui-framework-crash-course-deprecated/796618
- [ ] Iris and Vide: no 2025 comparison found. **(unverified)**
- [ ] Keep each file short. Size limit (e.g. 300 lines) is a suggestion, not sourced.

## Part B: Public AI skills, prompt files and repos

License column: "listed" means the license came from an aggregator or README snippet, not from the repo's LICENSE file. Check before crediting.

| Name | Author / org | URL | License | Covers |
|---|---|---|---|---|
| roblox-luau (in awesome-gamedev-agent-skills) | gamedev-skills | https://github.com/gamedev-skills/awesome-gamedev-agent-skills (aggregator: https://claudeskills.info/skills/gamedev-skills/awesome-gamedev-agent-skills/roblox-luau/) | Apache-2.0 (listed) | Luau services, Instances, events, client/server |
| roblox-brain | TabooHarmony | https://cdn.jsdelivr.net/gh/tabooharmony/roblox-brain@main/README.md | MIT (listed in README) | 28 skills incl. roblox-luau-core; Claude Code, Cursor, Codex |
| roblox-game-skill | brockmartin | https://github.com/brockmartin/roblox-game-skill | not shown | Broad game-dev router with lazy references |
| roblox-api, roblox-core | stackfox-labs | https://vibeindex.ai/skills/stackfox-labs/luau-skills/roblox-api | not shown | Engine APIs; client/server structure |
| roblox-ts, luau-roblox | christopher-buss; kursku | https://skills.sh/christopher-buss/skills/roblox-ts ; https://www.skills.sh/kursku/skills/luau-roblox | not shown | roblox-ts and Luau guidance |
| robloxstudio-mcp (fork) | Chrrxs (base: boshyxd) | https://github.com/Chrrxs/robloxstudio-mcp | MIT (listed) | Studio MCP server and plugin |
| roblox-studio skill | ellmos-ai | https://claudskills.com/skills/roblox-studio/ | MIT (listed, source github.com/ellmos-ai/skills) | Studio SKILL.md |
| Awesome Roblox (lists) | awesome-roblox; elevenpassin; JodeRBX; PhoenixCausesOof | https://devforum.roblox.com/t/awesome-roblox-curated-list-of-roblox-development-resources/2779302 ; https://www.context-awesome.com/list/elevenpassin/awesome-roblox ; https://www.context-awesome.com/list/joderbx/awesome-roblox | not verified | Curated links: tools, libraries, UI |
| Awesome roblox-ts | coyenn | https://www.context-awesome.com/list/coyenn/awesome-roblox-ts | not verified | roblox-ts packages |
| RbxSync Cursor rules | Smokestack-Games | https://tomevault.io/tome/Smokestack-Games/rbxsync | not verified | Luau: strict types, task.wait over wait() |
| awesome-cursorrules | ikhare | https://github.com/ikhare/awesome-cursorrules | not verified | Index of cursor rule files (no Roblox entry seen) |
| @rbxts/react | littensy | https://npmjs.com/package/@rbxts/react | MIT (listed) | React bindings for roblox-ts UI |
| Roact (deprecated) | Roblox | https://github.com/roblox/roact | Apache-2.0 (listed) | Declarative Lua UI; use React-Lua instead |
| Vide | littensy | https://github.com/littensy/vide | not verified | Signals-based Luau UI library |
| grand-hawk/ui-components | grand-hawk | https://repos.ecosyste.ms/hosts/GitHub/repositories/grand-hawk%2Fui-components | MIT (listed) | roblox-ts UI component library |

Not found in this run: a game UI design skill (none surfaced in the searches); the official Roblox Studio MCP license.

## Gaps to close before writing the skill
1. Official 1024x1024 upload limit and image moderation rules.
2. 10-foot UI guideline and console safe margins.
3. ApplyStrokeMode and UIAspectRatioConstraint details.
4. Iris and Vide status.
5. Default ScreenInsets value (sources conflict).
