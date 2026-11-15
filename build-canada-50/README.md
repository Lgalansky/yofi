# Canada 50+ build scripts

`index.html` on this branch is generated from the Skill preview (branch `main`) by running, in order:

1. `ca50.py`: light theme, categories, gentler words, landing hero
2. `ff.py`: Fall Fair palette and fonts, blue ribbon, stars, coins, age and interest sign-up, younger names for 25 to 34 (uses `words.py` and `cssfix.py`)
3. `more.py`: landing sections, reviews carousel, quick answers, colour fixes, tickets panel

The scripts use absolute paths from the session they were written in, so update `d=` at the top before rerunning. `landimg/` holds the landing photos (already inlined in `index.html`).
