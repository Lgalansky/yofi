# Real Money build, step 15 (after rmv11.py): the agreed Real Money loop.
#  - No paid fixed-payout qualifiers: qualifiers are the free voting game (coins). Upsells point to the Final.
#  - Photo entry is free once a photo is 70+ (touch up with coins to get there). Touch-up row back in the coins menu for photos under 70.
#  - Coins buy a free $1 Final pick (250 coins, 2 an hour) in the real pool. No free $1 qualifier.
#  - Final pool split: 78% top pickers, 10% finalists' creators (1st 4%, 2nd 2.5%, 3rd 1.5%, 4th-6th 2% shared), 12% Yofi.
#    Replaces the creator's 10% qualifier share. Perfect rosettes bonus is a fixed $25.
#  - Coin players see coin games only; depositors don't see the coin challenge.
#  - "Final entry" wording becomes "Final pick".
import os, re
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
def RX(p, b, n=1):
    global s; m = re.findall(p, s, flags=re.S); assert len(m) == n, (p[:80], len(m)); s = re.sub(p, lambda _: b, s, flags=re.S)

s = s.replace("function fcNotify() {", r"""const FIN_CR = [4, 2.5, 1.5, 2 / 3, 2 / 3, 2 / 3];
const finShare = (sl, pl) => +((ppGame(sl).players * RACE_AVG) * (FIN_CR[pl - 1] || 0) / 100).toFixed(2);
function gtUpsell() { const g = ppGame(), nm = raceName(g.sl);
  if (isCash()) return `<button class="btn block pc-go" id="gtFin">🎀 Pick the ${nm} Final · from $1</button>`;
  return fqLeft() && (S.gems || 0) >= FREE_BET_COINS ? `<button class="btn block pc-go" id="gtFin">🎟️ Free $1 pick in the ${nm} Final · ${FREE_BET_COINS} 🟡</button>` : `<button class="btn block pc-real" id="gtFin">💵 Pick the ${nm} Final for real · from $1</button>`; }
function fcNotify() {""", 1)

# --- qualifiers: no cash share, no fixed-payout real version
RX(r"share = \+\(\(30 \+ Math\.floor\(q\(\) \* 50\)\).*?setTimeout\(\(\) => \{ paintGems\(\); paintWallet\(\); \}, 100\);", "setTimeout(paintGems, 100);")
RX(r'<p class="gt-own">.*?</p>', '')
RX(r"\$\{tk && fqLeft\(\).*?win \$\$\{GATE_CASH\[3\]\}</button>`\}(?=\n)", "${gtUpsell()}")
RA("if ($('#gtTk')) $('#gtTk').onclick = () => fqStart();", "if ($('#gtFin')) $('#gtFin').onclick = () => { popClose(); setTimeout(ppOpen, 250); };")

# --- photo entry free at 70+
RA("  const free = !S.showFreeUsed; if (!free && (S.gems || 0) < SHOW_ENTRY) { toast(`Entering a photo costs ${SHOW_ENTRY} 🟡. ${y ? 'Judge' : 'Vote'} to earn ${SHOW_ENTRY - Math.floor(S.gems || 0)} more.`); return; }\n  if (free) S.showFreeUsed = 1; else { S.gems -= SHOW_ENTRY; paintGems(); }\n", "")
RA("📷 Enter a new photo to compete · ${free ? 'first one free' : `${SHOW_ENTRY} 🟡`}", "📷 Enter a new photo · free at ${FR_MIN}+")
RA("Enter<small>${free ? 'first one free' : `${SHOW_ENTRY} 🟡`}</small>", "Enter<small>free</small>")
RA("<em class=\"${ok ? '' : 'need'}\">${free ? 'Free' : `${SHOW_ENTRY} 🟡`}</em>", "<em>Free</em>")
RA("Win a qualifier and you get <b>10% of its real entries</b>. Entering costs ${SHOW_ENTRY} 🟡 (first one free): up to",
   "Every finalist’s creator shares <b>10% of the Final pool</b>. Entering is free once a photo is ${FR_MIN}+ (touch it up with coins): up to")
RA("if (0 && up) {", "if (up && up.s.total < CFG.QUALIFY) {")
RA("if (f) I.push({ ic: '🏅', t: 'Coin challenge'", "if (f && !isCash()) I.push({ ic: '🏅', t: 'Coin challenge'")

# --- coins buy a free $1 Final pick, 2 an hour
RA("gateOpen(true, true); }", "ppOpen(); }")
RA("You’ve used both free $1 qualifiers this hour.", "You’ve used both free $1 Final picks this hour.")
RA("<b>Free $${GATE_FEE} qualifier</b><small>Pick the top 3 of 5 · 3 right win <b>$${GATE_CASH[3]}</b> cash · ",
   "<b>Free $1 Final pick</b><small>The ${raceName(ppGame().sl)} Final · pick the top 3 of 6 · ")
RA("'Your free $1 qualifier is ready' : 'Free $1 qualifier · win $5'", "'Your free $1 Final pick is ready' : 'Free $1 Final pick'")
RA("const freeOk = (S.gems || 0) >= FREE_BET_COINS;", "const freeOk = (S.gems || 0) >= FREE_BET_COINS && fqLeft() > 0;")
RA(": `<button class=\"btn block pc-real\" id=\"ppReal\"",
   ": `<button class=\"btn block pc-go\" id=\"ppFree\" ${n3 && freeOk ? '' : 'disabled'}>🎟️ Free $1 pick · ${FREE_BET_COINS} 🟡</button>${!fqLeft() ? `<p class=\"pp-r\">Both free picks used this hour · next in ${frMinsLeft()} min</p>` : (S.gems || 0) < FREE_BET_COINS ? `<p class=\"pp-r\">${FREE_BET_COINS - Math.floor(S.gems || 0)} more 🟡 for a free pick. ${y ? 'Judge' : 'Vote'} to earn them.</p>` : `<p class=\"pp-r\">${fqLeft()} of ${FQ_MAX} free picks left this hour</p>`}\n        <button class=\"btn block pc-real\" id=\"ppReal\"")
RA("S.gems -= FREE_BET_COINS; paintGems(); rec(1, true);", "if (!fqLeft()) return; fqClaim(); rec(1, true);")
# second free pick in the same hour adds $1 to the pick
RA("${e && e.free && !cash ? `<button class=\"btn block pc-real\" id=\"ppMore\">",
   "${e && !cash && fqLeft() && (S.gems || 0) >= FREE_BET_COINS ? `<button class=\"btn block pc-go\" id=\"ppAdd\">🎟️ Add a free $1 · ${FREE_BET_COINS} 🟡</button>` : ''}${e && e.free && !cash ? `<button class=\"btn block pc-real\" id=\"ppMore\">")
RA("    if ($('#ppMore')) $('#ppMore').onclick",
   "    if ($('#ppAdd')) $('#ppAdd').onclick = () => { if (!fqLeft()) return; fqClaim(); S.pp[g.sl].stake = (S.pp[g.sl].stake || 1) + 1; save(); toast('🎟️ Free $1 added to your pick'); popClose(); setTimeout(ppOpen, 300); };\n    if ($('#ppMore')) $('#ppMore').onclick")

# --- Final pool split + creators' share + fixed perfect bonus
RA("const raceJP = sl => 250 + ((sl * 37) % 900);", "const raceJP = sl => 25;")
RA("const ppPool = (n, cur) => `$${Math.round(n * RACE_AVG * .8).toLocaleString()}`;", "const ppPool = (n, cur) => `$${Math.round(n * RACE_AVG).toLocaleString()}`;")
RA("net = n * RACE_AVG * .8, perfect", "net = n * RACE_AVG * .78, perfect")
RA("Top 10% share the pool by entry size.", "Top 10% share 78% of the pool by pick size · 10% to the finalists’ creators · 12% Yofi.")
RA("x.done = 1; x.place = pl; x.prize = pz;", "const fsh = pl <= RACE_N ? finShare(sl, pl) : 0; if (fsh) { S.cash = +((S.cash || 0) + fsh).toFixed(2); S.showWon = +((S.showWon || 0) + fsh).toFixed(2); earnAdd({ kind: 'f', pid: x.pid, t: ph.t, amt: fsh, place: pl, sl, k: g.k }); setTimeout(paintWallet, 200); } x.done = 1; x.place = pl; x.prize = pz; x.share = fsh;")
RA("<p class=\"pp-m\">${pz ? `You won <b>${amt}</b>` : 'Top 3 win prizes.'} · form",
   "<p class=\"pp-m\">You earned <b>${money(pz + (x.share || 0))}</b>: ${money(x.share || 0)} share of the Final pool${pz ? ` + ${amt} prize` : ''} · form")
RA("${e.kind === 'q' ? '🥇 Won its qualifier' :", "${e.kind === 'f' ? `🎀 Finalist · ${ppOrd(e.place)} · pool share` : e.kind === 'q' ? '🥇 Won its qualifier' :")
RA("(n => `${n} qualifier win${n === 1 ? '' : 's'}`)(L.filter(e => e.kind === 'q').length)", "(n => `${n} pool share${n === 1 ? '' : 's'}`)(L.filter(e => e.kind === 'f').length)")
RA("Enter a photo: the 1st place photo in a qualifier earns 10% of its real entries, and the Final’s 🥇🥈🥉 win $10 · $5 · $2.",
   "Get a photo into a Final: every finalist’s creator shares 10% of the Final pool, and the top 3 also win $10 · $5 · $2.")
RA("Your winnings will show here: qualifier wins and Final places.", "Your winnings will show here: Final pool shares and prizes.")

# --- wording: Final pick, not entry
for a, b in [("'Your free $1 entry is in!'", "`Your free ${money(e.stake || 1)} pick is in!`"), ("`Your ${money(e.stake || 1)} entry is in!`", "`Your ${money(e.stake || 1)} pick is in!`"),
             ("'A Final entry'", "'A Final pick'"), ("'🎟️ Free $1 entry in! Watch it live.'", "'🎟️ Free $1 pick in! Watch it live.'"),
             ("'free $1 entry' : `${money(st)} entry`", "'free $1 pick' : `${money(st)} pick`"), ("💵 Enter for real · from $1", "💵 Pick for real · from $1"),
             ("💵 Add to your entry · from $1", "💵 Add to your pick · from $1"), ("🎀 Enter ${money(stake)} on my 1-2-3", "🎀 Pick for ${money(stake)}"),
             ("'enter from $1' : 'free $1 entry'", "'pick from $1' : 'free $1 pick'")]:
    assert a in s, a; s = s.replace(a, b)

# --- photos enter the qualifiers at 70+ (not the friend-challenge 80)
a = s.find('var SHOW_ENTRY'); b = s.find('function friendsPop'); s = s[:a] + s[a:b].replace('FR_MIN', 'SHOW_MIN') + s[b:]
a = s.find('function rcStatus'); b = s.find('\n', s.find("if (p.s.total < FR_MIN) return { cls: 'low'", a)); s = s[:a] + s[a:b].replace('FR_MIN', 'SHOW_MIN') + s[b:]
RA("var SHOW_ENTRY = 100;", "var SHOW_ENTRY = 100, SHOW_MIN = 70;")
RA("to ${SHOW_MIN}+ to enter the show`", "to ${SHOW_MIN}+ to enter the qualifiers`")
RA("function raceBetRowHTML() { const L = fqLeft(),", "function raceBetRowHTML() { if (isCash()) return ''; const L = fqLeft(),")
open(d + 'yofi-real.html', 'w').write(s); print('rm v12 ok')
