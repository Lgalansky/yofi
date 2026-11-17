# Real Money build, step 37 (after rmv33.py): simple Final pick payouts, no points.
#  "Correct" = the right photo in the right place.
#  3 correct (exact 1-2-3) · 2 correct · 1 correct · all 3 in the top 3 but wrong order. Each pays a share of the pickers' pool
#  (78%), weighted 10 / 2.5 / 1 / 1.2 per $ picked. The pick screen shows "pays about N×" for each, estimated from this Final.
import os, re
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

m = re.findall(r"const PP_TIERS = \[.*?\n  return \{ T, sc, n, st, net, prize, mine, winners: T\.reduce\(\(a, t\) => a \+ t\.n, 0\) \}; \}\n", s, flags=re.S); assert len(m) == 1, len(m)
s = s.replace(m[0], r"""const PP_TIERS = [{ k: 3, w: 10, lab: '3 correct' }, { k: 2, w: 2.5, lab: '2 correct' }, { k: 1, w: 1, lab: '1 correct' }, { k: 'o', w: 1.2, lab: 'All 3 in the top 3, other order' }];
const ppCat = (p, ord) => { const top = ord.slice(0, 3), e = p.filter((x, i) => top[i] === x).length; return e || (p.every(x => top.includes(x)) ? 'o' : 0); };
function ppField(g, sl, n) { const r = cpRng(sl * 31 + 5), T = PP_TIERS.map(t => ({ ...t, n: 0, stake: 0 }));
  for (let i = 0; i < n - 1; i++) { const a = ppShuffle([...Array(RACE_N).keys()], r); if (r() < .45) { const w = a.indexOf(g.ord[0]); [a[0], a[w]] = [a[w], a[0]]; } const t = T.find(z => z.k === ppCat(a.slice(0, 3), g.ord)); if (t) { t.n++; t.stake += RACE_AVG; } }
  return T; }
function ppTiers(e, g) { const n = e.players || g.players, st = e.stake || 2, net = n * RACE_AVG * .78, c = ppCat(e.picks, g.ord), sc = ppScore(e.picks, g.ord), T = ppField(g, e.sl, n);
  const mine = T.find(z => z.k === c); if (mine) { mine.n++; mine.stake += st; }
  const shares = T.reduce((a, t) => a + t.stake * t.w, 0) || 1; T.forEach(t => { t.amt = net * t.stake * t.w / shares; });
  const prize = mine ? +(net * st * mine.w / shares).toFixed(2) : 0;
  return { T, sc, c, n, st, net, prize, mine, winners: T.reduce((a, t) => a + t.n, 0) }; }
function ppPaysHTML(g) { const n = g.players, T = ppField(g, g.sl, n + 1), shares = T.reduce((a, t) => a + t.stake * t.w, 0) || 1, net = n * RACE_AVG * .78;
  return `<div class="pp-pays"><b class="pp-pays-h">What pays</b>${T.map(t => `<div><span>${t.lab}</span><em>pays about ${(net * t.w / shares).toFixed(1)}×</em></div>`).join('')}<small>“Correct” = the right photo in the right place. Pays come from the prize pool, so they move a little as players join.</small></div>`; }
""")

# pick screen: replace the points rules with the pays table
m = re.findall(r'<p class="pp-r">10 pts for each photo in the right place.*?decide\.</p>', s, flags=re.S); assert len(m) == 1, len(m)
s = s.replace(m[0], '${ppPaysHTML(g)}<p class="pp-r">10% of the pool goes to the finalists’ creators · 12% to PhotoPicks. ${y ? \'Judges\' : \'Voters\'} decide the result.</p>')
RA('🎯 Score 15+ to win cash · an exact 1-2-3 pays <b>6×</b>', '🎯 Get 1 or more in the right place to win cash', 2)
RA('Score 15+ to win a share of the prize pool.', 'Get 1 or more in the right place to win a share of the prize pool.')

# result screen
RA("<p class=\"pp-m\"><b>${sc} points</b> · ${e.free ? 'free pick' : `${money(st)} pick`}</p>",
   "<p class=\"pp-m\"><b>${TR.mine ? TR.mine.lab : 'None in the right place'}</b> · ${e.free ? 'free pick' : `${money(st)} pick`}</p>")
m = re.findall(r'<p class="rs-gap">\$\{prize \? `You scored \$\{sc\}.*?\.`\}</p>', s, flags=re.S); assert len(m) == 1, len(m)
s = s.replace(m[0], "<p class=\"rs-gap\">${prize ? `You got <b>${TR.mine.lab.toLowerCase()}</b>: ${TR.mine.n} players shared ${money(TR.mine.amt)} by pick size, so you won <b>${amt}</b> (${(prize / st).toFixed(1)}× your pick).` : `Get at least 1 photo in its right place to win cash.`}</p>")
s = s.replace('</style>', """.pp-pays{text-align:left;border-radius:14px;padding:10px 12px;margin:8px 0;background:rgba(127,127,127,.08)}.pp-pays-h{display:block;font-size:.74rem;letter-spacing:.08em;text-transform:uppercase;opacity:.8;margin-bottom:4px}
.pp-pays div{display:flex;justify-content:space-between;gap:8px;padding:5px 0;border-top:1px solid rgba(127,127,127,.18);font-size:.92rem}.pp-pays div:first-of-type{border-top:0}.pp-pays em{font-style:normal;font-weight:900;color:#2F6B3F;white-space:nowrap}html.yg .pp-pays em{color:#21C77A}.pp-pays small{display:block;font-size:.72rem;opacity:.8;margin-top:4px}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v34 ok')
