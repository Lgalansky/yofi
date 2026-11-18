# Real Money build, step 83 (after rmv79.py): payouts rebalanced so every win pays more than the pick.
#  Before: ~81% "won", but 1 exact paid ~0.6x and 2-in-top-3 ~0.37x (losses shown as wins).
#  Now: you win with 2 photos in the top 3, at least 1 in its exact spot (~45% of pickers, simulated field):
#    3 correct ~5.8x · 2 correct ~2x · 1 correct + another in the top 3 ~1.1x. Pickers still share 78% of the pool.
#  Every place that states the rule is updated; the payout table uses the tier labels; near-miss chip explains the rule.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("const PP_TIERS = [{ k: 3, w: 10, lab: '3 correct' }, { k: 2, w: 2.5, lab: '2 correct' }, { k: 1, w: 1, lab: '1 correct' }, { k: 'o', w: 1.2, lab: 'All 3 in the top 3, other order' }, { k: 'p2', w: .6, lab: '2 in the top 3' }];",
   "const PP_TIERS = [{ k: 3, w: 5.3, lab: '3 correct' }, { k: 2, w: 1.8, lab: '2 correct' }, { k: 1, w: 1, lab: '1 correct + another in the top 3' }];")
RA("const t = p.filter(x => top.includes(x)).length; return e || (t === 3 ? 'o' : t === 2 ? 'p2' : 0); };",
   "const t = p.filter(x => top.includes(x)).length; return e >= 2 ? e : e === 1 && t >= 2 ? 1 : 0; };")
R = 'Win with 2 photos in the top 3, at least 1 in its exact spot'
RA("Get 1 photo in its exact spot, or 2 in the top 3, to win a share of the prize pool.", "Win with 2 photos in the top 3, at least 1 in its exact spot. Every win pays more than your pick.")
RA("get 1 photo in its exact spot, or 2 in the top 3, to win.", "win with 2 photos in the top 3, at least 1 in its exact spot. Every win pays more than your pick.")
RA("🎯 Win with 1 photo in its exact spot, or 2 in the top 3</p>", f"🎯 {R}</p>")
RA("🎯 Win with 1 in its exact spot or 2 in the top 3</p>", f"🎯 {R}</p>")
RA("win with 1 photo in its exact spot, or 2 in the top 3.", "win with 2 photos in the top 3, at least 1 in its exact spot. Every win pays more than your pick.")
RA("${t.k === 'p2' ? '2 in the top 3, any order' : t.k === 'o' ? 'Top 3, different order' : `${t.k} exact position${t.k === 1 ? '' : 's'}`}", "${t.lab}")
RA("'Needs 1 pick in its exact spot'", "'Needs 2 in the top 3, 1 in its exact spot'")
RA("const chip = !prize && inT === 1 ? `So close! One more photo in the top 3 would have paid about ${money(nearAmt)}`",
   "const chip = !prize && (inT || ex) ? `So close! 2 in the top 3 with 1 in its exact spot would have paid about ${money(nearAmt)}`")
open(d + 'yofi-real.html', 'w').write(s); print('rm v80 ok')
# floor: the lowest winning tier always pays at least 1.1x; the higher tiers share the rest of the pickers' pool
s = open(d + 'yofi-real.html').read()
RA("const ppCat = (p, ord) =>", """const PP_FLOOR = 1.1;
function ppUnits(T, net) { const W = T.reduce((a, t) => a + t.stake * t.w, 0) || 1; T.forEach(t => { t.x = net * t.w / W; });
  const lo = T.find(t => t.k === 1); if (lo && lo.x < PP_FLOOR) { lo.x = PP_FLOOR; const rest = Math.max(0, net - PP_FLOOR * lo.stake), W2 = T.filter(t => t !== lo).reduce((a, t) => a + t.stake * t.w, 0) || 1; T.forEach(t => { if (t !== lo) t.x = Math.max(PP_FLOOR, rest * t.w / W2); }); }
  T.forEach(t => { t.amt = t.x * t.stake; }); return T; }
const ppCat = (p, ord) =>""")
RA("const shares = T.reduce((a, t) => a + t.stake * t.w, 0) || 1; T.forEach(t => { t.amt = net * t.stake * t.w / shares; });", "ppUnits(T, net);")
RA("const prize = mine ? +(net * st * mine.w / shares).toFixed(2) : 0;", "const prize = mine ? +(st * mine.x).toFixed(2) : 0;")
RA("function ppPaysHTML(g) { const n = g.players, T = ppField(g, g.sl, n + 1), shares = T.reduce((a, t) => a + t.stake * t.w, 0) || 1, net = n * RACE_AVG * .78;",
   "function ppPaysHTML(g) { const n = g.players, T = ppField(g, g.sl, n + 1), net = n * RACE_AVG * .78; ppUnits(T, net);")
RA("pays about ${(net * t.w / shares).toFixed(1)}×", "pays about ${t.x.toFixed(1)}×")
open(d + 'yofi-real.html', 'w').write(s); print('rm v80 floor ok')
# reveal on a loss: no "Your 1st pick finished 1st." (sounds like a win); say what was needed
s = open(d + 'yofi-real.html').read()
RA(": w1 && ex === 1 ? 'Your 1st pick finished 1st.'", ": won && w1 && ex === 1 ? 'Your 1st pick finished 1st.'")
RA("txt: prize ? `You won ${money(prize)}` : 'No cash this time'", "txt: prize ? `You won ${money(prize)}` : 'No cash · you need 2 in the top 3, 1 exact'")
open(d + 'yofi-real.html', 'w').write(s); print('rm v80 loss copy ok')
