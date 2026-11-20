# Real Money build, step 204 (after rmv200.py): coin entry is one per player; Bonus Cash works as promised.
#  Coin entry (owner chose option A):
#   - ONE free Final entry per player, ever, for 250 coins, and it needs an account (guests are asked to sign up).
#     Lobby button: "🪙 Your first Final free · 250 coins". Once used it disappears everywhere.
#   - "Race again free · coins" on results is gone. The coins sheet shows the offer only until it's used.
#  Bonus Cash:
#   - Spent FIRST on entries, then real cash for any remainder ("🎁 $2.00 Bonus Cash used").
#   - Kept separate from real cash (no longer merged into cash on reload). Winnings are always real cash.
#   - Shown beside the cash balance ("+ $10.00 bonus") and in the Final lobby ("You have $5.00 + $10.00 Bonus Cash").
#   - Not withdrawable (stated where it's offered). There is no withdrawal screen in the prototype yet.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
# coin entry: once per player, account required
RA("const go = document.getElementById('qfpGo'); if (!go) return r; const g = Math.floor(S.gems || 0);", "const go = document.getElementById('qfpGo'); if (!go || S.coinFin) return r; const g = Math.floor(S.gems || 0);")
RA("🪙 Enter free with ${FIN_COINS} coins<small>a $2 entry · 1st wins ${money(2 * QF_PAY[0])} cash</small>", "🪙 Your first Final free · ${FIN_COINS} coins<small>one free $2 entry per player · 1st wins ${money(2 * QF_PAY[0])} cash</small>")
RA("if ((S.gems || 0) < FIN_COINS) return; S.gems -= FIN_COINS; save();", "if ((S.gems || 0) < FIN_COINS) return; if (S.user && S.user.guest) { popClose(); openSignup(() => setTimeout(() => qfPick(p, 2), 250), { locked: false, photo: 1 }); return; } S.gems -= FIN_COINS; S.coinFin = 1; save();")
RA("more coins</b> for a free $2 entry<span>", "more coins</b> for your one free $2 entry<span>")
RA("(S.gems || 0) >= FIN_COINS ? `<button class=\"btn block db-go rm-coin\" id=\"qrC\">", "false ? `<button class=\"btn block db-go rm-coin\" id=\"qrC\">")
RA("const per = document.querySelector('.t2 .t2-per'), g = Math.floor(S.gems || 0); if (per) per.insertAdjacentHTML", "const per = document.querySelector('.t2 .t2-per'), g = Math.floor(S.gems || 0); if (per && !S.coinFin) per.insertAdjacentHTML")
RA("<b>🎟️ ${FIN_COINS} coins = a free $2 Final entry</b>", "<b>🎟️ Your first Final free: ${FIN_COINS} coins</b>")
RA("'You have enough: use it when you enter a Final.' : `${FIN_COINS - g} more coins to go. Use it in the Final lobby.`", "'One per player. You have enough: use it when you enter a Final.' : `One per player. ${FIN_COINS - g} more coins to go.`")
# bonus cash
RA("if (S.bonus) { S.cash = +((S.cash || 0) + S.bonus).toFixed(2); S.bonus = 0; }", "")
RA("<p class=\"nv-sim\">You have ${money(S.cash || 0)} · demo: other finalists simulated</p>", "<p class=\"nv-sim\">You have ${money(S.cash || 0)}${(S.bonus || 0) > 0 ? ` + ${money(S.bonus)} Bonus Cash` : ''} · demo: other finalists simulated</p>")
s = s.replace("function fcNotify() {", r"""function payCash(amt, what, then) {
  if (S.user && S.user.guest) { openSignup(() => payCash(amt, what, then), { locked: false, real: 1 }); return false; }
  const tot = () => +((S.cash || 0) + (S.bonus || 0)).toFixed(2);
  const take = () => { const b = Math.min(S.bonus || 0, amt), c = +(amt - b).toFixed(2); S.bonus = +((S.bonus || 0) - b).toFixed(2); S.cash = +((S.cash || 0) - c).toFixed(2); try { goCash(); } catch (e) {} save(); paintWallet();
    if (b > 0) toast(`🎁 ${money(b)} Bonus Cash used${c > 0 ? ` · ${money(c)} cash` : ''}`); then(); };
  if (tot() < amt) { openStore(`${what} costs ${money(amt)}.`, () => { if (tot() >= amt) take(); }); return false; }
  take(); return true; }
(() => { const pw = paintWallet; paintWallet = function () { const r = pw.apply(this, arguments); try { const w = document.getElementById('wCash'); if (!w) return r; let t = document.getElementById('bnTag'); const b = S.bonus || 0;
  if (b > 0) { if (!t) { t = document.createElement('small'); t.id = 'bnTag'; const n = document.getElementById('cashNum'); n.insertAdjacentElement('afterend', t); } t.textContent = `+ ${money(b)} bonus`; } else if (t) t.remove(); } catch (e) {} return r; }; })();
setTimeout(() => { try { paintWallet(); } catch (e) {} }, 800);
function fcNotify() {""", 1)
s = s.replace('</style>', """#bnTag{margin-left:6px;padding:2px 7px;border-radius:999px;background:#FFF1C9;color:#9A6B12;font:800 .66rem Nunito,system-ui;white-space:nowrap}
</style>""", 1)
s = s.replace("cash to play · plus $10 Bonus Cash for entries", "cash to play · plus $10 Bonus Cash, spent first on entries · can’t be withdrawn")
open(d + 'yofi-real.html', 'w').write(s); print('rm v201 ok')
# pass 2: retire the older payCash defined later in the file so the Bonus-Cash-first version is the one used
s = open(d + 'yofi-real.html').read()
RA("function payCash(amt, what, then) {\n  if (S.user && S.user.guest) { openSignup(() => payCash(amt, what, then), { locked: false, real: 1 }); return false; }\n  if (amt === 1 &&",
   "function payCashOld(amt, what, then) {\n  if (S.user && S.user.guest) { openSignup(() => payCash(amt, what, then), { locked: false, real: 1 }); return false; }\n  if (amt === 1 &&")
open(d + 'yofi-real.html', 'w').write(s); print('rm v201 pass2 ok')
# pass 3: bonus tag sits as a small badge on the bottom edge of the cash pill (always visible)
s = open(d + 'yofi-real.html').read()
s = s.replace('</style>', """html body #wCash{position:relative;overflow:visible!important}html body #wCash #bnTag{display:block!important;position:absolute;left:50%;bottom:-13px;transform:translateX(-50%);margin:0;padding:0 8px;background:#FFF1C9;color:#9A6B12;box-shadow:0 0 0 1.5px #D9AE4F;font:800 .56rem/1.55 Nunito,system-ui;z-index:2}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v201 pass3 ok')
