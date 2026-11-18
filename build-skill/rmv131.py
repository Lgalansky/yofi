# Real Money build, step 134 (after rmv130.py): result bugs from a Final + Coin Pick run-through.
#  1. Top 3 and Winner picks on the same Final played two reveals ("Counting the votes…" twice) and the second one
#     closed the Top 3 result page. Now one reveal settles both: the box shows the total won with a line for each
#     pick ("🎯 Top 3 +$2.41" / "🏆 Winner pick · Adventure pup finished 2nd · no cash"). The Winner pick waits for
#     the Top 3 result instead of racing it. A Winner pick on its own keeps its own reveal.
#  2. Coin Pick: the page after the reveal repeated the "Spot on!" headline. It now says what's next:
#     "+10 coins in your balance" / "No coins this round".
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("function ppResult(e) { if (rvBusy(e)) return; e.__rv = Date.now(); const g = ppGame(e.sl), TR = ppTiers(e, g), prize = TR.prize;",
   "function ppResult(e) { if (rvBusy(e)) return; e.__rv = Date.now(); const g = ppGame(e.sl), TR = ppTiers(e, g), prize = TR.prize, W = (S.pw || {})[e.sl], wx = W && !W.done ? winSettle(W) : null, tot = +(prize + (wx ? wx.prize : 0)).toFixed(2);")
RA("res: { won: !!prize, amt: money(prize), txt: prize ? `You won ${money(prize)}` : 'No cash · you need 2 in the top 3, 1 exact' }",
   "res: { won: !!tot, amt: money(tot), txt: tot ? `You won ${money(tot)}` : 'No cash · you need 2 in the top 3, 1 exact' }, extra: wx ? `<div class=\"rv-wx\"><p class=\"${prize ? 'ok' : ''}\"><span>🎯 Top 3 pick</span><b>${prize ? '+' + money(prize) : 'no cash'}</b></p><p class=\"${wx.prize ? 'ok' : ''}\"><span>🏆 Winner pick · “${esc(wx.t)}”</span><b>${wx.prize ? `+${money(wx.prize)} at ${wx.od}×` : `finished ${ppOrd(wx.pl)} · no cash`}</b></p></div>` : ''")
RA('<p class="rv-pool">${title}</p>`', '${o.extra || \'\'}<p class="rv-pool">${title}</p>`', 2)
RA("const e = Object.values(S.pw).find(x => !x.done && Date.now() >= ppDue(x) && !rvBusy(x));",
   "const e = Object.values(S.pw).find(x => !x.done && Date.now() >= ppDue(x) && !rvBusy(x) && !((S.pp || {})[x.sl] && !(S.pp || {})[x.sl].done));")
RA("<h2 class=\"g2-h gq-h\">${pay ? 'Spot on!' : 'Not this time'}</h2>", "<h2 class=\"g2-h gq-h\">${pay ? `+${pay} coins in your balance` : 'No coins this round'}</h2>")
s = s.replace("function fcNotify() {", r"""function winSettle(w) { const g = ppGame(w.sl), od = winOdds(g, (w.sl + 1) * PP_MS - 1)[w.pick], st = w.stake || 2, prize = g.ord[0] === w.pick ? +(st * od).toFixed(2) : 0;
  w.__rv = Date.now(); w.done = 1; w.prize = prize; w.odds = od; if (prize) { S.cash = +((S.cash || 0) + prize).toFixed(2); paintWallet(); } save();
  return { prize, od, t: g.ph[w.pick].t, pl: g.ord.indexOf(w.pick) + 1 }; }
function fcNotify() {""", 1)
s = s.replace('</style>', """.rv-wx{margin:8px 0 2px;display:grid;gap:5px}.rv-wx p{margin:0;display:flex;justify-content:space-between;gap:8px;padding:7px 11px;border-radius:10px;background:#fff;box-shadow:inset 0 0 0 1.5px #EADCC6;font-size:.86rem;text-align:left}
.rv-wx p b{white-space:nowrap;color:#5B4A3F}.rv-wx p.ok{box-shadow:inset 0 0 0 2px #2F6B3F;background:#F1F6EC}.rv-wx p.ok b{color:#2F6B3F}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v131 ok')
#  3. "3 of your photos in the top 3" (reveal + result page) meant your picks, not photos you made: now "picks".
#  4. Final result page also states the Winner pick's outcome next to the Top 3 cash line.
s = open(d + 'yofi-real.html').read()
n = s.count('of your photos in the top 3'); assert n >= 2, n
s = s.replace('of your photos in the top 3', 'of your picks in the top 3')
RA("<b>Cash won: ${amt}</b> · ${e.free ? 'Free pick' : `${money(st)} pick`}</p>",
   "<b>Cash won: ${amt}</b> · ${e.free ? 'Free pick' : `${money(st)} pick`}${(S.pw || {})[g.sl] && S.pw[g.sl].done ? ` · 🏆 Winner pick: ${S.pw[g.sl].prize ? '+' + money(S.pw[g.sl].prize) : 'no cash'}` : ''}</p>")
open(d + 'yofi-real.html', 'w').write(s); print('rm v131 pass2 ok')
