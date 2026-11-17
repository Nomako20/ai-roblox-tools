# Roblox UI conventions by genre, plus casual mobile patterns (2025-2026)

Research status: 16 WebSearch calls and 4 WebFetch calls. Evidence is thin for most Roblox genres. Most search hits were DevForum threads, SEO pages, or asset-pack listings. Where a claim has no source, it is marked UNVERIFIED. Nothing here was checked in a live game.

## Cross-genre baseline (Creator Hub)
- Hierarchy first: "Put the most important information first." Show only contextually relevant controls, and swap buttons by role, location, or held item. Source: https://create.roblox.com/docs/production/game-design/ui-ux-design
- Buttons sit in a container so they look interactive. Gray means unusable. An X closes dialogs. A lock icon marks locked features. Source: same page.
- Keep mobile minimal. HUD layouts and button placement can be tested with Experiments. Source: same page.
- Feedback on every action: button state changes, purchase sounds, progress bars. Source: same page.

## Tycoon (Restaurant Tycoon 3, Retail Tycoon 2, Lumber Tycoon)
- **Screens:** menu-driven. Actions use a toolbar at the bottom of the screen. Build Mode and a Menu tool (add/remove dishes by category) are separate tools. Source: https://restaurant-tycoon-3.pages.dev/ (fan guide, community-sourced)
- **Shop:** gamepasses and developer products bought with Robux, plus a code-entry field. Wiki lists 6 gamepasses; may be outdated. Source: https://rt3.fandom.com/wiki/Shop
- **Gamepass copy:** convenience boosts such as auto collect and precision building; none required to progress (fan guide). Source: https://restaurant-tycoon-3.pages.dev/
- **Tab organization:** UI kit guides recommend tabs (Buildings / Upgrades / Gamepasses) instead of one long list. Source: https://robloxuikittycoontheme.pages.dev (SEO-grade; weak)
- **Buy pads (3D):** tycoon purchases are usually floor pads that show a label such as "Buy Dropper 2 - $500" on a brick. Show only when affordable. Source: https://devforum.roblox.com/t/need-advice-on-how-to-make-a-purchasing-system-in-a-tycoon/3090179 and https://generalistprogrammer.com/tutorials/how-to-make-a-roblox-tycoon-game (tutorial sites, weak)
- **Security:** keep buy logic on the server; client-side cash logic is called the most common tycoon exploit. Source: https://howtomakeatycooninrobloxstudio.pages.dev/ (weak; cross-check with Creator Hub monetization docs)
- **Unique:** the buy pad is world-space UI, not a ScreenGui. Retail Tycoon 2 specifics: UNVERIFIED.

## Obby / tower (Tower of Hell, stage-counter obbies)
- **Stage counter:** described as one of the most motivating obby UI elements. Source: https://www.creation.dev/blog/roblox-obby-design-guide (general guide)
- **Skip-stage purchase:** typical setup is a ScreenGui button that calls MarketplaceService:PromptProductPurchase on a developer product; the stage grant happens on the server after PurchaseGranted. Source: https://devforum.roblox.com/t/skip-stage-button-for-obby-game/1399543 (search snippet; the fetch returned an empty page, so only the snippet was seen)
- **Known pitfalls:** skip can respawn players at spawn or a random position instead of the checkpoint. Stage counter and checkpoint must update together. Source: same DevForum thread (snippet) and https://devforum.roblox.com/t/how-to-add-a-skip-button-to-a-obby/1341897
- **Feedback:** a DevForum thread notes the UI covers nearly half the screen and suggests a hide-UI button. Source: https://devforum.roblox.com/t/feedback-on-my-new-obby-game/2232727
- **Tower of Hell specifics:** UNVERIFIED (no source found).

## Roleplay (Brookhaven, Berry Avenue)
- Phone UI, house menus, avatar editor: NO EVIDENCE FOUND. The search returned restaurant-menu and phone-ordering results. Next step: search the Brookhaven or Berry Avenue wiki for the phone app, or inspect the games directly.
- Generic note from Creator Hub: roleplay players are experienced and familiar with conventions, so they need less tutorial text. Source: https://create.roblox.com/docs/production/game-design/ui-ux-design

## RPG / adventure (quest log, NPC dialogue with portrait, skill tree, map)
- **Portrait dialogue:** a DevForum thread asks for a dialogue box with a portrait beside it; a reply points to Roblox's built-in Dialogue System for runtime UI customization. Source: https://devforum.roblox.com/t/dialogue-system-with-character-portraits/228999
- **World-space dialogue:** a custom system used a world-space UI instead of a screen dialogue box. Source: https://devforum.roblox.com/t/custom-dialogue-system/514214
- **Quest log, skill tree, map:** NO EVIDENCE FOUND for Roblox specifics. The only related item is an itch.io post on quest-step lists (non-Roblox). Source: https://itch.io/blog/664783/creating-a-list-to-track-quest-steps

## Racing / driving (Driving Empire, dealership, speedometer)
- **Speedometer:** a needle rotated by tween, mapped from velocity over max speed. Round gauges use UICorner and UIGradient layered frames. Source: https://devforum.roblox.com/t/2508569 and https://devforum.roblox.com/t/need-feedback-on-speedometer-gui/3026051
- **HUD replacement:** turn off the default seat "HeadsUpDisplay" first. Source: https://devforum.roblox.com/t/replacing-the-speedometer-gui-for-roblox/2171120
- **Dealership:** the paid UXR Vehicle Systems Pack lists dealership gating by team, group rank, or gamepass, plus leaderstats.Cash currency. Source: https://builtbybit.com/resources/uxr-vehicle-systems-pack.35421/update/152272/ (product listing, not verified)
- Driving Empire layout details: UNVERIFIED.

## Tower defense (Toilet Tower Defense, Anime Defenders)
- **Tower panel:** clicking a tower opens a HUD panel showing name, level, and upgrade cost (computed from price and level). Source: https://coddy.tech/learn/courses/roblox_game_tower_defense/tower_panel
- **Wave counter:** a HUD label bound to a workspace attribute for the current wave. Source: https://coddy.tech/learn/courses/roblox_game_tower_defense/wave_counter
- **Upgrade UI feedback:** a DevForum thread says the upgrade menu looked cluttered and did not match the rest of the UI. Source: https://devforum.roblox.com/t/feedback-needed-for-td-upgrade-ui/3295956
- **Mobile-first:** most Roblox users are on mobile; check layout at smallest and largest sizes. Source: https://devforum.roblox.com/t/creator-spotlight-how-unroot-designs-ui-for-marbles-mermaids-and-more/3077233
- **Anime Defenders banner and summon:** every banner has one Secret, one Mythic, one Legendary, and a pity system (50 pulls for the current Legendary, 400 for the Mythic). Source: https://www.droidgamers.com/guides/anime-defenders-banners-guide/
- **Unit hotbar layout:** NO EVIDENCE FOUND for Anime Defenders screen placement. Hotbar is UNVERIFIED.

## Fishing (Fisch reel minigame)
- **Reel bar:** appears mid-screen or near the bottom-left; the first-time tutorial sits over the bar at the bottom. Hold or release click to keep the marker in a moving zone; progress fills while in zone. Source: https://allthings.how/?p=330118 and https://www.destructoid.com/go-fishing-roblox-guide/ (player guides)
- **Design advice:** a static bar is boring; vibrate and change color as the catch nears escape. Source: https://robloxfishingsystemscriptmechanics.pages.dev (SEO; weak)
- **Architecture:** client handles feel (bar movement, splashes); server stays authoritative. Source: same.
- Exact sizes, colors, and tuning: UNVERIFIED.

## Clicker / idle
- Few GUI-based idle clickers exist on Roblox; Cookie Clicker suggested as reference. Source: https://devforum.roblox.com/t/thoughts-on-gui-based-idle-game-mechanics/1482122
- Rebirth GUI did not fit mobile screens in one player report; fix is UI scaling. Source: https://devforum.roblox.com/t/what-should-i-add-to-my-simulator-game/2051076
- Rebirth button: keep hidden or locked until affordable, or show the cost clearly. Source: https://robloxtycoonrebirthsystemscript.pages.dev (weak)

## Party / minigame (lobby voting, round timer)
- Keep the vote UI hidden until voting time. Show map images, not default buttons, in voting slots. Source: https://robloxlobbyscript.pages.dev and https://robloxvotingsystemscriptmap.pages.dev (SEO; weak)
- Sync late joiners on PlayerAdded. Timer server-side, UI animation client-side. Same sources.
- Explicit round states: Intermission, Round Starting, Game Over. Same sources.

## Horror
- Stamina and sanity bars in an info frame are used in The Backrooms: Reimagined devlog; developer says the design is not final. Source: https://devforum.roblox.com/t/the-backrooms-reimagined-devlog-3-blackout/2802280
- Feedback: a HUD that is too dark hurt readability. Source: https://devforum.roblox.com/t/how-do-i-improve-game-gui/2492832
- Design-in-world UI approach for horror (SEO source, weak): https://roblox-horror-game-ui.pages.dev
- Flashlight UI: NO EVIDENCE FOUND as a dedicated UI pattern.

## Casual mobile patterns (Royal Match, Candy Crush, Clash of Clans, Coin Master, Subway Surfers)

**End-of-round and upsells (Royal Match)**
- EoR screen shows upsells for extra moves and the battle pass, with objectives beside the coin balance. Extra-move prices are tiered. Source: https://naavik.co/deep-dives/royal-match/
- Quit prompt tells the player what they will lose, then a large green continue button. Source: same.
- Timed infinite lives granted as rewards. Source: same.

**Events on home screen (Royal Match)**
- Time-limited events placed along the screen edges; staggered so some are always active. Source: same.

**Battle pass (Royal Match)**
- Monthly pass priced above $10; buyers get a temporary boost and a profile frame. Source: same.

**Prize road (Royal Match)**
- Free rewards visible in a sequence; next rewards locked behind a low-price purchase. Source: same.

**Piggy bank**
- Piggy bank: players fill it with in-game currency and make a one-time purchase to open it. Source: https://fungies.io/piggy-bank-monetization-mechanism-for-mobile-games.md (vendor blog). Farm Heroes Saga analysis argues the banked amount feels earned. Source: https://blog.incymo.ai/?p=176

**Shop**
- Royal Match: rotating offers and promotions; coin packs take more vertical space (3 instead of 4 visible). Sources: https://naavik.co/digest/royal-match-finding-success-through-iteration/ and https://www.gamigion.com/?p=31815
- Magic Sort: shop icon shows a notification marker on the bottom bar, but not inside the shop. Source: https://www.gamigion.com/?p=29235

**Daily reward calendar and spin wheel**
- Login calendars are often tied to events and introduced during first-time experience. Spin wheels: one spin per day, with card-flip or chest alternatives. Source: https://mycred.me/?p=91070 and https://skillselion.com/skills/rshankras/claude-code-apple-skills/variable-rewards
- Ethics: a UX guide argues a spin should stay free, with disclosed odds. Source: https://vp0.com/blogs/spin-the-wheel-daily-reward-ui-mobile
- Calendar streaks create sunk-cost pressure. Source: https://nerdbot.com/2026/08/18/the-psychology-behind-daily-rewards-in-video-games/

**Battle pass**
- Main long-term hook; daily rewards and missions feed it. Source: https://dev.to/hiroshi_takamura_c851fe71/how-to-build-a-reward-economy-for-a-mobile-game-2e3f

**Offer popups and manipulation**
- vzbv (German consumer group, 2025) tested Clash of Clans and Subway Surfers. Clash of Clans pairs an imperative buy call with a specific offer; Subway Surfers prompts more ad views for rewards; offers appear without the player visiting the shop. Coin Master was not in the test. Source: https://www.vzbv.de/sites/default/files/2025-04/25-03-11_Paper_vzbv_Manipulative_design_unfair_practices_online_games.pdf
- Lives mechanic (Candy Crush): timed waits per life create artificial scarcity. Source: parent guide https://screenwiseapp.com/guides/candy-crush (non-academic)
- Research: a 2024 study of 1,496 games found dark patterns in both problematic and benign games; pop-ups and redirections were among the most common. Source: https://www.arxiv.org/abs/2412.05039 and https://apo.org.au/sites/default/files/resource-files/2025-04/apo-nid330381.pdf
- Spin-based design (Coin Master) framed as a gamble. Source: https://www.deconstructoroffun.com/blog/2025/7/25/what-happened-to-coin-master-after-monopoly-go

**Gaps:** no source found on popup frequency, banner placement, dismiss patterns, or Candy Crush / Coin Master shop layouts. Those need direct captures or a teardown.

## Sources
- https://create.roblox.com/docs/production/game-design/ui-ux-design
- https://restaurant-tycoon-3.pages.dev/
- https://rt3.fandom.com/wiki/Shop
- https://devforum.roblox.com/t/need-advice-on-how-to-make-a-purchasing-system-in-a-tycoon/3090179
- https://robloxuikittycoontheme.pages.dev
- https://www.creation.dev/blog/roblox-obby-design-guide
- https://devforum.roblox.com/t/skip-stage-button-for-obby-game/1399543
- https://devforum.roblox.com/t/how-to-add-a-skip-button-to-a-obby/1341897
- https://devforum.roblox.com/t/feedback-on-my-new-obby-game/2232727
- https://devforum.roblox.com/t/dialogue-system-with-character-portraits/228999
- https://devforum.roblox.com/t/custom-dialogue-system/514214
- https://itch.io/blog/664783/creating-a-list-to-track-quest-steps
- https://devforum.roblox.com/t/2508569
- https://devforum.roblox.com/t/need-feedback-on-speedometer-gui/3026051
- https://devforum.roblox.com/t/replacing-the-speedometer-gui-for-roblox/2171120
- https://builtbybit.com/resources/uxr-vehicle-systems-pack.35421/update/152272/
- https://coddy.tech/learn/courses/roblox_game_tower_defense/tower_panel
- https://coddy.tech/learn/courses/roblox_game_tower_defense/wave_counter
- https://devforum.roblox.com/t/feedback-needed-for-td-upgrade-ui/3295956
- https://devforum.roblox.com/t/creator-spotlight-how-unroot-designs-ui-for-marbles-mermaids-and-more/3077233
- https://www.droidgamers.com/guides/anime-defenders-banners-guide/
- https://allthings.how/?p=330118
- https://www.destructoid.com/go-fishing-roblox-guide/
- https://robloxfishingsystemscriptmechanics.pages.dev
- https://devforum.roblox.com/t/thoughts-on-gui-based-idle-game-mechanics/1482122
- https://devforum.roblox.com/t/what-should-i-add-to-my-simulator-game/2051076
- https://robloxtycoonrebirthsystemscript.pages.dev
- https://robloxlobbyscript.pages.dev
- https://robloxvotingsystemscriptmap.pages.dev
- https://devforum.roblox.com/t/the-backrooms-reimagined-devlog-3-blackout/2802280
- https://devforum.roblox.com/t/how-do-i-improve-game-gui/2492832
- https://roblox-horror-game-ui.pages.dev
- https://naavik.co/deep-dives/royal-match/
- https://naavik.co/digest/royal-match-finding-success-through-iteration/
- https://www.gamigion.com/?p=31815
- https://www.gamigion.com/?p=29235
- https://fungies.io/piggy-bank-monetization-mechanism-for-mobile-games.md
- https://blog.incymo.ai/?p=176
- https://mycred.me/?p=91070
- https://skillselion.com/skills/rshankras/claude-code-apple-skills/variable-rewards
- https://vp0.com/blogs/spin-the-wheel-daily-reward-ui-mobile
- https://nerdbot.com/2026/08/18/the-psychology-behind-daily-rewards-in-video-games/
- https://dev.to/hiroshi_takamura_c851fe71/how-to-build-a-reward-economy-for-a-mobile-game-2e3f
- https://www.vzbv.de/sites/default/files/2025-04/25-03-11_Paper_vzbv_Manipulative_design_unfair_practices_online_games.pdf
- https://screenwiseapp.com/guides/candy-crush
- https://www.arxiv.org/abs/2412.05039
- https://apo.org.au/sites/default/files/resource-files/2025-04/apo-nid330381.pdf
- https://www.deconstructoroffun.com/blog/2025/7/25/what-happened-to-coin-master-after-monopoly-go
