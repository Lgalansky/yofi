# Real Money build, step 63 (after rmv59.py): the Final reveal matches the result screen.
#  - Reveal uses the same player count / prize pool as the result (the one stored with the pick), not the live count.
#  - Reveal ends with a "Your picks" row (Picked 1st ✓ Exact / Finished 2nd / Outside top 3), same as the result screen.
#  - Result headline chip uses the reveal's words: "1 of your photos in the top 3 · 1 in the exact spot".
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

RA("title: `${ppPool(g.players)} prize pool · ${g.players} players` },", "title: `${ppPool(e.players || g.players)} prize pool · ${e.players || g.players} players` },")
RA("""    $('#rvMe').innerHTML = `<b class="rv-sum">${inT} of your photos in the top 3 · ${ex} in the exact spot</b>${o.res ? `<span class="rv-res ${o.res.won ? 'won' : ''}">${o.res.txt}</span>` : ''}`; });""",
   """    const O = ['1st', '2nd', '3rd'], tg = (p, i) => top[i] === p ? '<em class="ok">✓ Exact</em>' : top.includes(p) ? `<em class="mid">Finished ${O[top.indexOf(p)]}</em>` : '<em>Outside top 3</em>';
    $('#rvMe').innerHTML = `<b class="rv-sum">${inT} of your photos in the top 3 · ${ex} in the exact spot</b>${o.res ? `<span class="rv-res ${o.res.won ? 'won' : ''}">${o.res.txt}</span>` : ''}
      <span class="rv-yp-h">Your picks</span><span class="rv-yp">${picks.filter(p => ph[p]).map((p, i) => `<span class="${top[i] === p ? 'ex' : ''}"><img src="${ph[p].src}" alt=""><b>Picked ${O[i]}</b>${tg(p, i)}</span>`).join('')}</span>`; });""")
RA(": ex ? `${ex} in the correct position` : inT === 3 ? 'All 3 in the top 3 · other order' : inT === 2 ? 'Neither in the correct position' : inT === 1 ? 'Not in the correct position' : 'Better luck next hour';",
   ": inT ? `${inT} of your photos in the top 3 · ${ex} in the exact spot` : 'Better luck next hour';")
s = s.replace('</style>', """.rv-yp-h{display:block;margin:14px 0 6px;font-weight:900;letter-spacing:.12em;text-transform:uppercase;font-size:.78rem;color:#1E3A6E}
.rv-yp{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.rv-yp>span{display:flex;flex-direction:column;align-items:center;gap:3px;padding:4px;border-radius:12px}.rv-yp>span.ex{box-shadow:inset 0 0 0 2px #1E3A6E;background:#E3EAF5}
.rv-yp img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:9px}.rv-yp b{font-size:.84rem;color:#1E3A6E}.rv-yp em{font-style:normal;font-size:.76rem;font-weight:700;padding:2px 8px;border-radius:999px;background:#EEE6D8}.rv-yp em.ok{background:none;color:#1E3A6E}.rv-yp em.mid{background:#FFF0C2}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v60 ok')
