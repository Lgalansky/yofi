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
```

## Skill only

`freech.py` replaces the Freeroll with a free cash challenge (300 coins, once an hour: a quick 1 v 1 photo battle, free, that pays $1.60 real cash on a win). `simplify.py` runs it for Skill and skips it when `YOFI_BUILD=real`, so Real Money keeps its Freeroll.
