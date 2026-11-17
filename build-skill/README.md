# How the Skill app (index.html) is built

The Skill app is generated from `skill-base.html` (the older single-look Skill app) by these scripts, run in order:

1. `ca50.py` – light theme, categories, gentler words, landing hero
2. `ff.py` – Fall Fair palette and fonts, blue ribbon, stars and coins, age and interest sign-up (uses `words.py` and `cssfix.py`)
3. `more.py` – landing sections, reviews, quick answers, colour fixes, tickets panel
4. `combine.py` – one app with two looks: 18 to 24 get the original dark Yofi, 25+ get Fall Fair; Skill save (`yofi.proto.v1`)
5. `simplify.py` – simpler Vote page, energy and loot boxes, coin swap for a Freeroll ticket (1 an hour), Freerolls in the tournament schedule, new-category bonus

The scripts use absolute paths from the session they were written in: update `d=` at the top of each before re-running. The output of step 5 (`yofi-simple.html`) is the Skill preview; for live, copy it to `index.html` with the title "Yofi - Skill".

## Real Money build

The horse-racing features (Podium Pick, the instant 1 v 1 Podium Pick, hourly races, heats, My stable) live in `racing.py` and are only for Real Money. `simplify.py` runs them when the build is started with `YOFI_BUILD=real`:

```bash
YOFI_BUILD=real python3 simplify.py
```

The Skill build (no `YOFI_BUILD`) leaves them out.

Then `realmoney.py` turns that output into Yofi - Real Money (`yofi-real.html`): its own saved data (`yofi.real.v1`), the "Real money" badge, mystery tournaments (a spin sets the winner's prize) and shared prizes on big spins. Copy `yofi-real.html` to `index.html` on the `real-money` branch.

```bash
python3 combine.py
```

```bash
YOFI_BUILD=real python3 simplify.py
```

```bash
python3 realmoney.py
```

Then `rmrace.py` adds the horse-racing game to `yofi-real.html`: 9-runner hourly race with bets ($1–$20, paid by stake), a perfect 1-2-3 jackpot, a free $1 bet for coin players (500 coins), qualification gates every 10 votes (pick 3 of 5, free with a $1 real version), and fewer voting pops.

```bash
python3 rmrace.py
```

Finally `rmshow.py` swaps racing and betting words for dog-show words (Best in Show, group judging, entries, rosettes, exhibitors, show catalogue, my show entries).

```bash
python3 rmshow.py
```

Then `rmv2.py`: Best in Show with 6 finalists (3 groups, top 2 go through) and big photos, only Pets / Nature & landscapes / Garden & flowers / Food shows (Food waits for sample photos), the group judging prize table, entering a photo costs 200 coins (first free), cash prizes for exhibitors, and the My show tab.

```bash
python3 rmv2.py
```

Then `rmv3.py`: shows whether you are a coin or real money player (account menu and My show) with a testing switch, a Friends pop to challenge friends (coins for coin players, real money for cash players), and friend challenges paid straight away with no club pot or blue ribbon.

```bash
python3 rmv3.py
```

Then `rmv4.py`: group judging is called Qualifiers ("Qualifiers · 3pm Pets"), the Lock in button is always active, and qualifier results no longer offer "Enter the Best in Show".

```bash
python3 rmv4.py
```

Then `rmv5.py`: a free qualifier for cash players too (with the $1 real upsell), and the owner of the 1st place photo in a qualifier gets 10% of its real entries.

```bash
python3 rmv5.py
```

Then `rmv6.py`: a creator earnings ledger (every qualifier win and Best in Show place, with photo, show, time and amount) on My show, in an earnings pop, and per photo.
Then `rmv7.py`: names. The 3-of-5 voting rounds are Qualifiers, the hourly 6-photo show is the Final (the knockout tournament keeps "Best in Show" for its last round), and My show is now Gallery.
Then `rmv8.py`: photo entries are free (3 photos in play, 3 qualifier tries each, an extra spot for every 20 votes, bank up to 3), and the free $1 Final entry costs 250 coins with a progress bar on the Vote screen for coin players.
Then `rmv9.py`: entering a photo costs 100 coins (first one free), and 250 coins buys a free $1 qualifier (pick 3 of 5, cash prizes), max 2 per hour. This replaces the free $1 Final entry.
Then `rmv10.py`: coin players asked to add a category photo see coin challenges, not the cash blue ribbon pot.
Then `rmv11.py`: no "Touch up a photo" row in the coins menu, and the coin challenge costs 100 coins (win 200).
Then `rmv12.py`: the agreed loop. Qualifiers are free-only (no paid fixed-payout version); photos enter free at 70+ (touch up with coins); 250 coins buys a free $1 Final pick, 2 an hour; the Final pool splits 78% top pickers, 10% finalists' creators, 12% Yofi; fixed $25 perfect bonus; coin players see coin games, depositors cash games; "Final pick" wording.
Then `rmv13.py`: design pass from the mock-ups: qualifier pick (Predict the top 3, prize chips, 1st/2nd/3rd slots), qualifier result (crowd's top 3 vs your picks with labels), Finalists card (big prize pool, countdown, Explore the finalists).
Then `rmv14.py`: newbie flow shows the core loop: when a photo reaches 70+, "Ready to compete!" enters it in the qualifiers (free) instead of offering a free first coin challenge.
Then `rmv15.py`: vote-first tutorial. Landing leads with "Start voting · free"; new players open on Vote; first qualifier after 5 votes (qualifiers no longer need a photo); first Final pick free; the first Final result offers "Get your own photo in a Final"; a player's first photo enters a qualifier free without needing 70+.
Then `rmv16.py`: "Next Finals" strip (time and category of the next 3 Finals) on the landing page, the end-of-tutorial card and Gallery; the first-photo pop names the Final it's going for; "Add a photo" opens the next Final's category.
Then `rmv17.py`: landing page category tiles are the Final categories (Pets, Nature & landscapes, Garden & flowers), each with its next Final time and prize pool, in time order.
Then `rmv18.py`: landing (no "Free to start"; Start voting / Enter with your own photo and win the prize / Watch the hourly Final live; next 6 Finals in a sideways row); no interest picker; category picker shows only Final categories; every upload is asked for a name; vote cards show photo names; first photo gets 150 coins and, once improved, goes straight into the next Final in its category; Final pick shows photo name, @username and 🔥 popularity; no real-money button for coin players on the pick screen.
Then `rmv19.py`: landing page redesign from the mock-up (headline, 1st/2nd/3rd podium, Earn a free pick, Enter your photo, Meet the contenders cards with prize pools and times, Watch the hourly Final).
Then `rmv20.py`: new-photo flow fixes: Enter your photo asks the Final category instead of guessing; name and first-photo prompts can show over the touch-up screen; the 150 coins are the sign-up welcome bonus (no double gift); first photo's status says "Touch up to go straight to the Final"; no Skill "first challenge free" pop for it; landing "How it works" (upload, improve to qualify, pick the top 3 of 6).
Then `rmv21.py`: landing page = the "PhotoPicks" mock-up (title, podium, Judge photos section, Your photo could win the Final with 3 coloured step cards, Enter your photo, Meet the contenders).

```bash
python3 rmv6.py
python3 rmv7.py
python3 rmv8.py
python3 rmv9.py
python3 rmv10.py
python3 rmv11.py
python3 rmv12.py
python3 rmv13.py
python3 rmv14.py
python3 rmv15.py
python3 rmv16.py
python3 rmv17.py
python3 rmv18.py
python3 rmv19.py
python3 rmv20.py
python3 rmv21.py
```

## Skill only

`freech.py` replaces the Freeroll with a free cash challenge (300 coins, once an hour: a quick 1 v 1 photo battle, free, that pays $1.60 real cash on a win). `simplify.py` runs it for Skill and skips it when `YOFI_BUILD=real`, so Real Money keeps its Freeroll.
