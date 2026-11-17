# Roblox simulator UI research (2025-2026)

**Method and limits.** I ran 13 web searches and fetched 8 pages. I did not view screenshots of any game, and most game-specific pages returned generic UI-kit listings. Where a claim is marked "not found", the search turned up nothing usable. Per-game facts are therefore thin. The section-by-section conventions below rest mainly on Roblox's own UI/UX and monetization docs plus the few game pages that were readable.

## 1. Shop screen

- **Gamepass listings carry name, effect and Robux price on one line.** Pet Simulator 99 wiki-style guides list items like "Lucky (200% hatch luck, 275 Robux)" and "Huge Hunter, 3,250 Robux" (progameguides, rowatcher). Showing the effect beside the price is the pattern described in the sources.
- **Sections seen in the sources:** an Exclusive/rotating shop (PS99 "Exclusive Shop", rotating eggs at roughly 400 Robux each), a permanent weekly-rotating bundle area (PS99 "Forever Pack", price scales with progress), and a Robux store with SHOP / GEAR / GAMEPASSES / MONEY tabs (Steal a Brainrot, allthings.how). The source names the tabs but does not say where they sit.
- **Featured/hero:** the only evidence is a UI-kit description of a large featured-item panel above a grid of gamepass cards (BuiltByBit kit listing). This is a vendor claim, not an observed game screen.
- **Bundles and emphasis:** Roblox's UI docs say the highest-value bundle should be larger with more padding to set it apart (Dragon Adventures example). Daily items are grouped by size and proximity (Tower Defense Simulator example). Source: create.roblox.com UI/UX page.
- **Limited timers:** PS99 events run "on a roughly biweekly cadence" (rowatcher). No on-screen countdown was described in the source.
- **Sale and discount tags:** not found. No DevForum or game source covered badge placement or percent-off labels.
- **Card shape, price-button style, rarity colours:** not found for these games. The only generic rules found: prices show in red when unaffordable, unusable buttons are greyed out (Roblox UI docs).

## 2. HUD layout

- **Minimal HUD, extra in menus.** Roblox's UI docs say to keep the HUD minimal, especially on mobile, and to show only what is relevant to the current context. A commercial-pack guide and a Roblox-doc passage both recommend health, currency and core action buttons on the HUD, with everything else in menus (Creation.dev guide, Roblox docs).
- **Currency:** Adopt Me's Bucks are described as "the money tab in the top right corner" (Adopt Me wiki, as quoted in search snippet). This is one wiki note, not a design spec. The wiki page itself returned an access-denied page to my fetch, so I rely on the search snippet only.
- **Tasks/quest tracker:** Adopt Me task prompts appear at the top of the screen (search snippet, guide site). A quest tracker top-right with checkboxes appears in a commercial GUI pack, not a verified game.
- **Bee Swarm Simulator:** the inventory's Sticker Book sits at the top of the inventory, with inbox and index at top right (Bee Swarm wiki Sticker page, search snippet).
- **Not found:** exact positions of the boosts strip, inventory button or menu bar in PS99, Grow a Garden, Fisch, Anime Vanguards or 99 Nights.

## 3. Other key screens

- **Daily/advent reward (Steal a Brainrot):** a calendar opens from an interaction with the in-world Christmas tree (E prompt). It shows the current day's reward with a Claim button. A missed day can be reclaimed via a Recover button for 49 Robux. Each reward must be claimed within 24 hours. Streak bonuses at 3, 7, 14 and 25 days. The source does not describe Claim button states or tabs (allthings.how).
- **Daily reward button state:** generic guidance says a claimed reward's button should visibly change (grey or check mark) (search snippet, daily-reward template listing). Not verified in a game.
- **Hive slots (Bee Swarm):** each hive slot shows the bee's face icon in the bee's colour (Bee Swarm wiki Hive page, search snippet).
- **Wardrobe (Dress to Impress):** a creator guide suggests a wardrobe panel with 5 to 10 named save slots for outfit switching (creator guide snippet). No game-verified source.
- **Rebirth lock labels:** Steal a Brainrot's shop marks items with "YOU NEED 5 REBIRTHS" above the item (allthings.how snippet, search result for Coins Shop).
- **Purchase prompt, toasts, loading screen, leaderboard, trade, settings:** not found for any of the ten games.
- **Shop open/close behaviour:** Roblox monetization docs say opening and closing the shop should be a seamless transition from gameplay (create.roblox.com monetization-foundations page).
- **Pet grid, egg opening:** Pet Simulator 99 has a Huge/egg system (rowatcher), but no UI layout was found.

## 4. Visual style

- **Fonts:** Roblox docs say choose fonts for legibility first and keep to one or two families. A font guide names the built-in GothamBold and GothamMedium as clear at most sizes and warns against thin or script fonts on small screens (creation.dev guide). Lilita One, Fredoka and Luckiest Guy were not confirmed for any of these games by any source.
- **Text scaling:** the font guide notes TextScaled helps on mobile but can distort some fonts.
- **Outline thickness, rarity colours, ray or bounce animations:** not found. The only related material is generic UI-kit marketing (Cartoony, Stud UI packs). These are not evidence of what the games use.
- **Consistency:** Roblox docs say to keep one stat colour everywhere (e.g. health always green) and to use square red close buttons with a white X in the top-right corner of dialogs.

## 5. Monetization patterns

- **Permanent offers:** PS99 "Forever Pack" is a permanent offer with bundles that scale with progress (rowatcher).
- **Event timers:** PS99 events are limited-time on a biweekly cadence (rowatcher).
- **Starter packs, timed popups, "best value" badges:** not found in any fetched game source.
- **Roblox guidance:** present each item's value in context of other options, explain what it does, and rotate stock to keep the shop inviting (Roblox monetization docs).
- **Ethical note from the source:** the rowatcher article is critical of PS99's monetization, which is useful as a warning about stacking paid boosts.

## 6. Commission designers and community

- DevForum portfolio threads exist for Roblox UI designers who specialise in simulator styles, including RIPWhipp (about three years, mostly simulator interfaces) and GameDevSky (commissions via DevForum or Discord). Source: DevForum portfolio threads. I did not verify their current availability or credits.
- Fiverr gigs advertise simulator UI packages with shop, inventory, coin counter and HUD. These are sales pitches, not evidence of convention.
- I did not find any designer who publicly documents "simulator UI conventions" on a page I could read. The DevForum "shop GUI redesign" thread returned blank on fetch.

## Gaps for the skill

- No game-level screenshots or verified UI measurements were obtained. Before the skill states specific layout rules for PS99 or Grow a Garden, someone needs to look at screenshots or the games in Studio.
- Sale-tag, rarity and card-shape conventions remain unverified.
- Adopt Me wiki and Bee Swarm/Anime Vanguards pages were blocked (HTTP 402/403 or access denied).

## Sources

- https://create.roblox.com/docs/production/game-design/ui-ux-design
- https://create.roblox.com/docs/en-us/production/game-design/monetization-foundations
- https://rowatcher.com/news/pet-simulator-99-inside-roblox-s-most-aggressive-monetization-machine
- https://progameguides.com/roblox/all-pet-simulator-99-gamepasses-are-they-worth-it-roblox/
- https://pet-simulator.fandom.com/wiki/Gamepasses_(Pet_Simulator_99)
- https://allthings.how/how-steal-a-brainrots-advent-calendar-rewards-work-and-how-not-to-miss-them
- https://bee-swarm-simulator.fandom.com/wiki/Hive
- https://bee-swarm-simulator.fandom.com/wiki/Sticker
- https://adoptme.fandom.com/wiki/Bucks (search snippet only; fetch blocked)
- https://www.creation.dev/blog/roblox-ui-design-best-practices
- https://robloxguifontlist.pages.dev/ (search snippet only)
- https://devforum.roblox.com/t/how-should-i-redesign-my-shop-gui/1553556 (fetch returned blank)
- https://devforum.roblox.com/t/user-interface-designer-skys-portfolio/683173
- https://devforum.roblox.com/t/ripwhipps-portfolio-ui-designer/4559562
- https://builtbybit.com/resources/cartoony-ui-frames-pro.111209/ (vendor listing)
- https://builtbybit.com/resources/grow-a-garden-template.104257/ (vendor listing)
- https://www.droidgamers.com/guides/anime-vanguards-raid-shop/ (fetch returned no UI detail)
- https://gfxcomet.gumroad.com/l/sidebar-tutorial (search snippet only)
