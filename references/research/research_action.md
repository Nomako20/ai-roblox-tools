# Action / Combat / Competitive Game UI: Research Notes (2025-2026)

Method: 12 WebSearch queries plus 6 WebFetch reads (one fetch returned 403, one was truncated). Most per-game claims below rest on search snippets or fan/aggregator sites, not official design documentation. Where that is the case, it is marked. Gaps are listed at the end.

## 1. Shop / battle pass / season pass

- **Brawl Stars (main-menu hub, not a shop page):** Home is a hub: the center shows the chosen brawler with rank, power and trophies; the left side holds Brawlers and Shop; the right side holds leaderboards and battle log. Fan guide, [samurai-gamers](https://samurai-gamers.com/brawl-stars/main-menu-guide/). Shop sections are reported as Offers, Daily Freebie, Cosmetics, Resources in a single horizontal track with no pop-ups, from a search snippet of a [design analysis](https://ixd.prattsi.org/2025/02/design-critique-brawl-stars/) (the critique itself does not discuss the shop when fetched; treat the section names as unverified).
- **Clash Royale:** Community analysis says yellow is used for the most important buttons, and that a popup rather than a full-screen window helps orientation ([The Rookies breakdown](https://discover.therookies.co/2020/02/24/game-design-ux-best-practices-detailed-breakdown-of-clash-royale/), search snippet only).
- **Stumble Guys (monthly, not daily):** Home screen quick-access row covers Shop, Customize, Friends, Clubs, Missions, Party, Play ([help center](https://stumbleguys.helpshift.com/hc/en/4-stumble-guys/faq/66-what-can-i-find-in-the-home-screen/)). The Market rotates monthly and is a separate section paid in Stumble Coins, while Daily Missions refresh every day ([FAQ](https://stumbleguys.helpshift.com/hc/en/4-stumble-guys/faq/265-what-s-new-stumble-coins-drops-the-market)). Update 0.86 shipped the new menu through a staged split: 10% of players in one of four test groups, then full rollout ([patch notes](https://www.stumbleguys.com/news/update86), snippet).
- **Fortnite battle pass:** Pass screen shows buy-levels and reward categories; Chapter 6 Season 4 had 100+ rewards, some unlocked through tasks offered to pass owners ([Beebom](https://beebom.com/fortnite-chapter-6-season-4-battle-pass-rewards); [VideoGamer](https://www.videogamer.com/?p=500585), snippet).

## 2. Crate / gacha / reveal

- **Clash Royale chests:** Community simulator describes tapping a chest; the first four taps each carry a chance to upgrade rarity, the fifth opens it, with tiers Common, Rare, Epic, Legendary, Champion. Approximate, fan tool ([RoyaleTracker](https://royaletracker.gg/chest-simulator), snippet).
- **Honkai: Star Rail:** Pull animation is personality-driven, and players read rarity from subtle differences in its playout ([PC Gamer](https://pcgamer.com/honkai-star-rails-gacha-animations-have-no-right-to-go-this-hard), headline plus snippet).
- **Genshin Impact Wish:** A star streaks across a night sky and its colour signals rarity; the rarest pulls get a fuller descent ([HostedGG](https://hostedgg.com/blog/gacha-pull-reveal-color-culture), snippet).
- **Shared layout:** A Reddit comment notes Genshin and Star Rail use the same layout, which it calls functional but plain (snippet, [search results](https://www.pcgamesn.com/genshin-impact/copy-honkai-star-rail-banners)).
- **Reveal choreography (general):** N3twork's six-step card-reveal article argues games often skip straight to the reveal, a missed opportunity for staged drama ([Medium](https://medium.com/n3twork/choreographed-emotion-6-steps-to-a-great-card-reveal-ux-a6e6bb8487dd), **fetch returned 403**; claim from snippet only).
- **Blox Fruits:** Update 27 (Aug 2025) reportedly refreshed the Random Fruit gacha UI with animations and rarity tiers, per a fan-style guide ([Sportskeeda](https://www.sportskeeda.com/roblox-news/blox-fruits-lightning-update-guide), low authority). No source found describing the reveal steps.

Reveal step pattern supported by the above (inferred, not verified as one source): anticipation (container or star appears) -> tension build -> reveal scaled by rarity -> card/item landing with label -> "claim" or "again" buttons.

## 3. Combat HUD

- **Mobile thumb zone (Fortnite docs):** Primary actions go in the bottom corners. Map, timers and scores go top-centre or collapsible. Show at most about five or six active controls. Use context-adaptive HUDs that expand and collapse with the player's activity. Ability cooldowns should be long enough that players are not juggling four or more at once ([Fortnite docs](https://dev.epicgames.com/documentation/fortnite/designing-for-mobile-in-fortnite)).
- **Roblox guidance (conflicts with Fortnite in one point):** Keep important info and virtual buttons out of the bottom corners because the default thumbstick and jump button sit there. A button about 40% down the screen is reachable on a phone. Place custom buttons relative to the jump button, e.g. 0.8x size and 20 px to its left. Show contextual actions only when relevant, using proximity prompts ([Roblox cross-platform design](https://create.roblox.com/docs/ui/cross-platform-design)).
  - **Reconciliation for Roblox:** Put ability cluster up and left of the default jump button, not in the corner, and test on phone and tablet sizes.
- **Valorant (2025-2026):** Patch 10.03 updated minimap visuals for clarity; Patch 11.07 improved ability clarity ([Riot patch notes 11.07](https://playvalorant.com/en-US/news/game-updates/valorant-patch-notes-11-07/)). The 5.08 HUD overhaul drew complaints that elements change size when switching weapons ([Dot Esports](https://dotesports.com/valorant/news/valorant-players-and-pros-unhappy-with-the-new-ui-update), snippet). Riot removed the headshot notification under the kill banner to reduce non-essential info (per a Riot employee, [Sportskeeda](https://sportskeeda.com/valorant/valorant-community-disappointed-recent-ui-changes-affect-agent-utility-lineups-sova-viper), snippet).
- **Marvel Rivals:** Allied Health Bars is a per-hero setting (Settings > Combat); spectators can toggle outlines, health bars and names ([OpenCritic](https://opencritic.com/news/10995/allied-health-bars-in-marvel-rivals-can-be-a-game-changer-and-most-dont-know-they-exist), snippet). Players ask for team bars top-left and smaller enemy bars. NetEase reportedly reworking ability VFX for team-fight readability ([PC Gamer](https://www.pcgamer.com/games/third-person-shooter/marvel-rivals-is-making-some-big-visual-changes-to-cut-down-on-battlefield-chaos-which-is-wonderful-because-my-old-brain-cant-handle-that-level-of-overstimulation/), **truncated, headline only**). Season 3 brought "significant UI changes" (headline only, [OpenCritic](https://opencritic.com/news/18557/marvel-rivals-season-3-makes-significant-ui-changes)).
- **Blox Fruits:** Update 30 reportedly reworked stats, health and energy displays ([Beebom](https://beebom.com/blox-fruits-update-30-patch-notes/), snippet; release date conflicts across sources).
- **Brawl Stars:** Attack radius shown as a white ring during play, so players learn range without memorising it ([ixd critique](https://ixd.prattsi.org/2025/02/design-critique-brawl-stars/)).

Not found: specific HUD sources for kill feed, minimap or ammo in Blade Ball, Rivals, The Strongest Battlegrounds, Jujutsu Shenanigans, Dead Rails, Murder Mystery 2 or BedWars.

## 4. Lobby / main menu

- **Brawl Stars:** The Play button is the most prominent home control, large and bright yellow ([ixd critique](https://ixd.prattsi.org/2025/02/design-critique-brawl-stars/)). Events are highlighted with themed artwork and countdowns. The critique warns that growing feature count clutters the home screen and suggests grouping features into three toggleable tabs. Some destinations take too many taps (brawler info needs catalog then scroll; proposed fix is direct open).
- Fan guide places the Play button bottom-right with token count shown in its corner ([samurai-gamers](https://samurai-gamers.com/brawl-stars/main-menu-guide/)).
- **Stumble Guys:** Five-plus destinations in one home row (see section 1).
- Roblox official: UI combines visual design with information design for menus, shops and HUDs ([Roblox UI/UX docs](https://create.roblox.com/docs/en-us/production/game-design/ui-ux-design)).

## 5. Victory / defeat / rewards / rank

- **Fortnite Victory Royale:** Epic added extra time between a win and the post-match screen so players can celebrate (community post, [Epic forums](https://communities.epicgames.com/thread/new-battle-royale-season-settle-the-score-in-fortnite-showdown/vzi8), snippet; season not confirmed).
- No reliable 2025-2026 source found for level-up or rank-up layouts in the listed Roblox games. Gap.

## 6. Loadout, inventory, emotes, settings

- **Marvel Rivals hero gallery:** PC Gamer reports the older gallery looked cooler but was harder to use, a usability tradeoff ([PC Gamer](https://www.pcgamer.com/games/fps/marvel-rivals-hero-gallery-ui-used-to-look-a-lot-cooler-but-also-a-lot-harder-to-use), headline/snippet). NetEase said in March 2026 it was focusing on interface design as the roster grows (snippet from [a news site](https://tdp-frontend.pages.dev/article/2026-03-25-marvel-rivals-focuses-on-interface-design-as-hero-roster-expands-rapidly-a0e14f89), low authority).
- **Valorant settings:** Riot's UI settings FAQ covers HUD visibility and loadout display ([Riot support](https://support.riotgames.com/ko-kr/valorant/gameplay/valorant-ui-settings-faq), snippet).
- No verified source for emote-wheel layout.

## 7. Horror (Doors and similar): minimal / diegetic UI

- **Doors:** No Doors-specific HUD source found. An Endsights piece says Doors limits tools and visibility, which is about scarcity rather than layout ([Endsights](https://endsights.com/horror-game-design), snippet).
- **Horror UI guide** ([roblox-horror-game-ui.pages.dev](https://roblox-horror-game-ui.pages.dev), fan-made, fetched):
  - Show health through in-world cues (limping, blur, bloodied clothing); inventory via inspecting pockets or backpack; objectives as in-world notes.
  - Restraint: no flashy buttons, neon or complex layouts. Short labels ("Activate Shield").
  - Muted palette (dark blue, grey, green, brown, desaturated). Reserve red for warnings.
  - Distressed or handwritten-style fonts that stay readable; check licences.
- Dead Space is the cited reference for a health meter on the character's spine, per a [Substack essay](https://steventus.substack.com/p/glancing-signalis-part-1-immersion) (snippet).
- Caveat: the guide warns a cryptic diegetic UI is worse than a clean non-diegetic one.

## 8. Rarity colour conventions

- Common grey/white, Uncommon green, Rare blue, Epic purple: broadly consistent across wikis and game guides (snippets from [Heroes of the Storm wiki](https://heroesofthestorm.fandom.com/wiki/Rarity), [Borderlands 3 / Wonderlands rarity](https://playwonderlands.2k.com/game-guide/gear-loot/rarity/), [Caliber](https://playcaliber.com/en/news/474/item-rarity-levels-in-caliber), not opened).
- Legendary: usually orange or gold. Mythic: varies (gold, red, violet). Rainbow used for limited or special items ([Roblox DevForum](https://devforum.roblox.com/t/need-help-on-selecting-value-colors/793985), snippet).
- Higher tiers get stronger glow or effects (snippet from search results on rarity design).
- No single authoritative standard across games.

## 9. Typography and motion

- **Font names:** No source found naming the typefaces these games use. Gap.
- **Motion:** Animated glow or wiggle draws attention to important buttons (snippet from [GameAnalytics](https://www.gameanalytics.com/blog/how-to-make-your-game-ui-shine-and-increase-conversions)). Brawl Stars critique praises clear signifiers.

## 10. Gaps and caveats

- Squad Busters: only an AppMagic revenue analysis found; no UI sources.
- Not found for Blade Ball, Rivals, The Strongest Battlegrounds, Jujutsu Shenanigans, Dead Rails, Murder Mystery 2, BedWars: HUD, shop, reveal or lobby specifics.
- Official sources were scarce. Most data is from fan guides, aggregators, and search snippets. The Roblox and Fortnite docs are the most reliable.
- Cross-platform HUD: Roblox and Fortnite docs disagree on bottom corners; the reconciliation above is inference.

## Sources

- https://create.roblox.com/docs/ui/cross-platform-design
- https://create.roblox.com/docs/en-us/production/game-design/ui-ux-design
- https://dev.epicgames.com/documentation/fortnite/designing-for-mobile-in-fortnite
- https://ixd.prattsi.org/2025/02/design-critique-brawl-stars/
- https://samurai-gamers.com/brawl-stars/main-menu-guide/
- https://discover.therookies.co/2020/02/24/game-design-ux-best-practices-detailed-breakdown-of-clash-royale/
- https://royaletracker.gg/chest-simulator
- https://medium.com/n3twork/choreographed-emotion-6-steps-to-a-great-card-reveal-ux-a6e6bb8487dd
- https://hostedgg.com/blog/gacha-pull-reveal-color-culture
- https://pcgamer.com/honkai-star-rails-gacha-animations-have-no-right-to-go-this-hard
- https://www.sportskeeda.com/roblox-news/blox-fruits-lightning-update-guide
- https://beebom.com/blox-fruits-update-30-patch-notes/
- https://www.pockettactics.com/blox-fruits/update
- https://playvalorant.com/en-US/news/game-updates/valorant-patch-notes-11-07/
- https://dotesports.com/valorant/news/valorant-players-and-pros-unhappy-with-the-new-ui-update
- https://sportskeeda.com/valorant/valorant-community-disappointed-recent-ui-changes-affect-agent-utility-lineups-sova-viper
- https://support.riotgames.com/ko-kr/valorant/gameplay/valorant-ui-settings-faq
- https://opencritic.com/news/10995/allied-health-bars-in-marvel-rivals-can-be-a-game-changer-and-most-dont-know-they-exist
- https://www.pcgamer.com/games/third-person-shooter/marvel-rivals-is-making-some-big-visual-changes-to-cut-down-on-battlefield-chaos-which-is-wonderful-because-my-old-brain-cant-handle-that-level-of-overstimulation/
- https://opencritic.com/news/18557/marvel-rivals-season-3-makes-significant-ui-changes
- https://www.pcgamer.com/games/fps/marvel-rivals-hero-gallery-ui-used-to-look-a-lot-cooler-but-also-a-lot-harder-to-use
- https://tdp-frontend.pages.dev/article/2026-03-25-marvel-rivals-focuses-on-interface-design-as-hero-roster-expands-rapidly-a0e14f89
- https://www.stumbleguys.com/news/update86
- https://stumbleguys.helpshift.com/hc/en/4-stumble-guys/faq/66-what-can-i-find-in-the-home-screen/
- https://stumbleguys.helpshift.com/hc/en/4-stumble-guys/faq/265-what-s-new-stumble-coins-drops-the-market
- https://beebom.com/fortnite-chapter-6-season-4-battle-pass-rewards
- https://www.videogamer.com/?p=500585
- https://communities.epicgames.com/thread/new-battle-royale-season-settle-the-score-in-fortnite-showdown/vzi8
- https://endsights.com/horror-game-design
- https://roblox-horror-game-ui.pages.dev
- https://steventus.substack.com/p/glancing-signalis-part-1-immersion
- https://heroesofthestorm.fandom.com/wiki/Rarity
- https://playwonderlands.2k.com/game-guide/gear-loot/rarity/
- https://playcaliber.com/en/news/474/item-rarity-levels-in-caliber
- https://devforum.roblox.com/t/need-help-on-selecting-value-colors/793985
- https://www.gameanalytics.com/blog/how-to-make-your-game-ui-shine-and-increase-conversions
- https://wnhub.io/news/analytics/item-44477
- https://gamertagmythras.com/blog/roblox/best-roblox-pvp-games
