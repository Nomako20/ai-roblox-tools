# Roblox strategy: how successful games are built

Use this when the user plans a game, a shop, an update, or asks why players leave or don't buy. Numbers are rules of thumb from how the platform behaves, not official targets; the Creator Dashboard is the source of truth for a specific game. Roblox changes its systems often, so check the current Creator Docs before quoting a policy.

## 1. How Roblox decides what to show players
Discovery is mostly the Home and Charts recommendation system. It tests a game with a small audience, watches what those players do, and shows it to more people if they behave well. What it reacts to:
- **Click-through on the thumbnail and icon.** Bad art = nobody clicks = the test ends early.
- **Early engagement.** Do new players stay past the first minutes and finish a first session of decent length.
- **Retention.** Do they come back the next day (D1) and the next week (D7).
- **Playtime per user and sessions per day.**
- **Monetization signals** (spend per user) matter too, but only after people stay. A game that sells hard but loses players does not grow.

Consequence: the first 5 minutes and the thumbnail decide whether a game ever gets traffic. Polish those before anything else.

## 2. The core loop
Every hit game has a loop the player understands in seconds and repeats for hours:
- **Simulator:** do action -> earn currency -> buy upgrade/pet -> do action faster -> rebirth for a multiplier -> repeat.
- **Tycoon:** collect money -> buy the next dropper/building -> earn more -> unlock new floor/area.
- **Garden/idle:** plant -> wait -> harvest -> sell -> buy rarer seeds -> come back later.
- **Obby:** next stage -> checkpoint -> harder stage -> skip-stage for the stuck.
- **Combat/round-based:** queue -> match -> rewards -> unlocks/cosmetics -> queue again.
Write the loop as one sentence before building. If you can't, the game isn't ready.

Layers on top of the loop, in order of importance:
1. **Progression** you can see (numbers going up, new zones, bigger pets).
2. **Collection** (pets, units, items with rarities; an index that shows what's missing).
3. **Goals** (quests, achievements, "next unlock in 3 levels").
4. **Social** (trading, leaderboards, showing off rare items, playing with friends).
5. **Events and updates** (limited items, weekly content).

## 3. The first session (FTUE)
- Player is doing the core action within **10-20 seconds**. No long intros, no walls of text.
- **First reward within the first minute**, first upgrade purchase within ~2-3 minutes.
- Teach by doing: arrows, glowing targets, one short instruction at a time.
- Show the long-term goal early (a rare egg, the next zone behind a gate, the top of the leaderboard).
- Hide advanced systems until they matter (trading, rebirth, crafting appear later).
- Mobile first: most players are on phones. Big buttons, nothing important under the thumbs.
- Measure it: track each tutorial step (see `research/` and Roblox AnalyticsService funnels) and fix the step where most people drop.

## 4. Retention
- **D1** is about the first session being fun and leaving a reason to return: a timer finishing, a daily reward, an egg hatching, a friend's invite.
- **D7** is about depth: more zones, collection goals, social status, weekly events.
- Tools that work: daily login rewards with a streak (day 7 big), quests that refresh daily, timed growth (plants, idle income), limited events, group rewards, offline earnings.
- Notifications and friend invites help, but only if the game is worth returning to.
- Don't punish missing a day too hard; a broken streak should sting, not make people quit.

## 5. Monetization
Revenue streams:
- **Gamepasses** (permanent): 2x currency, extra pet slots, auto-collect, VIP area, faster hatch. One-time purchase, should feel good forever.
- **Developer products** (consumable): currency packs, boosts, eggs, skip-stage, restock, revive. Can be bought again.
- **Subscriptions** where available for monthly perks.
- **Creator payouts from engagement** (Premium players' time in your game counts toward payouts): long, happy sessions earn even without purchases.

Price ladder rules:
- Offer something cheap (25-50 Robux) so the first purchase is easy; the first purchase is the hardest.
- Bigger packs give clearly more per Robux, and the UI says it (Good / Great / Most Value ribbons, bigger pile).
- A starter pack shown once to new players, with real value, converts well.
- Show the price in Robux on a green button, the item clearly, and what it does in a few words.
- **Never pay-to-lose:** free players must still have fun, or the game dies and payers have nobody to show off to.
- Paid random items (eggs, crates) must show odds. Follow Roblox's paid random item rules and age/region policy checks.
- Grant purchases on the server in `ProcessReceipt`, never trust the client.

Where to put offers:
- At the moment of need (out of currency -> currency pack; stuck on a stage -> skip; slow -> 2x speed).
- In the shop, organized by what it sells, best value marked.
- One popup at a time, not on every join. Too many popups hurt retention.

## 6. Thumbnails and icon (the storefront)
- The **icon** must read at tiny size: one clear subject, bright colours, a face or a recognizable item, no small text.
- **Thumbnails** show the fun moment: big pets, huge numbers, a giant explosion. Bold title text, high contrast.
- Test them: Roblox lets you A/B test thumbnails and icons. Change one thing at a time and keep the winner.
- Title: short and searchable (genre words players type), plus an update tag only when there really is one.
- Description: one line of what you do, then the update notes.

## 7. Updates and LiveOps
- Regular updates (weekly or bi-weekly for growing games) bring players back and refresh the algorithm's interest.
- Each update: new content (zone, egg, pets) + a limited reason to log in now (event, timer, code).
- Announce in the game (popup or board), in the description and in the community (Discord, group).
- Codes for free rewards are cheap and drive returns; put them in update posts.
- Don't break progress: test saves before releasing. A data-loss bug kills trust fast.

## 8. Data: what to watch
On the Creator Dashboard:
- **Qualified play-through / click-through rate**: storefront health.
- **D1 / D7 retention** and **average session length**: is the game fun.
- **Playtime per DAU**, **concurrent users (CCU)**.
- **Payer conversion** and **average revenue per paying user**: is the shop working.
- Funnels: tutorial steps, first purchase, first rebirth. Fix the biggest drop first.
Change one thing at a time and compare before/after; Roblox also supports experiments for A/B testing features.

## 9. Community
- A Roblox group (group rewards: join = small bonus) and a Discord for updates, codes and feedback.
- Show players' rare items (leaderboards, trade boards, announcements when someone hatches a mythic).
- Listen to bug reports quickly; fix exploits fast (they destroy economies).

## 10. Common reasons games fail
- Thumbnail/icon nobody clicks.
- Slow or confusing first minute.
- No clear goal after 10 minutes.
- Economy breaks (too fast = nothing left to do; too slow = boring).
- Over-monetized, popups everywhere, free players can't progress.
- No updates after launch.
- Lag on phones (too many parts, effects, unoptimized UI).
- Data loss or exploits.

## 11. A launch checklist
1. Core loop in one sentence, fun in the first 20 seconds.
2. First session tested with real players watching (not just you).
3. Shop with a cheap first purchase, clear value ladder, odds shown.
4. Daily reward + one timer that brings people back.
5. Thumbnail + icon tested on a phone screen size.
6. Analytics events on tutorial steps and purchases.
7. Saves tested (leave, rejoin, server shutdown).
8. Mobile, tablet and console checked in the device emulator.
9. Group + Discord ready, first update planned.
