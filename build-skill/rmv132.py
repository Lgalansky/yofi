# Real Money build, step 135 (after rmv131.py): Winner odds are locked when you pick.
#  Before: the live page showed "5.6× now" but the pick settled at the odds at close (e.g. 3.7×), so a win could pay a
#  third less than the screen promised. Now the odds shown when you pick are the odds you're paid at.
#  - Pick screen: "Sunset smile at 3.4×: a $2.00 pick pays $6.80 if it wins · odds locked when you pick";
#    button "Pays $6.80 if it wins" (no "about").
#  - Live Winner page and "Your picks in this Final": "locked at 5.6× · pays $11.20".
#  - Settlement (own reveal or combined with Top 3) uses the locked odds. Older picks without a stored price
#    fall back to the closing odds.
#  - Rules line explains it. Board odds still move for new pickers.
#  Simulated: in a real product fixed odds put the house at risk on long shots; would need limits per photo.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("function winLive(w) { const g = ppGame(w.sl), od = winOdds(g)[w.pick],", "function winLive(w) { const g = ppGame(w.sl), od = w.odds || winOdds(g)[w.pick],")
RA("${w.free ? 'Free pick' : money(w.stake)} · now ${od}×</em>", "${w.free ? 'Free pick' : money(w.stake)} · locked at ${od}× · pays ${money((w.stake || 2) * od)}</em>")
RA("if (W) { const r = rank[W.pick], od = winOdds(g)[W.pick];", "if (W) { const r = rank[W.pick], od = W.odds || winOdds(g)[W.pick];")
RA("${W.free ? 'Free pick' : money(W.stake || 2)} · ${od}× now</small>", "${W.free ? 'Free pick' : money(W.stake || 2)} · locked at ${od}× · pays ${money((W.stake || 2) * od)}</small>")
RA("const g = ppGame(w.sl), od = winOdds(g, (w.sl + 1) * PP_MS - 1)[w.pick], won = g.ord[0] === w.pick,", "const g = ppGame(w.sl), od = w.odds || winOdds(g, (w.sl + 1) * PP_MS - 1)[w.pick], won = g.ord[0] === w.pick,")
RA("function winSettle(w) { const g = ppGame(w.sl), od = winOdds(g, (w.sl + 1) * PP_MS - 1)[w.pick],", "function winSettle(w) { const g = ppGame(w.sl), od = w.odds || winOdds(g, (w.sl + 1) * PP_MS - 1)[w.pick],")
RA("a ${money(stake)} pick returns about <b>${money(stake * od[pick])}</b>`", "a ${money(stake)} pick pays <b>${money(stake * od[pick])}</b> if it wins<br><small class=\"wp-lock\">🔒 Odds locked when you pick</small>`")
RA("Pays about ${money(stake * od[pick])} if it wins", "Pays ${money(stake * od[pick])} if it wins")
RA("Winner pickers share 78% of the winner pool, in proportion to their pick. Odds move as picks come in and are fixed when picks close.",
   "Your odds are locked when you pick: if your photo wins, you're paid exactly what's shown. Odds on the board keep moving for new picks.")
s = s.replace('</style>', """html body .ppop .wp-lock{display:inline-block;margin-top:3px;font-weight:800;color:#2F6B3F}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v132 ok')
