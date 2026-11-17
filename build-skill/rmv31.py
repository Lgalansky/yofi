# Real Money build, step 34 (after rmv30.py): all Final prize money comes from the pool.
#  - No fixed $10 / $5 / $2 for the top 3 photos. Creators get only their pool share (10% split by place).
#  - Final result screen: pool breakdown (pool, shared by top N pickers, to the 6 creators) and how far you were from cash.
#  - Creator wording everywhere: "Finalists' creators share 10% of the prize pool".
import os, re
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

RA("const RACE_OWN = { cash: [10, 5, 2], gems: [300, 150, 50] }", "const RACE_OWN = { cash: [0, 0, 0], gems: [0, 0, 0] }")
RA("const ownTxt = c => c ? '$10 · $5 · $2' : '300 · 150 · 50 🟡';", "const ownTxt = c => 'a share of the prize pool';")
CR = "Finalists’ creators share <b>10% of the prize pool</b>"
for a, b in [
    ("and its top 3 photos win <b>$10 · $5 · $2</b>.", "and its finalists’ creators share <b>10% of the prize pool</b>."),
    ("`Top 3 photos win <b>${ownTxt(true)}</b>. Exhibitors can’t pick in their own show.`", "`" + CR + ". Creators can’t pick in a Final their own photo is in.`"),
    ("The Final’s top 3 win <b>${ownTxt(true)}</b><br>Photos need", CR + "<br>Photos need"),
    ("Its top 3 win <b>${ownTxt(true)}</b>.</p>", CR + ".</p>"),
    ("Final</b>. Top 3 win <b>${ownTxt(true)}</b>.<br>", "Final</b>. " + CR + ".<br>"),
    ("and the Final’s 🥇🥈🥉 win $10 · $5 · $2` }", "and finalists’ creators share 10% of the prize pool` }"),
    ("The Final’s 🥇🥈🥉 win <b>$10 · $5 · $2</b> real cash. Every finalist’s creator shares <b>10% of the Final pool</b>.", "Every finalist’s creator shares <b>10% of the Final’s prize pool</b>: 1st 4% · 2nd 2.5% · 3rd 1.5% · 4th–6th share 2%."),
    ("Qualifiers, then the hourly Final · top 3 win $10 · $5 · $2", "Qualifiers, then the hourly Final · finalists share 10% of the pool"),
    ("every finalist’s creator shares 10% of the Final pool, and the top 3 also win $10 · $5 · $2.", "every finalist’s creator shares 10% of the Final’s prize pool."),
    ("Every finalist’s creator shares <b>10% of the prize pool</b>, and the top 3 win <b>$10 · $5 · $2</b>.", "Every finalist’s creator shares <b>10% of the prize pool</b>, and 1st place gets the biggest share."),
]:
    assert a in s, a; s = s.replace(a, b)

# Final result screen
m = re.findall(r'<p class="pp-win">🏆 Won by .*?top \$\{paid\} paid`\}</p>', s, flags=re.S); assert len(m) == 1, len(m)
s = s.replace(m[0], """<p class="pp-win">🏆 Won by <b>“${esc(g.ph[g.ord[0]].t)}”</b> · @${esc(g.ph[g.ord[0]].h)}</p><h2 class="pp-h">${prize ? `You won ${amt}!` : 'No cash this time'}</h2>
    <p class="pp-m"><b>${sc} points</b> · ${ppOrd(rank)} of ${n} · ${e.free ? 'free pick' : `${money(st)} pick`}</p>
    <div class="rs-pool"><div><b>${money(n * RACE_AVG)}</b><small>prize pool</small></div><div><b>${money(net)}</b><small>shared by the top ${paid} pickers</small></div><div><b>${money(n * RACE_AVG * .1)}</b><small>to the 6 photo creators</small></div></div>
    <p class="rs-gap">${prize ? `You finished in the top ${paid}, so your share is <b>${amt}</b>.` : `Cash goes to the top ${paid}. You were <b>${rank - paid} place${rank - paid === 1 ? '' : 's'} off</b>.`}</p>""")
s = s.replace('</style>', """.rs-pool{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin:6px 0 6px}.rs-pool div{border-radius:12px;padding:8px 4px;text-align:center;background:rgba(127,127,127,.1)}.rs-pool b{display:block;font-size:1.05rem;font-weight:900;color:#2F6B3F}.rs-pool small{display:block;font-size:.7rem;line-height:1.2;opacity:.85}
html.yg .rs-pool b{color:#21C77A}.rs-gap{margin:4px 0 8px;font-size:.92rem}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v31 ok')
