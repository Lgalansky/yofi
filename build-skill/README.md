# How the Skill app (index.html) is built

The Skill app is generated from `skill-base.html` (the older single-look Skill app) by these scripts, run in order:

1. `ca50.py` – light theme, categories, gentler words, landing hero
2. `ff.py` – Fall Fair palette and fonts, blue ribbon, stars and coins, age and interest sign-up (uses `words.py` and `cssfix.py`)
3. `more.py` – landing sections, reviews, quick answers, colour fixes, tickets panel
4. `combine.py` – one app with two looks: 18 to 24 get the original dark Yofi, 25+ get Fall Fair; Skill save (`yofi.proto.v1`)
5. `simplify.py` – simpler Vote page, energy and loot boxes, coin swap for a Freeroll ticket (1 an hour), Freerolls in the tournament schedule, new-category bonus

The scripts use absolute paths from the session they were written in: update `d=` at the top of each before re-running. The output of step 5 (`yofi-simple.html`) is the Skill preview; for live, copy it to `index.html` with the title "Yofi - Skill".
