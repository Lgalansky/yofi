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
Then `rmv22.py`: Real Money is branded PhotoPicks everywhere players see it (logo, page title, text, invite links); landing heading "Pick the winning photos. Win real cash."; smaller header logo so the header fits.
Then `rmv23.py`: PhotoPicks logo in a handwritten script (Pacifico), maroon, smaller, top left on the landing page and in the app header.
Then `rmv24.py`: "Enter your photo" / "Add a photo" / Gallery "Enter a new photo" first open a "Choose your Final" page (categories with next Final time and prize pool); tapping one opens the photo picker for that category.
Then `rmv25.py`: no free-pick bar on the Vote screen; coins menu row reads "Free Final pick" (no $1).
Then `rmv26.py`: qualifier "Coming up" item and pops say "Upcoming qualifier" (no time) with a ⚖️ scales icon.
Then `rmv27.py`: coins menu adds Quick Sprint (100 coins, win 160) next to Coin challenge and drops "Enter a photo"; a photo never goes straight into the Final: once the first photo improves it enters the qualifiers for its category's next Final.
Then `rmv28.py`: new players' judging has no qualifiers; Coming up shows "Free Final pick · in 15 votes" and the free pick opens after 15 votes; qualifiers start once it's used.
Then `rmv29.py`: "You've got N coins!" nudge offers the free Final pick first (250+ coins, pick left this hour); Quick Sprint idea has a photo.
Then `rmv30.py`: after every Final result (when you have no photo in play) an "Enter your own photo" card to qualify for an upcoming Final; Final picks cost $2 / $5 / $10 / $20 / $50, and the free pick is a free $2 pick.
Then `rmv31.py`: all Final prize money comes from the pool (no fixed $10/$5/$2; creators share 10% by place); the Final result shows the pool, what the top pickers shared, the creators' 10%, and how far you were from cash.
Then `rmv32.py`: Final picks pay by score, not rank: everyone on 15+ points shares the pickers' 78%, by pick size x score weight (15 pts x1, 20 pts x2, exact 1-2-3 x6), so about 40% of pickers win and a higher score always pays more; result screen shows each score group.
Then `rmv33.py`: landing photo step 3 is "Win a share of the prize" (creators share 10% of the pool); new "Pick the winners every hour" section with the live Final, pool, closing time and "Pick the Final · from $2".
Then `rmv34.py`: Final picks without points: 3 correct / 2 correct / 1 correct / all 3 in the top 3 in another order ("correct" = right photo, right place), weighted 10 / 2.5 / 1 / 1.2; the pick screen shows "pays about N×" for each, worked out from that Final.
Then `rmv35.py`: a guest's Final picks are kept through sign-up, and the free pick is placed straight after.
Then `rmv36.py`: "You have unused coins" pop opens the coins menu (Open my coins); new players' free ticket waits there as "Free ticket earned · Use" and opens the Final picker; the 250-coin nudge does the same.
Then `rmv37.py`: Final pick screen from the mock-up: "Win a share of $X · Cash prize pool" header, "Pick your 1st, 2nd & 3rd", pool reminder above a green button that reads "Choose your top 3" until 3 are picked.
Then `rmv38.py`: new players don't see Quick Sprint or the coin challenge until their first free Final pick is used.
Then `rmv39.py`: third new-player journey: landing "Pick the Final · from $2" opens the live Final's picker with cash amounts even for a guest; they choose, then sign up and add cash before paying; the pick is kept and "Your pick is in" shows after payment.
Then `rmv40.py`: live Final board highlights your picks (green row, medal on photo, "Your 1st pick"), bigger photos; no "Add a free $2" for players who haven't deposited.
Then `rmv41.py`: qualifier pick and result screens from the mock-ups (Pick the top 3, 3 exact / 2 exact prizes, medal slots; N of 3 matched, Finalist / Finished 2nd / Exact match tags, Through to the Final box, Pick the Final winner).
Then `rmv42.py`: while a Final pick is running, Coming up shows "Your pick is live" with your 1st pick's place and minutes to results (tap opens the live board), and judging shows a toast when one of your picks moves up.
Then `rmv43.py`: after a player's first Final pick, the Vote screen shows the last Final's creator earnings ("@luna_loves earned $37.92 with ...") and, if they have no photo in play, "Got a pet photo? The 1am Pets Final pays creators 10% of a $840 pool · Enter it" (✕ hides it for 20 votes).
Then `rmv44.py`: flow is judge -> pick -> create: the creator prompts come off the Vote screen; the Final result's "Enter your own photo" card now opens with the winning creator's earnings.
Then `rmv45.py`: qualifier groups use only the Final's own category; Final result screen from the mock-ups (headline, position chip, cash won, winner, crowd's top 3 vs your picks with Picked/Finished tags, rule, pool and winners stats, creators line, View payouts table, View next Final, Judge photos).
Then `rmv46.py`: qualifier result for returning players: coin players without a free pick see coin progress and Keep judging; with a free pick ready, "Use your free pick" for the live Final; depositors get "Pick the <live> Final · from $2"; "picks open at" time for the Final the qualifier feeds.
Then `rmv47.py`: suspense and hero moments: "Counting the votes…" with live bars, 3rd/2nd/1st revealed one by one with your pick for each ("✓ Spot on!"), skip; wins get a confetti hero screen ("+50 coins" / "You won $6.45") before the results.
Then `rmv48.py`: first-ever cash win gets a bigger one-off celebration; your own photo in a Final gets a reveal and a creator-earnings hero; near-miss chip on Final results; live Final board shows "If it ended now" winnings, a ticking countdown, ▲/▼ moves and a new-leader flash.
Then `rmv49.py`: the new-player flow ends when the first free pick's result is seen; until then no qualifiers, side games, 250-coin pick row or coin nudges (coins menu shows "Your free pick is live"); after it, the coins menu shows every option and a one-time "Unlocked" note points to the coins.
Then `rmv50.py`: coin players' qualifier result never offers the Final; with 250+ coins it says "You have enough for a free Final pick · it's in your coins" and the button is Keep judging.
Then `rmv51.py`: the results reveal ends on a "Continue →" button instead of jumping on automatically.
Then `rmv52.py`: one navy-blue style for every pop (navy headings, kickers, buttons, selected borders, links; light-blue chips; gold prize strips and medals; cash amounts green); qualifier pick matches the mock-up ("Your top 3 is ready", photo slots, "Judge photos").
Then `rmv53.py`: invite friends to judge: coins menu row and pop (WhatsApp / copy link, invite list Sent -> Joined -> +100); you get 100 coins when a friend judges 15 photos (friend starts with 50, up to 10 paid invites); "Friend bonus +100 coins" pop. Prototype simulates the friend joining and judging.
Then `rmv54.py`: qualifiers pay for every exact match (1 exact 10, 2 exact 25, 3 exact 50 coins); the result screen leads with "+10 coins · 195 → 205 coins", the photo comparison folds under "See the full result".
Then `rmv55.py`: green "play for real" upsells, picker first then deposit: free pick win shows "A $10 pick would have won $X" ($2/$5/$10 tiles, at most every 30 min) and a green button; free pick loss gets a quiet green outline button; Quick Sprint coin win says "Same game for real: $2 wins $3.20"; every real-money button is green.
Then `rmv56.py`: "2 in the top 3" (any order) now wins a small Final share; rule is "1+ in its exact spot, or 2+ in the top 3"; the reveal ends with the same summary and win amount as the result screen.
Then `rmv57.py`: qualifier pick screen from the mock-up: "Win up to 50 coins" with a big gold coin and three prize cards (50 / 25 / 10 coins for 3 / 2 / 1 exact matches).
Then `rmv58.py`: invite pop from the mock-up ("Earn 100 coins for every friend you invite", coin stack, "Earn up to 1,000 coins · 10 friends", icon steps, friends start with 50 coins, WhatsApp / Copy link buttons, invites list, rewards count).

Then `rmv59.py`: framing replaces touch-ups. Name and frame a photo (200 coins, first frame free) to enter its category qualifiers; framed photos race again free. Gallery rebuilt: upcoming Finals by category, the framed wall (gold frame, name plate, prize money, Finals, best finish, qualifiers, form), "Ready to frame" photos, earnings. Touch-ups tab hidden.

Then `rmv60.py`: the Final reveal matches the result screen (same stored player count and prize pool, same "X of your photos in the top 3 · Y in the exact spot" line, and a "Your picks" row with Exact / Finished / Outside top 3).

Then `rmv61.py`: Final result creator card from the mock-up ("Your photo could win real cash", winner card with photo and earnings, creators shared line, two steps, "Enter your photo — free").

Then `rmv62.py`: Gallery from the mock-up ("My gallery" hero with three tilted photos, Upcoming Finals rows with creators' share, How your photo wins, One frame callout, creator prize fold, Your photos, green Photo earnings box).

Then `rmv63.py`: qualifier reveal and result use the same words ("X of 3 in the exact spot", "Top 2 go through to the Xpm Final", what 1 exact spot pays); the repeated "See the full result" fold is removed.

Then `rmv64.py`: reveal podium reads 1st · 2nd · 3rd, lined up with Your picks; in qualifiers non-exact picks show a muted "✗ Finished 3rd" / "✗ Not in top 3".

Then `rmv65.py`: reveal podium labelled "The crowd’s top 3"; photos you picked carry a "Your 1st pick" tag (navy when in the exact spot).

Then `rmv66.py`: reveal end state from the mock-up (story headline such as "You picked the winner!", navy "YOU WON $X" box with gold amount, pool line, gold-ruled labels, "✓ Exact match" chips, gold border on matched photos).

Then `rmv67.py`: qualifier pick screen ignores taps for 900 ms after it opens (stray voting taps were picking a top 3) and opens scrolled to the top; coin icon redrawn as a minted coin with rim and star.

Then `rmv68.py`: reveal drops 1st, 2nd, then 3rd; the 50-coin prize card is no longer highlighted; qualifier result is a full page (Spot on! / Not this time, YOU WON box, crowd's top 3 with Finalist and your-pick tags, Your picks, Through to the Final, coins balance).

Then `rmv69.py`: run-through fixes. "Add cash" (green) replaces "Get more coins" and the shop copy talks about Finals; pops wait until nothing is open and 2.5 s after a close, and a due Final result goes before a waiting qualifier; the extra "Winner!" pop is gone (kept for the first cash win); PhotoPicks 18+ age screen with navy button; clearer free-pick line; "Form" label and legend on Final pick tiles.

Then `rmv70.py`: live pick page: ticket-style "Free pick confirmed" card with your 1st/2nd/3rd, big green prize pool and navy "Results in m:ss" countdown; results open from this page at 0 (they used to wait for the pop to close); stale "Results at" line removed.

Then `rmv71.py`: Final result no longer repeats the reveal (crowd's top 3, your picks and rule line removed; winner line hidden when the creator card shows the winner).

Then `rmv72.py`: the "Your photo could win real cash" card shows on every Final result (it hid once you had a photo racing); button says "Enter another photo" when you already have a framed photo.

Then `rmv73.py`: qualifier result drops the repeated crowd's top 3 and your picks and gains the "Your photo could win real cash" card (Enter your photo → Choose your Final); qualifier pick screen loses the 1st/2nd/3rd slot row.

Then `rmv74.py`: photo card message is "Qualify for the Final" + "Earn a share of 10%" (the top-2 qualifier step is not the headline because it pays nothing).

Then `rmv75.py`: qualifier result trimmed to headline + photo card + Keep voting (exact-spot line, YOU WON box, coin line, Through to the Final and the free-pick note removed; the reveal already shows what was won).

Then `rmv76.py`: review fixes part 1: invite headline no longer clipped (single coin), no 'undefined' in earnings or account, unsolicited pops kept 90 s apart and daily rewards wait until the new-player journey ends.

Then `rmv77.py`: the Tournaments tab becomes a Finals tab (live Final with pool, countdown, finalists, green cash pick and navy free pick; coming-up Finals by category; your picks; recent results; how Finals work). Gallery tab title fixed (was 'Friends').

Then `rmv78.py`: landing clean-up: navy free buttons and green 'Pick the Final · from $2'; navy headings and links; 'From camera roll to cash' removed; realistic recent picker wins; testimonials and FAQ rewritten for Finals, picks and framing.

Then `rmv79.py`: align screens: voting uses only Final-category photos and names the category; coins menu drops the score-based Coin challenge; Finalists page uses the framing message; account shows Prize money and Framed photos, Finals button, no Coin store.

Then `rmv80.py`: payouts rebalanced: win with 2 photos in the top 3, at least 1 in its exact spot (~46% of pickers); 3 correct ~5x, 2 correct ~2x, 1 correct + another in the top 3 at least 1.1x (floor); rule text, payout table, near-miss chip and loss reveal updated.

Then `rmv81.py`: new-player fixes 1-4: cash pick lands ~1.6 s after paying with a toast, green 'Add $10' deposit; touch-up screen never shows and a new photo goes straight to one name+frame step; shared celebration pops in navy with no scores; 'Free pick unlocked!' opens the pick screen directly.

Then `rmv82.py`: new-player improvements 5-9: upload success pop (save photo / vote to watch it race); lucky boxes replaced by fixed streak rewards (+20/+40/+80); free pick after 10 votes with other counters hidden for new players; sign-up names the pick; first-pick guarantee (one more free pick in the next Final if the first loses).

Then `rmv83.py`: new player's first Final result pushes photo entry: 'Your turn: add a photo' card moves up under the result with the next Final and pool; cash upsell held back on that screen; guarantee pick stays on top on a loss; confetti null guard.

Then `rmv84.py`: free pick opens the live page at once (was ~9 s waiting for the pick screen to close); live status explains the rule from your picks (in top 3, exact, what is still needed) and each highlighted row shows where that pick needs to finish.

Then `rmv85.py`: streak boxes return as a fixed-value reveal: Bronze 20 / Silver 40 / Gold 80 for 3 / 6 / 10 right in a row, prize shown before opening, tap to open with shake and burst; new players get the coin burst only.

Then `rmv86.py`: streak bar names the boxes ('2 in a row · 1 more for a Bronze box') with bronze/silver/gold markers and shows for new players too; photo names on voting cards readable (white on navy).

Then `rmv87.py`: free pick unlock goes through a guided coins menu: 'Open my coins' → intro line on what coins are for, Free pick row first with gold highlight and pulse, others dimmed → tap → pick screen.

Then `rmv88.py`: results reveal scrolls on shorter screens (card no longer clips its content) and Continue stays pinned to the bottom.

Then `rmv89.py`: touch-up card removed from the Vote screen; Gallery tab always renders the new Gallery (no old 'photo challenges'); framing is a big reveal (photo fades in, thick gold frame closes round it, brass plaque with name, category and date slides up, shine and confetti, 'See your photo framed').

Then `rmv90.py`: first-pick guarantee removed; on every Final result the 'Your photo could win real cash' card sits straight under the result, with the prize split (pool, players who won, payouts) below it.

Then `rmv91.py`: Gallery becomes a creator page once you have a framed photo: record strip, each framed photo (gold frame + plaque) with record and live status (qualifier tries, next qualifier in N votes, its Final, Vote to move it along / Watch / Enter again), ready to frame, earnings, compact Add another photo, upcoming Finals, prize-share fold. No framed photo: intro page as before.

Then `rmv92.py`: games rotate after the first Final (qualifier, then Quick Sprint, every 10 votes; strip names the next one; old Sprint nudge and the score-based coin battle switched off); streak boxes pay coins with a burst, no pop; no toasts per qualifier try or 'in the ring now' for your photo.

Then `rmv93.py`: uploading never shows the old improve flow: short 'Preparing your photo…' then straight to the Gallery and Frame your photo (old score result / touch-up screen skipped); coin nudges never open over an upload or any open screen; sign-up text has no photo scores.

Then `rmv94.py`: three-game rotation every 15 votes (qualifier → Quick Sprint → free Final pick), unaffordable games skipped, never two qualifiers in a row (short of coins: qualifier alternates with a quiet slot); strip names the next game or shows progress to a free pick.

Then `rmv95.py`: every new player gets the free-pick journey once: framing a photo or placing a paid pick no longer ends it; it ends with the first free-pick result.

Then `rmv96.py`: Quick Sprint costs 25 coins and wins 40 (was 100/160) so it appears in the rotation for low-coin players; rotation slot 3 is the 'You have unused coins' pop leading to the guided coins menu with the free Final pick highlighted.

Then `rmv97.py`: the live Final is a race: six lanes with finalists' photos running to a chequered finish line as votes come in, your picks ringed gold/silver/bronze, current place on each runner, commentary line (lead changes, your picks climbing or dropping), photo-finish pulse in the last 20 seconds; replaces the standings list.

Then `rmv98.py`: 'Call the crowd' voting: after each vote both photos fill to the crowd's share with big percentages, and a banner lands ('You called it! +5 coins · 2 in a row' in green, or 'The crowd went the other way' in navy with a shake); streak line updates at once; old chips hidden; old 'Invite a friend… blue ribbons' pop off.

Then `rmv99.py`: the pick-3-of-5 coin game is renamed Coin Pick (chip, strip, reveal, result, win label); Call the crowd shows percentages only, no shading or fading on the photos; 'The crowd went the other way' without the ✕.

Then `rmv100.py`: back to 'Qualifier' for the coin game (Qualifier · Round 1 of 3); Call the crowd shows no percentages on the photo tiles, the banner carries the result ('62% agreed · +5 coins · 2 in a row').

Then `rmv101.py`: coin game named Coin Pick again (strip, round chip, reveal, result, win label); photo side keeps 'qualifiers'; vote tiles stay clean.

Then `rmv102.py`: vote reveal: big percentages back on both photo tiles (no shading); the called-it / other-way banner removed.

Then `rmv103.py`: vote reveal climbing fill back: each photo fills from the bottom to its crowd share (green for the crowd's pick, navy for the other) under the big percentage; no banner.

Then `rmv104.py`: winning effect on every vote you call right: pulsing gold glow and sparkle burst on your photo, coin burst (+5) flying from the photo to the balance, and a streak chip on 2+ in a row; misses stay quiet.

Then `rmv105.py`: Coming-up strip reads 'Coin Pick · pick 3 of 5 · free' with no category name.

Then `rmv106.py`: Coin Pick screen drops the 'Win up to · 50 coins' headline; the prize cards show what you can win.

Then `rmv107.py`: your photo's journey: track Framed → Qualifiers (3 tries with places) → Finalist → Final → Paid with the framed thumbnail on its stage; slim row under the streak bar on the Vote screen with a bar filling to the next qualifier; moving-forward moment (glow, sparkle, '3rd in its qualifier · 1 try left' / 'Through to the Final!'); full track on Gallery cards; your own photo's lane marked in the live race.

Then `rmv108.py`: Coming-up strip while a pick is live just says 'Your pick is live' (results-in button stays).

Then `rmv109.py`: Final result: prize pool, players who won cash and View payouts sit straight under the result; the 'Your photo could win real cash' card follows.

Then `rmv110.py`: 'Your photo could win real cash' card after every quick game: added to Quick Sprint results (Coin Pick and Final results already had it); Sprint result pop scrolls when taller than the screen.

Then `rmv111.py`: Coming-up strip no longer shows your photo (next qualifier / in the ring); the journey card under the streak bar covers it; strip shows the next game or your live pick.

Then `rmv112.py`: coins menu shows coin games to every player incl. after a deposit (Free Final pick, new Coin Pick row, Quick Sprint); unused-coins pop fires when the balance crosses 250 and at session start after the 3rd vote if 250+, max once per 15 votes, old milestone nudge off.

Then `rmv113.py`: 'Pick the winner' pool next to the Top 3: Top 3 | Winner tabs on the pick screen, live odds and share of winner picks on each photo, cash from $2 or free pick (250 coins), confirmation with pool, countdown and race, reveal and payout at closing odds.

Then `rmv114.py`: winner pick can always be placed: every player gets the stake row and green 'Pick to win' cash button, plus the free-pick button when they have 250 coins (otherwise a line says how many more coins).

Then `rmv115.py`: coins can't be used on Final pick screens: Top 3 and Winner are cash-only when opened normally; the free ticket comes only from the coins menu's Free Final pick row (or a new player's ticket) and shows 'Use your free ticket'; Finals tab free-pick button removed.

Then `rmv116.py`: one new-player journey: landing's main button is 'Start playing' (judge → free pick → result → add your photo); photo section's big button becomes a small 'Got a photo? Enter it now' link; green cash pick stays.

Then `rmv117.py`: all your picks on one race: lanes show every tag (Your 1st pick · Your winner · Your photo); 'Your picks in this Final' panel under the race updates live (Top 3 status/estimate, Winner odds/position, your photo's position); add-the-other-pick button when you have only one.

Then `rmv118.py`: Finals named by category with no clock time ('The Pets Final'); times only as countdowns; upcoming Finals show 'Starts when 6 finalists are in · 3 of 6 in'; no 'every hour' / 'hourly' copy; coin players get one free pick per Final (Top 3 or Winner). Simulated: Finals still run on the hourly timer behind the scenes.

Then `rmv119.py`: 'View next Final' opens an Up next card (finalists in x of 6, pool so far, vote / enter your photo) instead of reopening the finished race; results interrupt any open pop as soon as a Final ends (blocked only mid-pick, mid-upload or during a reveal); landing 'Enter your photo' opens the app Gallery before the photo picker.

Then `rmv120.py`: Photo picker always opens over your Gallery: pickPhoto moves you to the Gallery (closing pops and the Finals tab) from any entry point first. Finals 'How Finals work' no longer says 'Every hour'.

Then `rmv121.py`: No screen jump when the photo picker opens: Choose your Final stays up with the chosen category highlighted ('Choose your photo…'); the screen changes only once a photo is chosen. Brand-new players from the landing page answer the age question before the list appears.

Then `rmv122.py`: Version number on the account page ('PhotoPicks v122' under Reset prototype); taken from the newest rmvN.py, so it moves on with every step.

Then `rmv123.py`: Fix live pick page flashing back to voting: an interrupted result reveal no longer leaves the Final stuck half-way (which made the 1-second result check close every pop); interrupted results replay, stale marks cleared on load.

Then `rmv124.py`: Pick screens keep their scroll position when you tap a photo or stake (Top 3 and Winner). Bigger pick medals on a white disc; bigger Form chips; popularity % moved onto the photo as a chip like the Winner odds.

Then `rmv125.py`: Pick medals without the white disc (it covered the photo); big size kept with a drop shadow.

Then `rmv126.py`: County-fair prize rosettes for picks (gold/silver/bronze, gold star for Winner) in the photo's top-left corner, coloured border and 'Your 1st pick' strip, others fade once 3 are picked; chips off the photos (🔥% on the handle line, odds next to the name); pin bounce + sparkle, bigger burst on the 3rd pick; glide to the pick button which shows what a full win pays; same rosettes on live race lanes, race card, live ticket and picks panel.

Then `rmv127.py`: Picks get navy ticket tags ('My pick 1st'), rosettes are earned only in the result reveal when a pick lands in its exact spot (pinned onto the podium photo with a burst). No badges on race avatars; small 'Pick 1st' tags on the live ticket and picks panel, one pick per line.

Then `rmv128.py`: Rosettes for your own photos: navy Finalist rosette when a photo qualifies, gold/silver/bronze when it finishes top 3 in a Final; pinned onto the photo in the result pop, hung on its frame in the Gallery with a plaque record ('2 gold · 1 finalist').

Then `rmv129.py`: Slim one-line streak strip (flame count, track with three drawn chests, '1 more → Bronze box'; next chest wiggles when one away). Hitting a box plays a drawn chest opening over the photos with light rays and coins flying to the balance; fixed values kept (Bronze 20, Silver 40, Gold 80). Renamed to chestBurst so it never triggers the old random 'Big chest' pop.

Then `rmv130.py`: Pick result reveal: one signal per fact. Rosettes removed from picks (place label + 'Your 2nd pick' + gold border on the podium; 'Exact match' once, under Your picks). Rosettes stay for your own photos only.

Then `rmv131.py`: Result bugs: one reveal settles Top 3 + Winner picks on the same Final (total won with a line per pick; Winner pick waits for the Top 3 result so the result page isn't closed). Coin Pick page after the reveal no longer repeats 'Spot on!' ('+10 coins in your balance'). 'of your photos in the top 3' → 'of your picks'. Final result page states the Winner pick outcome.

Then `rmv132.py`: Winner odds locked when you pick: pick screen 'pays $X if it wins · 🔒 Odds locked when you pick', live page and picks panel 'locked at N× · pays $X', settlement uses the locked odds (fallback to closing odds for older picks); rules line updated.

Then `rmv133.py`: Every screen stays inside one category: Garden & flowers parked as 'coming soon' (no garden photos in the library), Nature & landscapes without the tiger, Finals never fill from other categories, voting pairs share one category and its label, Coin Pick uses 5 photos from the category with the crowd deciding the order (no 'top 2 reach the Final'); copy and entry checks list live categories.

Then `rmv134.py`: Quick Sprint pairs: both photos from the same live category; crowd share follows hidden photo appeal plus noise (stronger photo wins ~72%), replacing the 50/50 coin flip; nothing from the Finals feeds Sprint results.

Then `rmv135.py`: Photo Derby: 4-rider skill race on the same 10 photo pairs; coins or $1/$2/$5/$10 entry, 15% fee shown, 1st 70% / 2nd 30% of the pool; lobby, live horses, results with Rematch / Step up. Opponents simulated. Card on the Finals tab and in the coins menu.

Then `rmv136.py`: Three more skill games on the Derby engine: Match Race (1v1, win 1.7×), Grand National (50 riders, 1st 15× / 2nd 8× / 3rd 5.5× / 4th–10th 2×), Hot Streak (4 players, one wrong ends your run, longest run wins, opponents' streaks shown as targets). Coins or $1–$10, 15% fee shown, Rematch / Step up / Other games. Games row on the Finals tab, 'Photo games' in the coins menu. Opponents simulated.

Then `rmv137.py`: Stage 1 of 'your photos earn money': Final picks (cash and coins), Winner odds, free Final pick ticket, the free-pick newbie journey, Coin Pick, Quick Sprint, game rotation and unused-coins pop removed from reach (entry points lead to Photo games). New players: 10 votes → free coin Match Race. Finals tab → Play (Photo games + live Final to watch/vote). Framing free. Landing, coins menu, Add cash, FAQ reworded; example stories labelled as prototype.

Then `rmv138.py`: Stage 2 real-play funnel: coin players see coin games only plus 'Your first real game is on us' (free $1 Match Race, switches to real play for good); real players see $0.50–$10 only; Bonus Cash spent first, then $1 tickets, then cash; 'Add $5, get $10 Bonus Cash' after the first real game and on the add-cash screen; out-of-money screen; coins buy a free $1 ticket (500, 1 a day); simulated winners feed; green real-money buttons.

Then `rmv139.py`: Newbie run-through fixes: no age form on arrival (asked once, right before anything with cash); Fall Fair look when no age given; free real game account screen 'Your free $1 game is waiting · real-cash games are for adults 18+'; real-only switches on at the first deposit (non-depositors keep coin games, results offer 'Add cash to play again'); coin players' header shows coins and streak only.

Then `rmv140.py`: Stage 3: photo moment after the first game (upload, or try a starter photo · coins only), 'Collecting its first votes…' then an instant verdict (68% picked it · better than 7 in 10), every vote you cast adds a view to your photos, Gallery → My Photos with views/verdict per photo, 7-day reward calendar, notifications opt-in after the first win, frame screen wording updated.

Then `rmv141.py`: Stage 4: Play Pool (photos picked by 60%+ at their verdict), simulated royalties 0.7¢ per play to the cash balance (starter photos 1 coin), earnings card on My Photos (this week, plays, Play Pool count, top earner, how it works), per-photo plays and earnings, 'While you were away' pop with plays and earnings, every 5th vote is a live Final pair tagged 'your vote counts'.

Then `rmv142.py`: Stage 5 daily photo contests (no sponsors): per live category, a free daily (guaranteed $10/$6/$4) and a $2 cash daily (85% of entries, top 10% paid, stepped prizes that add up to the pool), closing at midnight. Pick your photo, enter; live position on My Photos; result with cash prize and a rosette for top 3. Cards on My Photos and Play, 'Enter today's contest' on a verdict. Entrants/rankings simulated; demo results 10 min after entering.

Then `rmv143.py`: Hidden fair matching: daily contests split into groups of similar-strength photos (under 60% / 60–70% / 70%+) — entries, prizes and position are for your group; one line tells the player they're matched with photos like theirs. Free daily $6/$4/$2 per group. New ⚡ Quick contest: 10 photos, $1, top 3 paid $4/$2.50/$2, result within the hour (demo ~5 min). Better-mixed random draws for entry results.

Then `rmv144.py`: First-session pacing: first game matched with newer (weaker simulated) players; free real game offer waits until after the photo verdict (or a skipped photo moment) and arrives as its own 'Now race for real cash' moment; starter photo auto-framed (3 screens to the verdict); daily reward only in the first 90 s of a later session; Play tab shows games only.

Then `rmv145.py`: Four of the owner's own photos added to the library: Pets 'Morning run' (Labrador on the dunes); Nature 'Golden cliff', 'Sea of flowers', 'Desert pause'. Cropped to 3:4 portrait. Pets now 7 photos, Nature 11.

Then `rmv146.py`: Newbie fixes: cash winnings ($0.50+) unlock real games without a deposit; starter photo scores 72%, joins the Play Pool and shows first plays within a minute; first-ever game against a newcomer (simulated 32%); earnings card shows how to start earning instead of zeros, and coins earned for a starter-only pool.

Then `rmv147.py`: Creative-director fun pass: race countdown 3·2·1·GO, live race caller (lead changes, neck and neck, final stretch), bigger horses, PHOTO FINISH flash before results; verdict % counts up with a meter marking the 60% Play Pool line, then the result and confetti; My Photos drops zero boxes (Fresh entry only for photos with no plays) and shows views/plays/earnings in a side panel with a live dot; Play cards show live player counts (simulated).

Then `rmv148.py`: Voting fun pass: hot-streak glow on the vote tiles at 3/5/10 in a row with banners (On fire! / Hot streak! / Crowd whisperer!); 🔮 Crowd Call bonus pair about every 20 votes (3× coins if right, nothing lost if wrong; never on a live-Final pair); race caller adds 'First past the post!' / 'Pipped at the post!'.

Then `rmv149.py`: Voting in rounds of 10: round bar (score, dots), stakes on about 1 in 3 pairs ('Today's Pets contest · fighting for 4th place'), your photo's strip with score and the 60% Play Pool line; end-of-round card with score, dots, 'you beat X% of voters', coins (100/60/40/25/10), rounds-in-a-row, what your votes did and your photo's move (can cross into the Play Pool); Next round / Race with this eye / Check on your photo; first round leads to the free first Match Race. Race clock fixed during the countdown.

Then `rmv150.py`: Judge 3 rounds to earn your photo entry: round bar shows 'Round 2 of 3 · earn your photo entry'; every 3rd round 'You qualified!' with an entry ticket and 'Enter your photo · free' as the main button; free daily needs a ticket ('🔒 Judge'), Quick contest takes a ticket instead of $1, cash $2 entries need none; contest screen shows tickets or rounds to go.

Then `rmv151.py`: Calmer voting: streak meter, streak chests and On-fire banners removed; rounds of 6 pairs (an entry costs 18 votes, not 30); round bar shows '🎟️ 2 rounds to your next photo entry' with 3 progress pips and '1 ready to use' when a ticket waits; bar repaints after each round.

Then `rmv152.py`: The photo loop: newbies start by entering a photo; each photo plays a 15 head-to-head qualifier (8 wins = finalist, 8 losses = out) that advances as you judge, shown live under the pair; finalists get a rosette + 50 coins and 'Race it in a Final · $1' (cash only); 6-photo live race with photo finish, 1st $3.50 / 2nd $1.60, top-3 rosettes; first entry free, then judge 3 rounds per entry; My Photos shows photos in play and tickets; Play Pool, royalties, contest cards and newbie Match Race offers removed from the path.

Then `rmv153.py`: Per-photo progress viewer at the top of voting: 'Your photos in play' with stage tracker (Qualifier › Final › Prize), wins bar to 8 with finish flag, won/lost counts, wins to go and losses to spare, last matchup, coins won per photo (+5 per win, +50 for qualifying), finalist Race $1 button, raced place and cash won; compact rows when 2+ photos.

Then `rmv154.py`: watch your photo's qualifier matches live at the top of the Vote screen (7-vote matches, countdown, verdict).

Then `rmv155.py`: the Final is a $2 one-on-one duel (winner takes $3.40), watched live on the Vote screen, with win streaks.

Then `rmv156.py`: free coin predictions on other players' live duels (+20 coins if right; cash stays with photo owners).

Then `rmv157.py`: My Photos rebuilt as photo hero cards (rosette on the frame, one next-step button, last duel); old 6-photo Final leftovers removed.

Then `rmv158.py`: the qualifier is 15 crowd votes (win 8), shown vote by vote; rounds 1-2 end with a banner, only the ticket round opens a popup.

Then `rmv159.py`: live duels shown inside judging (every 5th pair is a live $2 duel); prediction card removed; finished photos leave the panel.

Then `rmv160.py`: the 6-photo race Final is back ($1, 1st $3.50, 2nd $1.60); duel retired; wording restored everywhere.

Then `rmv161.py`: live-Final banner above the pair removed.

Then `rmv162.py`: simple loop: 100-coin photo entries, swipeable photo cards on the Vote screen, your votes move your photo to the Final, full-screen rivals + $2/$5/$10/$20 entry + race.

Then `rmv163.py`: watch your photo qualify full screen: at 7 wins the deciding votes play out live, then Qualified! with rosette.

Then `rmv164.py`: full-screen start line when a photo enters its qualifier (Sterling is in!).

Then `rmv165.py`: no 100-coin pop; free retry when a photo goes out; first two entries strongly favoured to qualify.

Then `rmv166.py`: loop for photos that miss: free tune-up, training head-to-heads for coins and form, then free re-entry.

Then `rmv167.py`: accuracy counter removed from the Vote screen; round bar shows only coins to the next photo entry.

Then `rmv168.py`: Play tab becomes your Stable: train photos head-to-head for coins and form, cash head-to-heads ($2/$5) for qualified photos, Finals and re-entry from each horse's card.

Then `rmv169.py`: old qualifier popups switched off; big rival photos; coin countdown removed from the Vote screen.

Then `rmv170.py`: free photo entries (5 a day, several at once); training costs 20 coins a match, 3 wins before 3 losses = cash-ready for good (Finals + cash head-to-heads).

Then `rmv171.py`: your 10 votes start a photo's qualifier; the qualifier is a full-screen live 2-horse race (first to 11 votes).

Then `rmv172.py`: 3 correct votes in a row move your photo 1 step (3 steps to the qualifier, 3 more to the Final); 3-2-1 head-to-head intro before the qualifier race.

Then `rmv173.py`: on 2 in a row the third streak dot pulses with '1 more for a step!'.

Then `rmv174.py`: 2 correct in a row moves a photo a step; votes move one photo at a time (the card you're on); cash and coin balances always shown.

Then `rmv175.py`: when no photo is in play, the Vote screen shows an empty-lane card promoting a free photo entry (or the stable).

Then `rmv176.py`: sign-up after the first framed photo; slower qualifier race with each voter shown; prize up front on the race and rivals screens.

Then `rmv177.py`: Qualified! screen shows the Final and what 1st could win.

Then `rmv178.py`: coins sheet is now Train for Cash Races (your photos with training progress); training costs 50 coins a match.

Then `rmv179.py`: "cash-ready (for good)" renamed to "Ready for Cash Races" everywhere.

Then `rmv180.py`: encourage 2 photos: entry tip, 'Add a second photo' on the start line, +25 coins for two in play, Name it on auto-named photos; start line matches the streak rule.

Then `rmv181.py`: navy & gold redesign of the live qualifier (Race to 11), You're in the final!, and the Final lobby, from the owner's mock-ups.

Then `rmv182.py`: every race has a goal, 3-2-1, suspense and a celebration: stable head-to-heads rebuilt as navy Race to 8; 3-2-1 before the 6-photo Final.

Then `rmv183.py`: head-to-head in the owner's mock-up style: story headlines (One vote from victory), Winner takes, 15-vote counting bar, You won + net win, New challenge.

Then `rmv184.py`: the 3-2-1 before every race rebuilt: Get ready, prize in gold, big photos with VS, gold countdown ring, green GO!.

Then `rmv185.py`: the Stable in the owner's mock-up style: hero cards for photos unlocked for cash races, training cards with Wins/Losses, Add a photo.

Then `rmv186.py`: Train for Cash Races sheet in the owner's navy mock-up style.

Then `rmv187.py`: finalist cards no longer get stuck at Step 3 of 3: they show Into the Final! with Meet your finalists & race.

Then `rmv188.py`: qualifier is a real 2-horse race on a track; full-screen 3-2-1; clearer step label.

Then `rmv189.py`: first Final free ($2 entry); vote pairs match your qualifying photo's category; daily-rewards pop held until first qualifier; finalist card says Your Final is waiting.

Then `rmv190.py`: winning the qualifier sends you back to voting; 3 voting-streak steps take the photo to its Final.

Then `rmv191.py`: free first Final switched off; all Final entries paid.

Then `rmv192.py`: My Photos rebuilt as your trophy wall: earnings banner, framed photos with rosettes, record row, one current status line per photo.

Then `rmv193.py`: 300 coins = a free $2 Final entry (lobby button + coins sheet).

Then `rmv194.py`: one-tap rematch on results: Race again, Step up, and Race again free with 300 coins; Step up on head-to-heads.

Then `rmv195.py`: challenges while you're away: other players challenge your race-ready photos; While you were away card, Stable Challenges box, Play tab count.

Then `rmv196.py`: lost qualifier loop: near-miss coins, free rematch on a timer, train now to skip the wait; free Final entry 250 coins; challenges only after first cash race.

Then `rmv197.py`: consistency pass: all full-screen moments share one navy and one gold wordmark; one green / navy / gold button system; stray blues removed.

Then `rmv198.py`: head-to-head entries of $2/$5/$10/$20 with step-up through each level.

Then `rmv199.py`: every extra photo you pick gets its own name-and-frame step before it joins the race.

Then `rmv200.py`: pinned main buttons on all navy screens; old coins popup, 3-in-a-row toast and prize-pool figure removed; landing page rewritten to the real loop.

Then `rmv201.py`: coin entry is one per player (account required); Bonus Cash spent first, kept separate, shown beside cash.

Then `rmv202.py`: honest money lines (lobby pool/prizes/fee, net result, head-to-head fee); simpler Stable cards; Form hidden; one rosette rule.

Then `rmv203.py`: one Welcome back screen on return (rematch, Final, challenges, daily reward); reopen on Vote; My Photos banner and rematch status fixed.

Then `rmv204.py`: Your cash sheet with withdrawal (min $10, bank or PayPal, demo only); Bonus Cash shown as not withdrawable.

Then `rmv205.py`: the + on the cash balance opens the Your cash sheet.

Then `rmv206.py`: rmv206: Daily Cup. 100 coins enters one race-ready photo into a daily $100 fixed prize pot (top of the Stable).

Then `rmv207.py`: rmv207: Tell me when it's ready (rematch and Daily Cup) and sign-up titles that match the moment.

Then `rmv208.py`: rmv208: cash entries with too little cash open Add cash, not the coins pop.

Then `rmv209.py`: rmv209: navy Add cash sheet that names the entry, sizes the offer to cover it and enters straight after paying.

Then `rmv210.py`: rmv210: clear path after a missed qualifier (free rematch or train for 50 coins, straight into the match).

Then `rmv211.py`: rmv211: one-tap Train again with wins and coins left.

Then `rmv212.py`: rmv212: Ready for Cash Races celebration after the third training win.

Then `rmv213.py`: rmv213: tap-through audit fixes (Final buttons say Vote N steps, photos return to voting after a Final, no instant Final replays, low-coin training, invite sheet, picker wording, one Add cash sheet).

Then `rmv214.py`: rmv214: route cards (steps > qualifier race > steps > Final), stacked Stable buttons, head-to-heads as live horse races.

Then `rmv215.py`: rmv215: age group asked at sign-up (and once on open for older accounts), not before the Final.

Then `rmv216.py`: rmv216: one Final per run; Race it again from the qualifier (free); head-to-heads stay open.

Then `rmv217.py`: rmv217: simpler Vote cards (name, route, one goal line) and a short button-led coins sheet.

Then `rmv218.py`: rmv218: coins sheet buttons show the coin cost, right aligned.

Then `rmv219.py`: rmv219: Vote card shows Steps n/3 and Streak n/2 with feedback on every vote.

Then `rmv220.py`: rmv220: fun pass (visible vote verdict + coin float, sounds and haptics with mute, race emoji, playable landing guess, winners ticker).

Then `rmv221.py`: rmv221: vote reveal starts at 50/50 and slides to the real split.

Then `rmv222.py`: rmv222: landing page from the mock-up (crowd-favourite guess, navy Live races card, vote link), copy corrected.

Then `rmv223.py`: rmv223: train-only way back after a missed qualifier, training as replays of earned votes, shorter races (7 and 5), horse ladder to cash challenges in Play.

Then `rmv224.py`: rmv224: first Final free with one button; Final result goes to the stable; ladder shows the Final; 250-coin entry retired.

Then `rmv225.py`: rmv225: one required sign-up right after framing; no walls later.

Then `rmv226.py`: rmv226: navy & gold sign-up showing the framed photo.

Then `rmv227.py`: rmv227: no coin bonus at sign-up.

Then `rmv228.py`: rmv228: Play for Real welcome popup at the Final (deposit $10 get $5), Welcome back with big streak, navy training screen, no tune-up, Cup teaser, simpler Stable card.

Then `rmv229.py`: rmv229: first Final is free only; welcome offer moves to the next Final.

Then `rmv230.py`: rmv230: 2-option head-to-head result, navy qualifier start screen, simpler Daily Cup tile, Done/Now/Still-to-do progress.

Then `rmv231.py`: rmv231: two actions per Stable card and qualifier screen.

Then `rmv232.py`: rmv232: So close with low coins offers Enter another photo as the second option.

Then `rmv233.py`: rmv233: button colour rule (green = real money, gold = coins, navy/cream = free).

Then `rmv234.py`: rmv234: free buttons pick navy or cream from the colour behind them.

Then `rmv235.py`: Survivor coin game ($100 house prize), Coin games toggle in Play, one yellow coin icon everywhere.

Then `rmv236.py`: Survivor polish: coin icon sizing, Coin games heading, Survivor on the coins sheet.

Then `rmv237.py`: Simple Ready for Cash Races popup (one button to the stable); stable card shows Trained, buttons under Now, challenge as the green button.

Then `rmv238.py`: Stable card: 5-stop progression track (Framed, Qualifier, Training, Cash games, Final) + Real games / Coin games buttons; Real games sheet.

Then `rmv224.py`: rmv224: first Final free with one button; Final result goes to the stable; ladder shows the Final; 250-coin entry retired.

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
python3 rmv22.py
python3 rmv23.py
python3 rmv24.py
python3 rmv25.py
python3 rmv26.py
python3 rmv27.py
python3 rmv28.py
python3 rmv29.py
python3 rmv30.py
python3 rmv31.py
python3 rmv32.py
python3 rmv33.py
python3 rmv34.py
python3 rmv35.py
python3 rmv36.py
python3 rmv37.py
python3 rmv38.py
python3 rmv39.py
python3 rmv40.py
python3 rmv41.py
python3 rmv42.py
python3 rmv43.py
python3 rmv44.py
python3 rmv45.py
python3 rmv46.py
python3 rmv47.py
python3 rmv48.py
python3 rmv49.py
python3 rmv50.py
python3 rmv51.py
python3 rmv52.py
python3 rmv53.py
python3 rmv54.py
python3 rmv55.py
python3 rmv56.py
python3 rmv57.py
python3 rmv58.py
python3 rmv59.py
python3 rmv60.py
python3 rmv61.py
python3 rmv62.py
python3 rmv63.py
python3 rmv64.py
python3 rmv65.py
python3 rmv66.py
python3 rmv67.py
python3 rmv68.py
python3 rmv69.py
python3 rmv70.py
python3 rmv71.py
python3 rmv72.py
python3 rmv73.py
python3 rmv74.py
python3 rmv75.py
python3 rmv76.py
python3 rmv77.py
python3 rmv78.py
python3 rmv79.py
python3 rmv80.py
python3 rmv81.py
python3 rmv82.py
python3 rmv83.py
python3 rmv84.py
python3 rmv85.py
python3 rmv86.py
python3 rmv87.py
python3 rmv88.py
python3 rmv89.py
python3 rmv90.py
python3 rmv91.py
python3 rmv92.py
python3 rmv93.py
python3 rmv94.py
python3 rmv95.py
python3 rmv96.py
python3 rmv97.py
python3 rmv98.py
python3 rmv99.py
python3 rmv100.py
python3 rmv101.py
python3 rmv102.py
python3 rmv103.py
python3 rmv104.py
python3 rmv105.py
python3 rmv106.py
python3 rmv107.py
python3 rmv108.py
python3 rmv109.py
python3 rmv110.py
python3 rmv111.py
python3 rmv112.py
python3 rmv113.py
python3 rmv114.py
python3 rmv115.py
python3 rmv116.py
python3 rmv117.py
python3 rmv118.py
python3 rmv119.py
python3 rmv120.py
python3 rmv121.py
python3 rmv122.py
python3 rmv123.py
python3 rmv124.py
python3 rmv125.py
python3 rmv126.py
python3 rmv127.py
python3 rmv128.py
python3 rmv129.py
python3 rmv130.py
python3 rmv131.py
python3 rmv132.py
python3 rmv133.py
python3 rmv134.py
python3 rmv135.py
python3 rmv136.py
python3 rmv137.py
python3 rmv138.py
python3 rmv139.py
python3 rmv140.py
python3 rmv141.py
python3 rmv142.py
python3 rmv143.py
python3 rmv144.py
python3 rmv145.py
python3 rmv146.py
python3 rmv147.py
python3 rmv148.py
python3 rmv149.py
python3 rmv150.py
python3 rmv151.py
python3 rmv152.py
python3 rmv153.py
python3 rmv154.py
python3 rmv155.py
python3 rmv156.py
python3 rmv157.py
python3 rmv158.py
python3 rmv159.py
python3 rmv160.py
python3 rmv161.py
python3 rmv162.py
python3 rmv163.py
python3 rmv164.py
python3 rmv165.py
python3 rmv166.py
python3 rmv167.py
python3 rmv168.py
python3 rmv169.py
python3 rmv170.py
python3 rmv171.py
python3 rmv172.py
python3 rmv173.py
python3 rmv174.py
python3 rmv175.py
python3 rmv176.py
python3 rmv177.py
python3 rmv178.py
python3 rmv179.py
python3 rmv180.py
python3 rmv181.py
python3 rmv182.py
python3 rmv183.py
python3 rmv184.py
python3 rmv185.py
python3 rmv186.py
python3 rmv187.py
python3 rmv188.py
python3 rmv189.py
python3 rmv190.py
python3 rmv191.py
python3 rmv192.py
python3 rmv193.py
python3 rmv194.py
python3 rmv195.py
python3 rmv196.py
python3 rmv197.py
python3 rmv198.py
python3 rmv199.py
python3 rmv200.py
python3 rmv201.py
python3 rmv202.py
python3 rmv203.py
python3 rmv204.py
python3 rmv205.py
python3 rmv206.py
python3 rmv207.py
python3 rmv208.py
python3 rmv209.py
python3 rmv210.py
python3 rmv211.py
python3 rmv212.py
python3 rmv213.py
python3 rmv214.py
python3 rmv215.py
python3 rmv216.py
python3 rmv217.py
python3 rmv218.py
python3 rmv219.py
python3 rmv220.py
python3 rmv221.py
python3 rmv222.py
python3 rmv223.py
python3 rmv224.py
python3 rmv225.py
python3 rmv226.py
python3 rmv227.py
python3 rmv228.py
python3 rmv229.py
python3 rmv230.py
python3 rmv231.py
python3 rmv232.py
python3 rmv233.py
python3 rmv234.py
python3 rmv235.py
python3 rmv236.py
python3 rmv237.py
python3 rmv238.py
python3 rmv224.py
```

## Skill only

`freech.py` replaces the Freeroll with a free cash challenge (300 coins, once an hour: a quick 1 v 1 photo battle, free, that pays $1.60 real cash on a win). `simplify.py` runs it for Skill and skips it when `YOFI_BUILD=real`, so Real Money keeps its Freeroll.

## Winner pop (Skill)

`winpop.py` gives every challenge win (coin challenge, head-to-head, friend and rivalry challenges, Quick Sprint, free cash challenge, bounty, showdown, tournament) one celebration pop: confetti, falling coins (or notes for cash), the winning photo with a trophy badge, the prize counting up, and a "Collect" button that flies the coins or cash into the balance.

```bash
python3 build-skill/winpop.py index.html skill-preview.html   # preview copy
python3 build-skill/winpop.py                                  # on "push live": patch index.html in place
```

## Upload hint (Skill)

`uploadhint.py`: if tapping an upload button opens no photo picker within ~1.5 s (some in-app browsers, such as the Claude app viewer, Facebook and Instagram, block it), a hint appears under the button pointing to the sample photos and to opening the page in Safari or Chrome. Run after `winpop.py`, same arguments.

## Upload read fix (Skill)

`uploadread.py`: chosen photos are read as data URLs instead of `blob:` links, which some hosts (the Claude app viewer) block, so photos picked from the library never appeared. Run after `uploadhint.py`, same arguments.

## Galleries (Skill preview)

`galleries.py` adds Gallery and Improve tabs to Touch-ups: a room of 3 frames per category (Pets → Travel → Nature → Family → Garden → Baking → Home), room tier set by its lowest photo (Gold 70, Diamond 80, Platinum 90), the next room opens at Gold, and hanging photos earn 2 coins × their rate when voters pick them. It also renames the photo levels to Gold / Diamond / Platinum / Masterpiece. Build the preview from the live `index.html`:

Then `album.py` shows the Gallery as a card album (binder page with sleeves, holographic tier foil, named photo cards, a big card view):

```bash
python3 build-skill/galleries.py index.html sp-g.html
python3 build-skill/album.py sp-g.html sp-a.html
python3 build-skill/album2.py sp-a.html sp-a2.html
python3 build-skill/improve2.py sp-a2.html sp-i2.html
python3 build-skill/votegoal.py sp-i2.html sp-v.html
python3 build-skill/votecash.py sp-v.html sp-c.html
python3 build-skill/noenergy.py sp-c.html sp-n.html
python3 build-skill/samples.py sp-n.html sp-s.html
python3 build-skill/compete.py sp-s.html sp-x.html
python3 build-skill/nowow.py sp-x.html sp-w.html
python3 build-skill/stakes.py sp-w.html sp-k.html
python3 build-skill/collect.py sp-k.html sp-j.html
python3 build-skill/jarfull.py sp-j.html sp-f.html
python3 build-skill/judge.py sp-f.html sp-u.html
python3 build-skill/jackpot.py sp-u.html sp-p.html
python3 build-skill/polish.py sp-p.html sp-m.html
python3 build-skill/map.py sp-m.html sp-q.html
python3 build-skill/potsheet.py sp-q.html sp-r.html
python3 build-skill/cmp2.py sp-r.html sp-c2.html
python3 build-skill/games.py sp-c2.html sp-g.html2
python3 build-skill/results.py sp-g.html2 sp-rs.html
python3 build-skill/places.py sp-rs.html sp-pl.html
python3 build-skill/coins.py sp-pl.html sp-co.html
python3 build-skill/friends.py sp-co.html sp-fr.html
python3 build-skill/upflow.py sp-fr.html sp-uf.html
python3 build-skill/tourlive.py sp-uf.html sp-tl.html
python3 build-skill/steal.py sp-tl.html sp-st.html
python3 build-skill/cmp3.py sp-st.html sp-c3.html
python3 build-skill/cardfix.py sp-c3.html sp-cf.html
python3 build-skill/winall.py sp-cf.html sp-wa.html
python3 build-skill/losetip.py sp-wa.html sp-lt.html
python3 build-skill/vreset.py sp-lt.html sp-vr.html
python3 build-skill/livegames.py sp-vr.html sp-lg.html
python3 build-skill/choose.py sp-lg.html sp-chs.html
python3 build-skill/jarpop.py sp-chs.html sp-jpp.html
python3 build-skill/votefx.py sp-jpp.html sp-vf.html
python3 build-skill/cpfix.py sp-vf.html sp-cp.html
python3 build-skill/screens.py sp-cp.html sp-sc.html
python3 build-skill/gstyle.py sp-sc.html sp-gs.html
python3 build-skill/ctafix.py sp-gs.html sp-ct.html
python3 build-skill/sprintic.py sp-ct.html sp-si.html
python3 build-skill/h2hopen.py sp-si.html sp-ho.html
python3 build-skill/qsicon.py sp-ho.html sp-qi.html
python3 build-skill/names.py sp-qi.html sp-nm.html
python3 build-skill/jartext.py sp-nm.html sp-jt.html
python3 build-skill/judgecard.py sp-jt.html sp-jc.html
python3 build-skill/galfix.py sp-jc.html skill-preview.html
```

`votecash.py` lays out Vote as goal bar → "Which is better?" with a small streak widget → photos → one cash card (a friend's challenge, else the category champion and the next tournament taking turns) and the "Head-to-head in N votes" line.

`votegoal.py` puts a goal bar at the top of Vote (in place of the "Coming up" chip): coins to the next touch-up of the photo holding back your collection, "upgrade is ready", or "add 2 more Pets photos"; tapping it opens that photo's card.

`noenergy.py` removes energy from the screen (votes were already unlimited): no energy bar, button, sheets, or "+N energy" rewards.

`album2.py` restyles the Gallery list: icon pills, "Pets collection" with a filled/tier badge, stitched binder, tier-foil cards with a burgundy "2x coins per vote / +20 today" band, the next collection as a picture sleeve, progress dots and one big button.

`improve2.py` replaces the Improve tab with the card-style screen: the photo card with a burgundy band previewing coins per vote, four touch-ups (Fix lighting, Boost colour, Sharpen details, Soften background) with projected scores, premium filters from 80, and Apply with the price set into the button. Touch-ups raise the matching part score so the overall score stays the average of the five, and the look is saved into the photo.

`samples.py` swaps the six Pets sample photos for the owner's dog photos in `samples/pets/` (600x800; dog-only, collar tag blurred).

`compete.py` merges the Compete and Tournaments buttons into one Compete menu with Challenges | Tournaments tabs.

`nowow.py` drops Wow factor: the overall score is the average of the four touch-up scores; existing photos are rescored once on load.

`stakes.py` lets players pick $1, $2 or $5 per daily photo challenge; a cash win earns 1 star per $1 (rematch doubles), 80% of the stake goes into the pot, and your stars for each category show on the front of its challenge photo. Players with 3+ stars share the 70% in proportion to their stars.

## Live (galleries build)

The live `index.html` now includes the galleries steps. Their input is the earlier live app, kept as `build-skill/pre-galleries.html`: run the chain from `galleries.py pre-galleries.html sp-g.html` through `gstyle.py`, then copy the result to `index.html` with the title "Yofi - Skill".

`collect.py` puts the coins your photos earn from voters' picks (and while you are away) into a jar on the top Vote card: "3 voters picked Milo", with a pulsing gold "+12" button that ticks up on each pick. Tap to collect and the coins fly into your balance. With nothing to collect, the earnings card reads "Milo earns 4 coins a pick" and "Earn more" opens Improve. It also sets the one status line on every photo screen to say what a voter's pick pays ("Earns you 2 🟡 per vote · 🥇 Gold earns 4", "🥇 Gold photos earn you 4 🟡 per vote"), and gallery sleeves show coins per vote instead of "2×". Each level pays one rate (unranked 2, Gold 4, Diamond 8, Platinum 12 coins per vote). Gallery photos show their level icon by the score, a gold "+N today" pill on the photo and "Earns N per vote" underneath. Reaching a new level shows a celebration with the new rate ("Milo is Gold! now earns you 4 🟡 per vote").

`jarfull.py` makes the coin jar fill over time from votes on your hung photos (replacing the one-off "while you were away" credit). It holds 8 hours of earnings; the Vote card shows a fill bar and "Jar full in 5h 0m", and once full it reads "Your coin jar is full!" and stops filling until collected. The Vote tab shows a gold "+N" badge for coins waiting, or a pulsing "FULL". The app always opens on Vote (signed-in players used to land on Compete). Completing a collection at a new level pays a free $1 cash challenge entry (S.cashTix), shown as a ticket on the celebration pop; "Play my free challenge" opens that category's daily challenge with the $1 stake marked FREE.

`judge.py` adds a judge score: how often your vote matches the crowd over your last 50 votes. The 🔥 pill still shows only streak days; a thin gold ring around the flame fills towards the next judge level and "+1 ✓" pops on a match. Tapping the pill opens the judge card: level (Good Eye, Sharp Eye 65%+, Expert 75%+ pays +1 coin a correct vote, Master 85%+ pays +2), a progress bar, two goals (8 of your next 10 right = +20 coins; reach the next level) and a 3-row league of players with a similar number of votes (simulated). The score shows after 20 votes; a level only drops when you fall 3% below it. The old "Daily rewards" pop (4 sessions a day) is gone: the streak is now one line in the judge card ("🔥 3-day streak · Vote 2 more today to keep it"), a streak day is 3 votes that day, and nothing pops up by itself.

`jackpot.py` gives the daily jackpot challenges (Today's photo challenges) every other turn in the green real-money card on Vote: "$2,855 Pet jackpot · You 0/3 ⭐ · from $1 · daily" with a green Play button that opens that category's challenge with the $1/$2/$5 stake picker. Categories you have a 70+ photo for take turns. Every 4th turn is Quick Sprint (1 v 1, pick the crowd's photo in 10 pairs) sold with your judge score: "Your 75% eye vs a 73% rival". An incoming friend challenge still comes first.

`polish.py` fixes the wrong-vote overlay (now a light card with navy text) and the score screen after an upload: all bar rows line up, rows and the button use the four touch-up names from Improve, and the button is gold because it spends coins.

`map.py` adds the collection map: a full-screen road of the 7 collections (finished stops gold with a tick, the current one bobbing under a "You are here" pin, locked ones grey; each shows its 3 slots and its 🎟️ reward). Stops pop in, the road marches, clouds drift. It shows the first time Gallery opens (S.mapSeen), from the collection badge ("🗺 1/3 filled"), and from the collection-complete pop ("See Travel on the map"), where the next stop unlocks with confetti. One button: "Fill Travel · 2 to go".

`potsheet.py` rebuilds the daily jackpot challenge screen: "🐾 Pet jackpot", the pot counting up with "Pays in 5h 35m", your star count ("Win a ⭐ to get a share" / "★ 5 · Your share now: about $9.28"), the ribbon holder vs your photo, the $1/$2/$5 chips, one green "Challenge · $2" button with "Win: +2 ⭐ and take the ribbon", and a "How it works" link. Under 70 the button becomes "✨ Touch up Coast to 70" (opens Improve). Rival photos never use one of your own photos. Every star now shares the 70% (no 3-star minimum), and all screens show your star count instead of "0/3".

`cmp2.py` turns Compete into two tabs by what competes. 📷 Your photo: Daily jackpots (a pot card per category, yours first), 1 v 1 now (Head-to-head, Beat the champion, Challenge a friend), Tournaments: Sprint (the one knockout: pyramid icon, 16 photos, starts when 16 have joined; $2 entry, winner $25, finalist $2.20, $4.80 rake) and Showdown, then Clubs. Big Cup is removed (a bigger field would cost too many live votes). 🎯 Your eye (shows your judge score): your judge card, Quick Sprint and Crowd Championship. Picture-led: jackpots are a swipeable row of photo cards (pot, your stars, green Play), 1 v 1 games are photo tiles (your photo VS a rival, the champion, a friend) with "$1 → $1.70" pills, tournaments are navy banners with countdown chips, and Your eye shows your score as a ring and Quick Sprint as your ring VS a rival ring. Green pills always show the entry price. Rivals never show your own photos. Coin Cup is no longer listed in Compete. The tournament list and Clubs keep the same two tabs on top.

`games.py` gives every cash game the same screen: name + one line, a green prize box (what you can win + when), a VS picture (rival left, you right: photos, eye rings, a room of 5, or "the field"), 3 stake chips that each say what they win (or one outlined chip when the stake is fixed), one big green "Play · $2" button and one small link. Games: Daily jackpot, Head-to-head (with "Challenge a friend instead"), incoming friend challenges (Accept · $1 / Decline, stake set by the friend), Quick Sprint, Showdown, Big Cup / Sprint and Crowd Championship. Champion is cut (the jackpot ribbon holder plays that role). The Vote card and Compete open these screens; an incoming challenge shows at the top of 1 v 1 and on the Vote card as "🤝 @mike challenged you".

`results.py` gives jackpot, head-to-head and friend challenges one result screen in the same style as the game screen: name + "Pet · Final result", a headline ("You won!" / "@mike won", by N votes), a prize box (green "+2 ⭐ · Your share now" or "$1.70 · Added to your cash"; neutral "You lost $1" with one tip), the VS photos with a WINNER tag and votes, the vote bar, one green "Play again · $2" / "Rematch" button and a "Back to voting" link. It also shows your stars today ("★ 2 TODAY") big and gold on the Compete jackpot photos.

`places.py` brings Quick Sprint, Showdown, Crowd Championship and knockout tournaments into the same result frame. 1 v 1 games (Quick Sprint) show VS (your score ring vs theirs); games with many players show your place in a list: the top places, a dashed "paid" line, you highlighted with the players either side, "+N more". Crowd Championship shows standings so far when your run ends ("11/15 right · You’re 23rd of 205 so far", results at the hour). Tournament "Play · $1" now joins in one tap, and Sprint says "Starts 1 min after you join" instead of a countdown that never moved.

`coins.py` rebuilds the coin balance drop-down ("Your coins · 180 🟡"): Touch-ups first, then "Practise for coins" with Quick Sprint · coins and Head-to-head · coins (same names as the cash games; one marked Suggested: Quick Sprint once your judge score is 70%+), and a green line to the cash versions. The coin game screen is titled "Head-to-head · coins". The usual celebration pop ("You’ve got 260 coins" · Use my coins / Keep voting) shows only at high milestones (250, 500, 1,000, 2,500 coins; the top card already nudges touch-ups); each once (S.coinPop), at most once per visit, only on Vote with nothing else open.

`friends.py` makes friend challenges work in coins and cash (they bring new players in). The friend challenge screen has a Coins | Cash toggle: 100 / 250 / 500 🟡 (gold, winner takes double) or $1 / $2 / $5 (green, into the club pot); the WhatsApp button says what it costs. The coin drop-down offers Challenge a friend · coins (Suggested) and Quick Sprint · coins; Head-to-head · coins is gone because it used live votes on strangers' matches. Compete › Your photo › 1 v 1 has a "Challenge a friend" tile next to Head-to-head.

`upflow.py` puts the upload journey in order: pick a photo (or a sample) → "Name your photo" with the photo shown (button "Score my photo") → the scan → straight onto Improve with the score counting up from 0. The first photo comes with a welcome gift of coins that covers its first touch-up (S.firstGift). The Improve button uses the touch-up name ("Soften background") and is gold. The old "Touch up your photo" result screen no longer flashes for new uploads, and the collection map waits until the next Gallery visit.

`tourlive.py` restyles the live knockout (Sprint) screen: pyramid icon with "Sprint · Knockout of 16 · live", a calm "You’re out · Level 1" box, framed photos with names underneath (not over the photos), counts by each name under the vote bar, a small "20 votes to go" chip, and "Keep voting". The lobby shows "15/16 joined" with a fill bar instead of a countdown, and "It starts when 16 have joined".

`steal.py` adds card stealing. Gallery photos are cards that earn per vote. After 2h+ away, a (simulated) rival may steal one card (you keep what it earned; its slot is empty until you win it back). On return the usual key-moment pop shows "While you were away · +40 🟡 earned by your cards" (the jar is collected) and "1 card stolen · Emma won 5–4" with "Win Falls back". Steal battles (win back, or steal a rival's card from Compete › Your photo › Cards): risk one of your cards, first to 5 votes wins both cards, 3 a day, navy buttons (no money at stake). A stolen card joins your collection ("🃏 Won from Zara") and earns for you; it is never entered in cash games. Platinum cards (90+) can't be stolen or risked and show a "🛡 Safe" tag.

`cmp3.py` lays out Compete › Your photo as agreed: Daily jackpots (photo cards with "From $1" / "Add photo", "Ends in" timer), Head-to-head (VS photo card, "Entry $1 · Win $1.70", green "View matchup"), Challenge a friend (WhatsApp row, green "Invite"), Card challenges panel ("Win Falls back · Emma won 5–4" + navy "Rematch"; "Steal a card"), Tournaments as full-width navy rows (gold "Win $25", green "Entry $2"), then Clubs.

`cardfix.py` tidies three things: the Improve button uses the shared gold coin button (centred "Fix lighting · 50 🟡"); the first photo's welcome gift is a small coin fly-in plus one gold line under the score ("🎁 Welcome gift · first touch-up on us"), and big "+N" coin banners stay on screen; cards won in a steal show "🃏 Won from Maya" in the bottom pill instead of over the score.

`winall.py` makes every game win pause on the winner pop before the result screen (jackpot, head-to-head, friend, Quick Sprint, Showdown, Sprint, Crowd Championship, card steals). Cash and coin prizes say "Collect" and fly into the balance; stars and cards say "See result". If a game already fired its own winner pop, that one is kept, so there is only ever one pop per win.

`losetip.py` keeps a lost game to two actions. If the photo you played with scores under 75, the main button is gold "✨ Touch up <name>" (opens Improve on it) and the rematch becomes the link; otherwise it's the rematch button and the Back link. Card steals are left out.

Card steals are now free to try (like Steal a Brainrot): a steal or win-back battle never risks one of your cards. Lose and nothing is taken; it just uses one of your 3 daily tries ("Not this time · Nothing lost · 2 of 3 tries left today", with "Try again"). Cards are only lost to overnight steals, and Platinum cards stay safe from those.

`vreset.py` clears each photo's vote record once (votes, coins earned from votes, lost games and the out-of-lives flag) on the next open. Scores, cards, coins and the judge score stay.

`livegames.py` puts a "Live games" row under the vote, replacing the single green card. Tiles use short fixed lines so every word shows (chip on the photo, big "Win …" line, one small detail line, entry button: green cash, navy free). What just happened leads in gold (a friend's challenge, a stolen card, a jackpot where your photo won stars today), then Jackpot, Head-to-head, Challenge a friend, Sprint and Steal. "See all ›" opens Compete.

Live games tiles: each tile has a third small detail line ("Result in minutes", "Starts at 16", "3 of 3 tries left") and a one-line entry button ("Play · $1", "Join · $2", "Play · free"); tile photos are 96px tall (doubled at the user's request), so the buttons sit just below the fold and show with a short scroll.

Compete › Your photo: the Your photo | Your eye tabs scroll with the page instead of floating over the jackpot cards. With no photo at 70+, Head-to-head shows the VS card with a rival photo and your best photo ("62 → 70" badge), "Get Milo to 70 to play · Entry $1 · Win $1.70" and a gold "Improve" button that opens Improve on that photo (navy "Add photo" if you have none).

Live games moment tiles: 5+ right votes in a row adds a gold "🔥 N right · Win $3.20 · Quick Sprint · Play · $2" tile (gone after you play it or miss a vote); a Crowd Championship starting within 15 minutes adds a gold "⏱ N min · 1st wins $X · Join · $2" tile (gone once you join).

`choose.py` lets players choose their next collection: when a collection reaches Gold, the pop says "Pick any collection to open next" with a navy "Choose your next collection" button. The picker lists every locked collection with "N of your photos fit" (ones you can fill first, in gold). The pick moves into the next spot and plays the map unlock reveal; the order is saved in `S.galPath`. If the pop is closed, the map offers the choice (pulsing locked stops, "Choose your next collection" button).
Tapping a locked category in the Gallery opens the collection map (or the picker when a choice is waiting), instead of the old "opens when all 3 … reach Gold" toast.

The coin jar now holds 3 hours of earnings and fills in 3 hours (`JAR_HRS = 3` in `jarfull.py`; same coins per hour, so more frequent, smaller collects).


`jarpop.py` adds the coin jar receipt. One tap still collects (coins fly in at once); then a pop shows what each photo earned since your last collect ("+68 collected · since 2h 36m ago"): your photos with tier and +coins, cards you stole in gold ("won from Maya +14", "Stolen cards earned you +14 extra", or a "Steal a card" teaser if you have none), and cards taken from you in red ("Emma has it · missed ~22"). One navy button ("Win Tidepool back" or "Steal a card · free try") and "Done". Only shows when you tap the jar yourself.

The Steal button under the vote photos was removed (user decision); stealing stays in the Live games row (Steal / Stolen tiles), the coin jar receipt, and Compete.

Stolen cards always earn into the coin jar, on top of your collections, even when their collection is locked or full (`jarHung` in `jarfull.py`). The jar receipt lists every stolen card you own, even at +0.
The jar receipt reads as a payday: a gold "💰 PAYDAY" badge, "+67" counting up, "🗳 Voters picked your photos in the last 2h", rows sliding in with each amount counting up, "📸 Your photos earned" / "🃏 Stolen cards · bonus" / "😤 Taken from you" sections, "🎉 Stealing earned you +18 extra", and confetti.
The jar receipt always offers stealing when there is a rival card: "Steal a card · 3 free tries left", or "Steal a card · new tries tomorrow" when the day's 3 are used. The "Steal a card" teaser row is tappable too.

`votefx.py` makes voting exciting: right votes burst coins towards you; now and then one of the two vote photos is a face-down "✨ Special" tile (the other photo waits) that flips in place when tapped: 🃏 Joker +20/+50/+100 coins (60/30/10%), 🛡 Shield (blocks one overnight steal, hold up to 3, 🛡 pill in the header), or every 10–15 votes 🦝 Steal, which switches straight to a Raid. The raid is a full-screen heist (flash, slam, rotating rays, sparkles, a rival's wall of 3 spot-lit framed photos; best of 3 live votes with bursts and a "Deciding vote!" moment; win = gold flash, confetti, coin rain, the photo spins in as a NEW CARD; lose = "So close!", nothing lost), then "Back to voting". Raids are free and don't use the 3 daily steal tries.
After a raid win, "Back to voting" flies the stolen card into the earnings card at the top of Vote, which turns gold for 7 seconds with a shimmer: "<name> is earning for you · 🃏 Stolen card · in your collection" and a "+8 a vote" chip, then goes back to normal.
The special tile cracks open in 3 taps: tap 1 shudders it and a glowing crack appears ("Again!"), tap 2 adds cracks and it glows gold (Joker), blue (Steal) or silver (Shield) ("One more!"), tap 3 bursts it open in place with sparks (no flip) and the prize appears one piece at a time: the icon, then the title, then the amount. A Joker's amount (random 20/50/100) slams in with glowing rays and sparks: "Joker! +20", "Big Joker! +50" (bigger number, double burst), "MEGA Joker! +100" (red giant number, gold flash, screen shake), then the coins fly to your balance.
Joker reveals use the user's card art (`build-skill/assets/joker20.jpg`, `joker50.jpg`, `joker100.jpg`: teal / purple / red), embedded by `votefx.py`. The special tile follows its vote photo every frame, so it stays lined up if the page shifts or scrolls.
Steal reveals use the user's Steal card art (`build-skill/assets/steal.jpg`) with a green glow and sparks, held for a moment before the raid opens.

The raid is now called Steal everywhere a player sees it ("STEAL!" banner, "another steal is coming").
Special tiles fit their vote photo exactly: the tile re-finds the current photo every frame (photos can be rebuilt or pushed down by the jar card), positions are measured from the real containing block, nothing tilts (the face-down tile pulses its glow instead of wiggling), and the Joker/Steal art fills the whole photo.

`cpfix.py`: tournaments that need other players (Crowd Championship, Sprint) are no longer offered in the Live games row on Vote, only in Compete. Crowd Championship and Quick Sprint picks stamp "✓ Right!" / "✗ Missed" on your photo (sparks on a right pick), the progress dots turn green/red, the Championship tip reads "Everyone gets the same 15 pairs · top 20% share the prize", and a finished Championship run opens a celebration pop ("You're in the money!" / "Great eye!" / "Run complete!", "9/15", place so far, results time) before the standings.
Vote screen: the crowd's % is bold in the "So close! / Missed it" box ("**57%** picked the other one").

Challenge special tile: about 1 in 25 right votes (when you have a photo at 70+) the special tile holds the Challenge card art (`build-skill/assets/challenge.jpg`, red hint glow on tap 2); after the reveal the head-to-head offer opens and the player chooses whether to play. Steal votes show as numbered 1 2 3 slots that fill with the photo that won each vote (gold ring = rival, blue = you), with the tally in screen order (rival – you). Lost results show the "You lost" box in soft red.

Every steal uses the same full-screen Steal (Live games tile, Payday receipt, Compete, win-backs); the old first-to-5 sheet is no longer used. Button-started steals use one of the 3 daily tries; Steal tiles while voting are free. Win-backs go straight to the vote: "WON BACK! · back in your gallery".

Live games row: Steal / Stolen tiles removed; the jackpot tile chip reads "💰 Pet challenge"; the Friend tile is WhatsApp green with a white icon.

`screens.py` redoes two screens to the user's mock-ups. Rematch: "REMATCH?", both photos with "Score 84" pills (tap yours to change photo), "<part> made the difference", "Choose your entry" $1/$2/$5 with the stars a win earns (doubled for a rematch), one gold Touch up row, green "Rematch for $2", "Win to earn 4 stars · double for a rematch". Quick Sprint: illustrated rival / you avatars (`assets/av_rival.jpg`, `av_you.jpg`; your profile photo replaces yours when set) with the eye % in a red / navy pill.

The Challenge special tile uses the user's head-to-head card art (`assets/challenge.jpg`). The 1 v 1 tile is gone from the Live games row (head-to-head now comes from the tile reveal); the row is Pet challenge and Friend.
Live games row: "💰 Pet challenge" and "🤝 Friend challenge".

Steals are a score face-off instead of a vote: the rival wall hides scores ("?", "Score hidden"); you pick the photo you think scores lowest; your best photo's score shows, theirs shakes as "?" then slams in with a flash and sparks; match or beat it to steal it ("79 beats 76!"). Win-backs compare your best photo with your held card the same way.

Payday receipt rows show each photo's tier and multiplier, for your photos and stolen cards: "💎 Diamond ×4 · 8 🟡 a vote" ("No tier ×1" under 70).

The Live games jackpot tile follows the category being voted on: voting "Best Nature & Seasons" shows "Nature challenge", "Best Pet" shows "Pet challenge".

`gstyle.py` restyles the Gallery to the user's binder mock-up: navy leather binder with gold stitching and round gold rings, cream page with "Pets Collection" + "1/3 filled" and a gold rule, gold-framed photo cards with a round score medallion and a name / tier / per-vote plaque inside the card, glossy empty sleeves, and the next collection as a navy leather card (photo, gold lock, "Travel Collection", "Opens at Gold").
Gallery binder rings are angled gold loops from the leather spine into a punched hole in the page margin.

Losing a steal shows a gold "✨ Touch up Milo · beat 77" button (opens Improve on your best photo) and a "Back to voting" link. Live games labels sit above the tile image instead of over it, and the "⚔️ 1 v 1 challenge" (head-to-head) tile is back in the row.

`ctafix.py`: the touch-up keeps one name from Improve to Before and after. While the welcome gift covers the first touch-up, the gold Improve button reads "Boost colour · Free 🎁" (not the 50-coin price); the selected touch-up row shows "↑" instead of a projected score the result rarely matched; the Before and after button reads "Use Boost colour · Gold 🥇" (was "Touch up · Unlock Gold") and stays navy because nothing more is spent there. Live `index.html` input: run it after `gstyle.py`.

`sprintic.py`: Sprint uses the pyramid icon everywhere (4 levels of 1 v 1): next to the title on its game screen (was a stopwatch), on the field tile (was a trophy) and on the Compete › Tournaments row. The game line reads "4 rounds of 1 v 1 · 16 photos".

`h2hopen.py`: no score locks on higher stakes. Head-to-head $5 and $10 (and tournament tiers) are open to any photo; the "🔒 80+ / 90+" chips are gone.

Lost games (`losetip.py`) now always lead with the gold "✨ Touch up <name>" button whenever the photo can still be touched up (was only under 75); "Play again" moves to the link. The Payday receipt (`jarpop.py`) no longer shows the "×2" multiplier badge next to "4 🪙 a vote".

Shield reveals use the user's navy Shield card art (`build-skill/assets/shield.jpg`, embedded by `votefx.py`), fitted inside the tile on a navy background. Showdown uses a race icon (5 pins racing to a chequered finish line, from the user's mock-up) on its Compete row, game screen and result (`sprintic.py`); the row reads "5 entries · top vote wins".

Live games Friend tile shows your own best photo (the one you'd play with) with a small green WhatsApp badge in the corner, instead of the plain green WhatsApp tile (`livegames.py`).

`qsicon.py`: Quick Sprint uses its rival / you avatars everywhere. Compete › Your eye shows the two avatars with their eye % pills on the Quick Sprint button (was two score rings), and Vote › Live games has a Quick Sprint tile after the 1 v 1 tile (avatars VS, "Win $3.20", "Your eye vs a rival", "Play · $2"); it is left out while the 🔥 streak Quick Sprint tile is showing.

Live games: the 1 v 1 tile is now called "⚔️ Head-to-head" (same name as its game screen and Compete) and always shows when you have a photo. Under 70 it reads "Get Milo to 70 · Then play for $1" with a gold "✨ Touch up" button that opens Improve; a photo already in a game reads "Milo is in a game" with a navy "See game". Sprint stays out of Live games because it isn't instant (`qsicon.py`).

`names.py`: games are named by what competes (user chose option A). Your photo competes: Head-to-head is now **Photo Duel**, Sprint is now **Photo Knockout**. Your judging competes: Quick Sprint is now **Judge Duel**. "Crowd Sprint" labels read Crowd Championship. It swaps the text across the whole app (code comparisons change on both sides); lower-case ids such as `'sprint'` are untouched. Run it last.

Compete tabs use the game families: "📷 Photo games | 🎯 Judge games" (was Your photo | Your eye), and the judge card's label reads "Your judge score" (`names.py`). The Judge Duel avatars on the Compete button sit in round frames (`qsicon.py`).

`jartext.py`: the coin jar card on Vote says plainly whose photo earned what (user chose option A): "Milo earned you 16 coins" / "Players voted for it" / fill bar / "Full in 1h 5m", a "Your photo" label on the picture, and the gold button reads "Collect +16" (was "A voter picked Milo · Jar full in …").

Judge Duel result screen uses the same rival / you avatars as its game screen (score such as "6/10" in each pill, gold WINNER tag on top) instead of score rings; the loss tip reads "Vote more to sharpen your judging" (`qsicon.py`).

The upgrade card on Vote matches the coin jar card: "Milo can reach Diamond" / "71 → 80 · 8 coins a vote", a "Your photo" label on the picture, and a gold "Improve" button with the cost ("120 🪙") under it (was "Milo’s upgrade is ready · 71 → 80 for Diamond · 120 c…") (`jartext.py`).

The "Your photo" label on the coin jar and upgrade cards was removed (user decision).

`judgecard.py`: the judge card (tap the 🔥 pill) follows the user's "Judge status" mock-up: a Current rank card (medallion, rank, "34% accuracy", "You picked the crowd favourite in 11 of your last 32 votes."), a Rank progression ladder of the four ranks (Good Eye 👁️, Sharp Eye 🦅 65%, Expert 🏅 75% +1 coin a correct vote, Master 👑 85% +2) marked Current / Next / Top rank, League position and Judging streak tiles, and one navy "Keep voting" button. The goal rows and 3-row league list are gone; the 8-of-10 bonus still pays.

`galfix.py`: a Gallery binder page with no photos yet keeps its layout. The empty sleeves on the first row had no height, so their "+ Add a home photo" labels sat on the page title; empty sleeves now keep a filled card's height.

The coin jar card was simplified (user mark-up): no "Players voted for it" line, and the button reads just "Collect" because the amount is already in the title (`jartext.py`).
