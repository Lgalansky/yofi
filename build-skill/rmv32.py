# Real Money build, step 35 (after rmv31.py): Final picks pay by score group, not by rank.
#  Pickers' pool (78% of the prize pool) splits: 30 pts (exact 1-2-3) 25% · 20 pts 30% · 15 pts 45%.
#  Inside a group, money splits by pick size. An empty group's money moves down to the next group
#  (and if 15 is empty, up to the nearest group with players). Replaces the top-10% rule and the perfect-rosettes bonus.
import os, re
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

s = s.replace("function fcNotify() {", r"""const PP_TIERS = [{ pts: 30, w: 6, lab: 'Exact 1-2-3' }, { pts: 20, w: 2, lab: '20 points' }, { pts: 15, w: 1, lab: '15 points' }];
function ppTiers(e, g) { const r = cpRng(e.sl * 31 + 5), sc = ppScore(e.picks, g.ord), n = e.players || g.players, st = e.stake || 2, net = n * RACE_AVG * .78;
  const T = PP_TIERS.map(t => ({ ...t, n: 0, stake: 0 }));
  for (let i = 0; i < n - 1; i++) { const a = ppShuffle([...Array(RACE_N).keys()], r); if (r() < .45) { const w = a.indexOf(g.ord[0]); [a[0], a[w]] = [a[w], a[0]]; } const x = ppScore(a.slice(0, 3), g.ord), t = T.find(z => z.pts === x); if (t) { t.n++; t.stake += RACE_AVG; } }
  const mine = T.find(z => z.pts === sc); if (mine) { mine.n++; mine.stake += st; }
  const shares = T.reduce((a, t) => a + t.stake * t.w, 0) || 1; T.forEach(t => { t.amt = net * t.stake * t.w / shares; });
  const prize = mine ? +(net * st * mine.w / shares).toFixed(2) : 0;
  return { T, sc, n, st, net, prize, mine, winners: T.reduce((a, t) => a + t.n, 0) }; }
function fcNotify() {""", 1)

# result logic
RA("""  const rank = better + 1, paid = Math.max(3, Math.ceil(n * .1)), win = rank <= paid, net = n * RACE_AVG * .78, perfect = sc === 30;
  let prize = win ? +(net * st / ((paid - 1) * RACE_AVG + st)).toFixed(2) : 0; const jpWin = perfect ? +(jp / (1 + (e.sl % 2))).toFixed(2) : 0; prize = +(prize + jpWin).toFixed(2);""",
   """  const rank = better + 1, TR = ppTiers(e, g), net = TR.net, prize = TR.prize, jpWin = 0;""")
RA("""    <div class="rs-pool"><div><b>${money(n * RACE_AVG)}</b><small>prize pool</small></div><div><b>${money(net)}</b><small>shared by the top ${paid} pickers</small></div><div><b>${money(n * RACE_AVG * .1)}</b><small>to the 6 photo creators</small></div></div>
    <p class="rs-gap">${prize ? `You finished in the top ${paid}, so your share is <b>${amt}</b>.` : `Cash goes to the top ${paid}. You were <b>${rank - paid} place${rank - paid === 1 ? '' : 's'} off</b>.`}</p>""",
   """    <div class="rs-pool"><div><b>${money(n * RACE_AVG)}</b><small>prize pool</small></div><div><b>${TR.winners}</b><small>of ${n} pickers won cash</small></div><div><b>${money(n * RACE_AVG * .1)}</b><small>to the 6 photo creators</small></div></div>
    <div class="rs-tiers">${TR.T.map(t => `<div class="${TR.mine === t ? 'me' : ''}"><b>${t.lab}</b><span>${t.n} player${t.n === 1 ? '' : 's'} shared</span><em>${money(t.amt)}</em></div>`).join('')}</div>
    <p class="rs-gap">${prize ? `You scored ${sc}: <b>${TR.mine.n} players</b> in your group shared ${money(TR.mine.amt)} by pick size and score, so you won <b>${amt}</b> (${(prize / st).toFixed(1)}× your pick).` : `15 points or more wins cash. You scored <b>${sc}</b>${sc === 10 ? ': one more photo in the top 3 would have paid' : ''}.`}</p>""")
RA("<p class=\"pp-m\"><b>${sc} points</b> · ${ppOrd(rank)} of ${n} · ${e.free ? 'free pick' : `${money(st)} pick`}</p>",
   "<p class=\"pp-m\"><b>${sc} points</b> · ${e.free ? 'free pick' : `${money(st)} pick`}</p>")
# pick screen + finalists card wording
RA("Top 10% share 78% of the pool by pick size · 10% to the finalists’ creators · 12% PhotoPicks.",
   "Score 15+ to win: the pickers’ 78% is shared by everyone on 15+, by pick size, and 20 points pays 2× and an exact 1-2-3 pays 6× what 15 points pays per $ · 10% to the finalists’ creators · 12% PhotoPicks.")
RA('<p class="rc-jp">🎀 Perfect rosettes bonus · <b>$${jp.toLocaleString()}</b></p>', '<p class="rc-jp">🎯 Score 15+ to win cash · an exact 1-2-3 pays <b>6×</b></p>')
RA('<p class="rc-jp">🎀 Perfect rosettes bonus · <b>$${raceJP(cur).toLocaleString()}</b></p>', '<p class="rc-jp">🎯 Score 15+ to win cash · an exact 1-2-3 pays <b>6×</b></p>')
s = s.replace('</style>', """.rs-tiers{margin:4px 0 6px;text-align:left}.rs-tiers div{display:grid;grid-template-columns:1fr auto auto;gap:8px;align-items:baseline;padding:6px 10px;border-radius:10px}.rs-tiers div+div{margin-top:3px}.rs-tiers b{font-size:.88rem}.rs-tiers span{font-size:.78rem;opacity:.8}.rs-tiers em{font-style:normal;font-weight:900;color:#2F6B3F}
.rs-tiers div.me{background:#E6F0DF;box-shadow:inset 0 0 0 1.5px #2F6B3F}html.yg .rs-tiers div.me{background:#10301F;box-shadow:inset 0 0 0 1.5px #21C77A}html.yg .rs-tiers em{color:#21C77A}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v32 ok')
