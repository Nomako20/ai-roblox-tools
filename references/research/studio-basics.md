# Roblox Studio Basics for AI Coding Agents

Working reference for agents editing Roblox Studio projects. Read before placing any new script, module, remote or UI. Domain skills (networking, data, GUI, performance) hold the deep detail; this file is the map.

## 1. Where everything goes

Rule of thumb: if a client must never see it, it lives on the server side (ServerScriptService or ServerStorage). Anything replicated to every client is public, including its code.

| Container | Who gets it | Put here | Never put here |
|---|---|---|---|
| Workspace | Everyone (3D world) | Map geometry, spawned models, world props, Terrain, Camera | Secrets, server-only state, scripts that hold game logic (tag instances with CollectionService instead) |
| ServerScriptService | Server only | Server bootstrap Script, server ModuleScripts (services), server config | LocalScripts, anything a client must `require` |
| ServerStorage | Server only | Large templates, hidden maps, server-only ModuleScripts, items not yet needed | Scripts that must run (they do not run from here) |
| ReplicatedStorage | Server and clients | Shared pure ModuleScripts (types, constants, helpers), item definitions without secrets, remotes folder, clone-able templates | Secrets, API keys, drop rates or hidden detection thresholds, authoritative state, LocalScripts (they do not run) |
| ReplicatedFirst | Clients first, before everything | Minimal loading screen, essential startup pieces | Heavy assets, game logic |
| StarterGui | Copied to each PlayerGui on join | ScreenGui templates, HUD and menus | Gameplay logic on the server side |
| StarterPlayer > StarterPlayerScripts | Client, runs on join | Client bootstrap LocalScript, controllers (input, camera, UI) | Server logic, trusted values |
| StarterPlayer > StarterCharacterScripts | Client, runs each spawn | Per-character client effects (animations hooks, character-bound UI) | Anything that must survive respawn |
| StarterPack | Copied to backpack on spawn | Tools, plus LocalScripts that set up tools | Stock items that depend on server state |
| Lighting | Everyone | Lighting, atmosphere, sky, post effects | Gameplay scripts |
| SoundService | Everyone | Global sound settings, music and ambient containers | Hidden game logic |
| Teams | Everyone | Team objects (names, colors) | Team logic; keep the rules in a server module |

The Roblox docs describe the same split: ServerScriptService and ServerStorage are server-only, ReplicatedStorage and ReplicatedFirst replicate, and StarterGui is copied per player. Lighting and SoundService are environment containers. The docs page we checked did not cover Teams in detail, so treat the Teams row as a convention.

### Example project tree

```
ServerScriptService/
  Bootstrap            (Script: requires and starts each server service once)
  Services/            (ModuleScripts: DataService, CombatService, ShopService)
  Config/              (ModuleScripts: prices, drop rates, server-only tuning)
ServerStorage/
  Maps/                (large hidden maps, moved into Workspace at runtime)
  Templates/           (server-only spawn templates)
ReplicatedStorage/
  Shared/              (ModuleScripts: Types, Constants, Util, ItemDefs without secrets)
  Remotes/             (RemoteEvents and RemoteFunctions, one per action, named by domain)
  Templates/           (models and UI pieces clients clone)
ReplicatedFirst/
  LoadingScreen        (LocalScript + minimal ScreenGui)
StarterGui/
  HUD                  (ScreenGui, DisplayOrder 10, ResetOnSpawn false)
  Menus                (ScreenGui, DisplayOrder 50)
  Popups               (ScreenGui, DisplayOrder 100)
  Notifications        (ScreenGui, DisplayOrder 150)
StarterPlayer/
  StarterPlayerScripts/
    Bootstrap          (LocalScript: requires and starts each controller once)
    Controllers/       (ModuleScripts: InputController, UIController, CameraController)
Workspace/
  Map/                 (world geometry)
  Spawns/              (SpawnLocation parts)
```

## 2. UI placement on screen

Each visible layer gets its own ScreenGui. Do not stack everything in one ScreenGui, because one broken layout then hides or reorders the rest.

| Layer | Purpose | DisplayOrder (our convention) | ResetOnSpawn |
|---|---|---|---|
| World UI (BillboardGui, SurfaceGui) | Name tags, floating prices | n/a (world space) | n/a |
| HUD | Health, currency, minimap, buttons that stay on screen | 10 | false |
| Menus | Shop, inventory, settings | 50 | false (or true if it should close on death) |
| Popups and dialogs | Confirmations, reward screens | 100 | true for per-life screens |
| Notifications and toasts | Short messages | 150 | false |
| Debug | Developer overlays | 900, hidden in release | n/a |

The DisplayOrder numbers are a project convention we chose, not a Roblox rule. Only the relative order matters: higher draws on top. Leave gaps so you can insert a layer later.

ResetOnSpawn: a ScreenGui that is a direct child of StarterGui with `ResetOnSpawn = false` is cloned once and survives respawn. With the default `true`, it is deleted and re-cloned on each respawn, so any state held in its objects is lost. Nested deeper under StarterGui, it is re-cloned too. Use `false` for HUD and menus, `true` only for screens that should reset.

### Screen edges and safe areas

- **IgnoreGuiInset:** leave `false` by default. Set `true` only on purpose, because it changes where the top-left corner sits relative to the top bar. Positions measured across ScreenGuis with different values need converting to one coordinate space first.
- **ScreenInsets and ClipToDeviceSafeArea:** choose per container which device cutouts and the top bar should be respected. Clipping to the safe area is on by default; check it when a menu gets cut at the edges of a notched phone.
- **Interactive UI:** the GUI guidance says to keep interactive elements inside CoreUISafeInsets (or a deliberate alternative) and to check placement by measurement (AbsolutePosition, AbsoluteSize), not by eye.
- **Scale and Offset:** UDim2 is Scale (fraction of parent) plus Offset (pixels). Use Scale for position and Offset for fixed-size pieces, so layouts survive phones and tablets. Lay out repeated items with UIListLayout or UIGridLayout instead of hand-placed coordinates.

### Mobile thumb zones

Roblox's default controls use the screen corners, so keep them clear:

- **Bottom-left:** reserved for the dynamic thumbstick. It accepts touches across a large part of the left side. Put no buttons there.
- **Bottom-right:** the jump button sits here, and players drag the camera with the right thumb. Custom buttons go beside the jump button, not on top of it, and should not cover the area where camera drags start.
- **Top bar:** the Roblox top bar and chat use the top edge. Keep important HUD text below it.
- **Thumb reach:** the most used action buttons belong in the bottom corners, near the thumbs. Keep menus and text in the center or top.

Test every HUD on a phone-sized device simulator in landscape, because the phone is the hardest case. A simulator cannot show thumb reach or notches, so check a real device before calling the layout finished.

## 3. Script rules for AI agents

1. **Small files, one job.** Aim for under about 200 to 300 lines per file. A file that grows past that gets split by responsibility (combat rules, shop, data), not by arbitrary chunks.
2. **One bootstrap, many modules.** Exactly one server Script and one client LocalScript start things. Everything else is a ModuleScript that returns a table. The bootstrap requires each module once and starts it in a known order. Do not put startup work in module top level that yields.
3. **Services on the server, Controllers on the client.** A service owns authoritative state and rules (DataService, ShopService). A controller owns client presentation and input (InputController, UIController). Clients ask services through remotes; services push results back.
4. **Remotes in one folder, validated on the server.** Put every RemoteEvent and RemoteFunction in one folder, one per action, named by domain (for example `Shop_Buy`). Every handler on the server checks argument types, ranges, ownership, cooldown and the current game state before doing anything. Treat every argument as attacker-controlled.
5. **Never trust the client.** The client shows and predicts. The server decides. The client never sends a currency amount, damage number, inventory result or permission. It sends an intent ("buy item 12") and the server looks up the price itself.
6. **Clean up every connection.** Store every connection and every spawned task. Disconnect them at teardown, for example when a character dies or a UI closes. Otherwise handlers stack up after respawn.
7. **Use task.wait, not wait.** Use `task.wait`, `task.spawn`, `task.delay` and `task.defer`. Never write a `while true do` loop without a yield inside it.
8. **TweenService for UI motion.** Animate position, size and transparency with TweenService. Do not write per-frame Heartbeat loops for simple UI movement.
9. **Build UI as real instances.** Make frames, labels and buttons as Instances in Studio (or cloned templates in ReplicatedStorage). Keep the Luau code to filling text, showing or hiding, and wiring events. Do not generate a whole screen from a 1,000-line script.
10. **Name things for the next reader.** Modules are PascalCase (`ShopService`). Remotes are `Domain_Action`. Attributes and tags are lowercase or camelCase and documented in one place. Use one language for names, comments and UI text, and follow the project's existing choice.
11. **Read before you write.** Inspect the existing folder, module names and remote names first. Reuse a proven module instead of rebuilding it. Read the file back after every edit.
12. **Keep secrets out of replicated containers.** API keys, webhook URLs, admin lists and hidden thresholds belong in ServerScriptService or ServerStorage. Assume anything in ReplicatedStorage can be read by a player.

## 4. Before you finish: agent checklist

- [ ] Every new script is in the container from section 1, and no secret or server module is replicated.
- [ ] Each UI layer is its own ScreenGui with the planned DisplayOrder and ResetOnSpawn.
- [ ] Nothing sits in the bottom-left thumbstick area or over the jump button; the top bar is clear.
- [ ] Every remote handler validates input on the server.
- [ ] Connections and tasks created by a feature are cleaned up on teardown.
- [ ] Playtest ran (start_stop_play or the user's own playtest). If the user is already playing, do not stop their session; save and report at the end instead.
- [ ] Console is clean: no errors or warnings from the new code (check the output after the playtest).
- [ ] The HUD was checked in a phone-sized device simulator, landscape and portrait if the game supports both.
- [ ] Both Client and Server contexts were checked for the feature, not only one.
- [ ] Place saved (save_place or Studio save).
- [ ] The report lists what was not verified (real phone, real console, live server load) rather than claiming success.

## 5. Credits

- **roblox-brain** by TabooHarmony. Repo: https://github.com/TabooHarmony/roblox-brain (README at https://cdn.jsdelivr.net/gh/tabooharmony/roblox-brain@main/README.md). License: MIT, "Copyright (c) 2026 TabooHarmony" (LICENSE file checked). The README credits contributors MrFearTick (code references, networking, monetization) and eeyq (growth-design content). Idea taken: the skill-per-domain layout, the "quick reference plus full reference" split, and the core/gameplay/design/tools grouping. Local roblox-* skills appear to be the same names (see below); the raw SKILL.md path for a direct content comparison returned 404, so content identity is not verified.
- **Roblox Creator Docs** (create.roblox.com/docs). Pages used: projects/client-server, scripting/locations, projects/data-model, ui/position-and-size. License: not checked; cite only, do not copy text. Idea taken: which container runs where and what replicates.
- **Local roblox-architecture, roblox-gui, roblox-luau-patterns, roblox-networking, roblox-data, roblox-security, roblox-studio-mcp, roblox-performance, roblox-collaboration-mode** (~/.claude/skills). Author: not stated in the files. Each cites Roblox docs and other projects in its `sources:` list and marks some entries "original". Ideas taken: the quick-reference-first structure, authority model, remote validation, session-locked saves, the execute-read-back loop.
- **roblox-game** (~/.claude/skills\roblox-game). Author: not stated in the files. Not in the roblox-brain list. Ideas taken: MCP detection before acting, the playtest-and-verify habit.
- **External projects cited by the local skills** (not checked for license): ProfileStore (MadStudioRoblox), Blink (1axen), jecs (Ukendio), Kampfkarren luau guidelines, chrrxs robloxstudio-mcp (its README says MIT, per the roblox-brain README, not verified here).
- **Web search** (1 search, used for the roblox-brain license check).
