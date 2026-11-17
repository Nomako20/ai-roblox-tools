# Studio basics + code rules for AI agents

Short version. Full notes with sources: `research/studio-basics.md`. For deep coverage of architecture, data, networking and security use the skills in roblox-brain (TabooHarmony, MIT): https://github.com/TabooHarmony/roblox-brain

## Where things go (Explorer)
| Service | Put here | Never here |
|---|---|---|
| ServerScriptService | server Scripts + server-only ModuleScripts | anything the client needs |
| ServerStorage | server-only assets, maps, templates, secrets | - |
| ReplicatedStorage | shared modules, RemoteEvents (one `Remotes` folder), UI templates, shared assets | secrets, server logic |
| ReplicatedFirst | loading screen only | big assets |
| StarterGui | ScreenGuis built as real instances (HUD, Shop, Popups) | UI built entirely in code |
| StarterPlayerScripts | client bootstrap LocalScript + controllers | per-character stuff |
| StarterCharacterScripts | per-character client scripts | UI |
| Workspace | the world, 3D shop pads, NPCs | modules |
| SoundService | SoundGroups, UI sounds | - |

## Code rules
1. One responsibility per file; aim under ~200-300 lines. Split before it grows.
2. One bootstrap Script (server) and one LocalScript (client) that require ModuleScripts (Services on the server, Controllers on the client).
3. UI is made of real instances in StarterGui (or templates in ReplicatedStorage cloned per item). Code only wires behaviour.
4. RemoteEvents live in one folder. The server validates every argument, rate-limits, and never trusts prices or amounts sent by the client.
5. Purchases: `MarketplaceService` prompts on the client, grants only in `ProcessReceipt` on the server, idempotent.
6. Store every connection; disconnect on close or `Destroying`. No duplicated handlers after respawn (`ResetOnSpawn = false` for HUD).
7. `task.wait`/`task.spawn`/`task.delay`, never `wait`/`spawn`. No `while true` without a yield.
8. UI motion with TweenService (hover 1.07x, press 0.93x, open with UIScale 0.5 -> 1 Back). Avoid RenderStepped for UI.
9. Names: PascalCase instances, camelCase locals; folders `Remotes`, `Modules`, `Templates`.
10. Luau gotcha: a line starting with `(` right after a statement is "Ambiguous syntax". Assign to a local first.

## Before you finish
Play test -> console clean -> device emulator (phone, tablet, console) -> stop the test -> tell the user to save the place.
