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

```bash
python3 rmv6.py
python3 rmv7.py
python3 rmv8.py
python3 rmv9.py
python3 rmv10.py
python3 rmv11.py
```

## Skill only

`freech.py` replaces the Freeroll with a free cash challenge (300 coins, once an hour: a quick 1 v 1 photo battle, free, that pays $1.60 real cash on a win). `simplify.py` runs it for Skill and skips it when `YOFI_BUILD=real`, so Real Money keeps its Freeroll.
