# Real Money build, step 12 (after rmv8.py):
#  1) Entering a photo costs 100 coins (first one free). The 3 spots stay.
#  2) Coins turn into a free $1 qualifier (pick 3 of 5, cash prizes: 3 right $5, 2 right $1.50) for 250 coins,
#     max 2 per hour. This replaces the free $1 Final entry.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

s = s.replace("function fcNotify() {", r"""var FQ_MAX = 2;
const fqLeft = () => FQ_MAX - (S.fqH === frHourKey() ? (S.fqN || 0) : 0);
function fqClaim() { if (S.fqH !== frHourKey()) { S.fqH = frHourKey(); S.fqN = 0; } S.fqN++; S.gems -= FREE_BET_COINS; paintGems(); save(); }
function fqStart() { try { closeSheet(); } catch (x) {} const y = isYoungW();
  if (!fqLeft()) { toast(`You’ve used both free $1 qualifiers this hour. Next ones in ${frMinsLeft()} min.`); return; }
  if ((S.gems || 0) < FREE_BET_COINS) { toast(`${y ? 'Judge' : 'Vote'} and win free qualifiers to earn coins. ${FREE_BET_COINS - Math.floor(S.gems || 0)} 🟡 to go.`); return; }
  gateOpen(true, true); }
function fcNotify() {""", 1)

# 1) photo entry 100 coins, first free
RA("var SHOW_ENTRY = 200;", "var SHOW_ENTRY = 100;")
RA("  const r = rcRec(id); r.st = 'heats'; r.runs = 0;",
   "  const free = !S.showFreeUsed; if (!free && (S.gems || 0) < SHOW_ENTRY) { toast(`Entering a photo costs ${SHOW_ENTRY} 🟡. ${y ? 'Judge' : 'Vote'} to earn ${SHOW_ENTRY - Math.floor(S.gems || 0)} more.`); return; }\n  if (free) S.showFreeUsed = 1; else { S.gems -= SHOW_ENTRY; paintGems(); }\n  const r = rcRec(id); r.st = 'heats'; r.runs = 0;")
RA("data-msen=\"${p.id}\">Enter<small>free</small>", "data-msen=\"${p.id}\">Enter<small>${free ? 'first one free' : `${SHOW_ENTRY} 🟡`}</small>")
RA("📷 Enter a new photo to compete · free</button>", "📷 Enter a new photo to compete · ${free ? 'first one free' : `${SHOW_ENTRY} 🟡`}</button>")
RA("<b>Enter a photo to compete</b><small>Qualifiers, then the hourly Final · top 3 win $10 · $5 · $2</small></span><em>Free</em>",
   "<b>Enter a photo to compete</b><small>Qualifiers, then the hourly Final · top 3 win $10 · $5 · $2</small></span><em class=\"${ok ? '' : 'need'}\">${free ? 'Free' : `${SHOW_ENTRY} 🟡`}</em>")
RA("Entering is free: up to ${SLOT_BASE} photos in play,", "Entering costs ${SHOW_ENTRY} 🟡 (first one free): up to ${SLOT_BASE} photos in play,")
RA("${n < SLOT_BASE ? `Entering is free · ${SLOT_BASE - n} spot", "${n < SLOT_BASE ? `${SLOT_BASE - n} spot")

# 2) coins -> free $1 qualifier, 2 per hour
RA("function gateOpen(real) {", "function gateOpen(real, tk) {")
RA("${real ? `<div class=\"on\"><b>Entry $${GATE_FEE}</b>", "${real ? `<div class=\"on\"><b>${tk ? `Free $${GATE_FEE} entry` : `Entry $${GATE_FEE}`}</b>")
RA("<button class=\"btn block pc-go\" id=\"gtGo\">${real ? `🎀 Play for real · $${GATE_FEE}` : '🎀 Lock in · free'}</button>",
   "<button class=\"btn block pc-go\" id=\"gtGo\">${tk ? `🎟️ Lock in · ${FREE_BET_COINS} 🟡` : real ? `🎀 Play for real · $${GATE_FEE}` : '🎀 Lock in · free'}</button>")
RA("if (real) { popClose(); payCash(GATE_FEE, 'A qualifier entry', () => gateResult(G, picks, true)); } else gateResult(G, picks, false); };",
   "if (tk) { if (!fqLeft() || (S.gems || 0) < FREE_BET_COINS) { popClose(); fqStart(); return; } fqClaim(); gateResult(G, picks, true, true); } else if (real) { popClose(); payCash(GATE_FEE, 'A qualifier entry', () => gateResult(G, picks, true)); } else gateResult(G, picks, false); };")
RA("function gateResult(G, picks, real) {", "function gateResult(G, picks, real, tk) {")
RA("${real ? `<button class=\"btn block pc-go\" id=\"gtAgain\">🎀 Next qualifier for real · $${GATE_FEE}</button>`",
   "${tk && fqLeft() && (S.gems || 0) >= FREE_BET_COINS ? `<button class=\"btn block pc-go\" id=\"gtTk\">🎟️ Another free $${GATE_FEE} qualifier · ${FREE_BET_COINS} 🟡</button><button class=\"btn block pc-real\" id=\"gtReal\">💵 Play for real · $${GATE_FEE} · win $${GATE_CASH[3]}</button>` : tk ? `<button class=\"btn block pc-real\" id=\"gtReal\">💵 Play for real · $${GATE_FEE} · win $${GATE_CASH[3]}</button>` : real ? `<button class=\"btn block pc-go\" id=\"gtAgain\">🎀 Next qualifier for real · $${GATE_FEE}</button>`")
RA("if ($('#gtReal')) $('#gtReal').onclick = () => gateOpen(true);", "if ($('#gtReal')) $('#gtReal').onclick = () => gateOpen(true); if ($('#gtTk')) $('#gtTk').onclick = () => fqStart();")

# coins menu row
RA("function raceBetRowHTML() { const g = ppGame(), e = (S.pp || {})[g.sl], ok = !e && (S.gems || 0) >= FREE_BET_COINS;",
   "function raceBetRowHTML() { const L = fqLeft(), ok = L && (S.gems || 0) >= FREE_BET_COINS;\n  return `<button class=\"ug-r ug-swap\" id=\"rbBet\"><span class=\"ug-i\">🎟️</span><span class=\"ug-t\"><b>Free $${GATE_FEE} qualifier</b><small>Pick the top 3 of 5 · 3 right win <b>$${GATE_CASH[3]}</b> cash · ${L ? `${L} of ${FQ_MAX} left this hour` : `next in ${frMinsLeft()} min`}</small></span><em class=\"${ok ? '' : 'need'}\">${FREE_BET_COINS} 🟡</em></button>`; }\nfunction raceBetRowOld() { const g = ppGame(), e = (S.pp || {})[g.sl], ok = !e && (S.gems || 0) >= FREE_BET_COINS;")
RA("if (e.target.closest('#rbBet')) { e.preventDefault(); e.stopPropagation(); try { closeSheet(); } catch (x) {} ppOpen(); }",
   "if (e.target.closest('#rbBet')) { e.preventDefault(); e.stopPropagation(); fqStart(); }")

# Vote screen bar
RA("const g = Math.floor(S.gems || 0), ok = g >= FREE_BET_COINS, pct = Math.min(100, Math.round(100 * g / FREE_BET_COINS));",
   "const g = Math.floor(S.gems || 0), L = fqLeft(), ok = L && g >= FREE_BET_COINS, pct = Math.min(100, Math.round(100 * g / FREE_BET_COINS));")
RA("<b>🎟️ ${ok ? 'Your free $1 Final entry is ready' : 'Free $1 Final entry'}</b><em>${ok ? 'Use it ›' : `${g} / ${FREE_BET_COINS} 🟡`}</em>",
   "<b>🎟️ ${ok ? 'Your free $1 qualifier is ready' : 'Free $1 qualifier · win $5'}</b><em>${!L ? `next in ${frMinsLeft()}m` : ok ? 'Play ›' : `${g} / ${FREE_BET_COINS} 🟡`}</em>")
RA("if ((S.gems || 0) >= FREE_BET_COINS) ppOpen(); else toast(`${isYoungW() ? 'Judge' : 'Vote'} and win free qualifiers to earn coins. ${FREE_BET_COINS - Math.floor(S.gems || 0)} 🟡 to go.`);",
   "fqStart();")

# Final pick screen: no coin entry any more, coin players enter for real
RA("`<button class=\"btn block pc-go\" id=\"ppFree\" ${n3 && freeOk ? '' : 'disabled'}>🎟️ Free $1 entry · ${FREE_BET_COINS} 🟡</button>\n        <button class=\"btn block pc-real\" id=\"ppReal\"",
   "`<button class=\"btn block pc-real\" id=\"ppReal\"")
RA("${freeOk ? '' : `<p class=\"pp-r\">You need ${(FREE_BET_COINS - Math.floor(S.gems || 0)).toLocaleString()} more 🟡 for the free entry. ${y ? 'Judge' : 'Vote'} to earn them.</p>`}", "")
open(d + 'yofi-real.html', 'w').write(s); print('rm v9 ok')
