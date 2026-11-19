# Real Money build, step 142 (after rmv138.py): newbie run-through quick fixes.
#  1. No age form on arrival: the game shows first. Age is asked (once) right before anything with cash: the free real
#     game, a cash entry, the deposit offer, or tapping the cash balance.
#  2. The account screen for the free real game says what it is: "Your free $1 game is waiting · real-cash games are
#     for adults 18+" — no coins bonus, no "save your photo".
#  3. Real-only switches on at the first deposit, not at the free real game. A player who takes the free game but
#     doesn't deposit keeps coin games; their results offer "Add cash to play again" with the Bonus Cash offer.
#  6. Coin players' header: coins and streak only (no $0.00 cash pill or "18+ · Real money" pill until they go real).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
# 1. no age form on load; with no age given, the look is Fall Fair (not the 18–24 dark look)
RA("setTimeout(ageGate, 0);", "")
RA("const isYoung = () => S && (!S.ageBr || S.ageBr === '18 to 24');", "const isYoung = () => S && S.ageBr === '18 to 24';")
# 2. account screen for cash
RA("openSignup(() => payCash(amt, what, then), { locked: false, pick: /pick/i.test(what) })", "openSignup(() => payCash(amt, what, then), { locked: false, real: 1 })")
RA("<h2>${opts.bonus ? 'Claim your welcome bonus'", "<h2>${opts.real ? ((S.cashTix || 0) > 0 ? 'Your free $1 game is waiting' : 'Create your account to play for cash') : opts.bonus ? 'Claim your welcome bonus'")
RA("${opts.bonus || !S.giftEn ? `<div class=\"wbx\">", "${!opts.real && (opts.bonus || !S.giftEn) ? `<div class=\"wbx\">")
RA("<p class=\"sub\">${opts.pick ? 'Your picks and any winnings are saved to your account. '", "<p class=\"sub\">${opts.real ? 'Real-cash games are for adults 18+. Your winnings are saved to your account. ' : opts.pick ? 'Your picks and any winnings are saved to your account. '")
RA("Create your account so nothing gets lost.</p>", "${opts.real ? '' : 'Create your account so nothing gets lost.'}</p>")
# 3. real-only at first deposit
RA("S.cashTix = (S.cashTix || 0) + 1; S.frGiven = 1; S.cashMode = 1; save();", "S.cashTix = (S.cashTix || 0) + 1; S.frGiven = 1; save();")
RA("setTimeout(() => { gmOpen('match', 1); setTimeout(() => { const b = document.getElementById('dbGo'); b && b.click(); }, 80); }, 250); }",
   "setTimeout(() => { window.__forceReal = 1; gmOpen('match', 1); setTimeout(() => { const b = document.getElementById('dbGo'); b && b.click(); }, 80); }, 250); }")
RA("const gmTiers = () => isCash() ? GM_R : GM_C;", "const gmTiers = () => { const r = isCash() || window.__forceReal; window.__forceReal = 0; return r ? GM_R : GM_C; };")
RA("function gmFreeRealHTML() { return !isCash() ?", "function gmFreeRealHTML() { return !isCash() && !S.frGiven ?")
RA("() => { if (!S.bonusGot) { S.bonusGot = 1; S.bonus = +((S.bonus || 0) + 10).toFixed(2); save(); toast('🎁 $10 Bonus Cash added · used first on entries'); } }",
   "() => { S.cashMode = 1; if (!S.bonusGot) { S.bonusGot = 1; S.bonus = +((S.bonus || 0) + 10).toFixed(2); } save(); toast('🎁 $10 Bonus Cash added · used first on entries'); try { paintWallet(); } catch (e) {} }")
RA("() => { if (w && !S.bonusGot) { S.bonusGot = 1;", "() => { S.cashMode = 1; save(); if (w && !S.bonusGot) { S.bonusGot = 1;")
RA("<button class=\"btn block db-go ${t.coins ? '' : 'cashb'}\" id=\"dbRe\">🔁 Rematch · ${gmAmt(t, t.fee)}</button>${up !== ti ? `<button class=\"btn block quiet db-up\" id=\"dbUp\">Step up · ${gmAmt(T[up], T[up].fee)}</button>` : ''}\n    <div style=\"text-align:center\"><button class=\"link pc-later\" id=\"dbOther\">",
   "${!t.coins && !isCash() ? `<button class=\"btn block db-go cashb\" id=\"dbAdd\">💵 Add cash to play again${S.bonusGot ? '' : ' · get $10 Bonus Cash'}</button><button class=\"btn block quiet db-up\" id=\"dbBack\">Back to coin games</button>` : `<button class=\"btn block db-go ${t.coins ? '' : 'cashb'}\" id=\"dbRe\">🔁 Rematch · ${gmAmt(t, t.fee)}</button>${up !== ti ? `<button class=\"btn block quiet db-up\" id=\"dbUp\">Step up · ${gmAmt(T[up], T[up].fee)}</button>` : ''}`}\n    <div style=\"text-align:center\"><button class=\"link pc-later\" id=\"dbOther\">")
RA("$('#dbRe').onclick = () => { popClose(); setTimeout(() => { if (!sameMode)", "if ($('#dbAdd')) { $('#dbAdd').onclick = depositOffer; $('#dbBack').onclick = () => { popClose(); setTimeout(gmHub, 200); }; }\n  if ($('#dbRe')) $('#dbRe').onclick = () => { popClose(); setTimeout(() => { if (!sameMode)")
RA("const dep = firstReal && !S.bonusGot ? `<button class=\"gmdep\"", "const dep = firstReal && !S.bonusGot && isCash() ? `<button class=\"gmdep\"")
# age right before cash
s = s.replace("function fcNotify() {", r"""function needAge(then) { if (S.obDone && S.ageBr) { then(); return; } try { popClose(); closeSheet(); } catch (e) {} ageGate(); const w = setInterval(() => { if (!document.querySelector('#ageGate.on')) { clearInterval(w); if (S.ageBr) setTimeout(then, 200); } }, 250); }
(() => { const fr = freeRealStart, dep = depositOffer, pe = gmPayEntry;
  freeRealStart = function () { needAge(fr); }; depositOffer = function () { needAge(dep); };
  gmPayEntry = function (t, mode, go) { if (t.coins) return pe(t, mode, go); needAge(() => pe(t, mode, go)); }; })();
document.addEventListener('click', e => { if (e.target.closest && e.target.closest('#wCash') && !(S.obDone && S.ageBr)) { e.preventDefault(); e.stopPropagation(); needAge(() => { try { openStore('Add cash to play'); } catch (x) {} }); } }, true);
setInterval(() => { try { document.documentElement.classList.toggle('coinp', !!S && !isCash() && !((S.cash || 0) > 0)); } catch (e) {} }, 500);
function fcNotify() {""", 1)
s = s.replace('</style>', """html.coinp #wCash,html.coinp .rm-pill{display:none!important}
html.coinp .wallet{grid-template-columns:1fr!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v139 ok')
