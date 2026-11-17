# Real Money build, step 48 (after rmv44.py):
#  - Qualifier groups only use photos from the Final's own category (no child/garden photos in a Pets qualifier).
#  - Final result screen from the user's mock-ups: headline, position chip, cash won pill, winner, crowd's top 3 / your picks
#    with "Picked 1st · Finished 3rd" tags, rule line, pool + winners stats, creators line, collapsible payout table,
#    "View next Final" and "Judge photos". The "Enter your own photo" creator card stays.
import os, re
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

RA("fill = ppShuffle(SEED.filter(x => x.src && !used.has(x.src) && shSeed.includes(x.cat)), rr)",
   "fill = ppShuffle(SEED.filter(x => x.src && !q.some(z => z && z.src === x.src) && shSeed.includes(x.cat)), rr)")

m = re.findall(r"  popOpen\(`<div class=\"pp\"><button class=\"pc-x\" data-shclose aria-label=\"Close\">\$\{QS_X\}</button>\n    <p class=\"pp-k\">🎀 The \$\{raceName\(g\.sl\)\} Final · \$\{esc\(showName\(g\.k\)\)\} · results</p>.*?\n    <button class=\"btn block \$\{cashP \? 'pc-go' : 'pc-real'\}\" id=\"ppNext\">.*?</div></div>`\);\n", s, flags=re.S)
assert len(m) == 1, len(m)
s = s.replace(m[0], r"""  const ex = e.picks.filter((p, i) => top[i] === p).length, inT = e.picks.filter(p => top.includes(p)).length, ORD = ['1st', '2nd', '3rd'];
  const head = prize ? `You won ${amt}!` : inT ? `${inT} photo${inT === 1 ? '' : 's'} in the top 3` : 'No photos in the top 3';
  const chip = ex ? `${ex} in the correct position` : inT === 3 ? 'All 3 in the top 3 · other order' : inT === 2 ? 'Neither in the correct position' : inT === 1 ? 'Not in the correct position' : 'Better luck next hour';
  const ptag = (p, i) => top[i] === p ? '<em class="ok">✓ Exact</em>' : top.includes(p) ? `<em class="mid">Finished ${ORD[top.indexOf(p)]}</em>` : '<em>Outside top 3</em>';
  popOpen(`<div class="pp fr2"><button class="pc-x" data-shclose aria-label="Close">${QS_X}</button>
    <p class="pp-k">${esc(showName(g.k))}</p><p class="fr2-sub">${raceName(g.sl)} Final · Results</p>
    <h2 class="fr2-h">${head}</h2><span class="fr2-chip">${chip}</span>
    <p class="fr2-cash ${prize ? 'won' : ''}"><b>Cash won: ${amt}</b> · ${e.free ? 'Free pick' : `${money(st)} pick`}</p>
    <p class="fr2-win">🏆 Winner: <b>“${esc(g.ph[g.ord[0]].t)}”</b> by @${esc(g.ph[g.ord[0]].h)}</p>
    <p class="fr2-row">Crowd’s top 3</p><div class="fr2-g">${top.map((p, i) => `<figure><span class="fr2-m">${PP_MED[i]} ${ORD[i]}</span><img src="${g.ph[p].src}" alt=""></figure>`).join('')}</div>
    <p class="fr2-row">Your picks</p><div class="fr2-g">${e.picks.map((p, i) => `<figure class="${top[i] === p ? 'ok' : top.includes(p) ? 'mid' : ''}"><img src="${g.ph[p].src}" alt=""><b>Picked ${ORD[i]}</b>${ptag(p, i)}</figure>`).join('')}</div>
    <p class="fr2-rule">Win with at least 1 exact position, or all 3 photos in any order.</p>
    <div class="fr2-st"><div><b>${ppPool(n)}</b><small>Total prize pool</small></div><div><b>${TR.winners} of ${n}</b><small>players won cash</small></div></div>
    <p class="fr2-cr">6 photo creators shared ${money(n * RACE_AVG * .1)}</p>
    <details class="fr2-pay"><summary>View payouts</summary><table><tr><th>Result</th><th>Winners</th><th>Total shared</th></tr>${TR.T.map(t => `<tr class="${TR.mine === t ? 'me' : ''}"><td>${t.k === 'o' ? 'Top 3, different order' : `${t.k} exact position${t.k === 1 ? '' : 's'}`}</td><td>${t.n}</td><td>${money(t.amt)}</td></tr>`).join('')}</table>${prize ? `<p>You won <b>${amt}</b> (${(prize / st).toFixed(1)}× your pick).</p>` : ''}</details>
    ${S.tut === 3 || !(S.photos || []).some(p => ['heats', 'q'].includes(rcRec(p.id).st)) ? `<div class="tut-up">${(() => { const w = g.ph[g.ord[0]]; return w ? `<p class="cr-earn">🏆 @${esc(w.h)} earned <b>${money(finShare(g.sl, 1))}</b> as the creator of “${esc(w.t)}”, this Final’s winner</p>` : ''; })()}<b>📷 Enter your own photo</b><span>Qualify for an upcoming Final and win real cash. The top 2 in each qualifier go through, and every finalist’s creator gets paid.${ffreeFirst() ? ' We’ll give you 150 coins to improve your first photo.' : ''}</span>${finSchedHTML(3)}<button class="btn block pc-go" id="ppUp">📷 Enter a photo</button></div>` : ''}
    <button class="btn block fr2-next" id="ppNext">View next Final →</button>
    <div style="text-align:center"><button class="link fr2-j" id="ppOk">⚖️ ${y ? 'Judge photos' : 'Judge photos'}</button></div></div>`);
""")
s = s.replace('</style>', """.fr2{text-align:center}.fr2 .pp-k{color:#2F6B3F;letter-spacing:.14em;margin-bottom:0}.fr2-sub{margin:0 0 2px;font-size:.88rem;opacity:.8}.fr2-h{font:800 2rem/1.08 Fraunces,Georgia,serif;margin:2px 0 6px}
.fr2-chip{display:inline-block;background:#E6F0DF;color:#2F6B3F;font:700 1rem Fraunces,Georgia,serif;padding:4px 16px;border-radius:999px;margin:0 0 8px}
.fr2-cash{display:inline-block;background:#EEE6D8;border-radius:999px;padding:5px 16px;margin:0 0 8px}.fr2-cash b{font:800 1.08rem Fraunces,Georgia,serif}.fr2-cash.won{background:#E6F0DF;color:#2F6B3F}
.fr2-win{margin:0 0 10px}.fr2-win b{color:#2F6B3F}.fr2-row{text-align:left;background:#E6F0DF;color:#2F6B3F;font-weight:900;letter-spacing:.12em;text-transform:uppercase;font-size:.78rem;border-radius:999px;padding:4px 14px;margin:6px 0 8px}
.fr2-g{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:0 0 6px}.fr2-g figure{margin:0;border-radius:14px;padding:2px}.fr2-g img{width:100%;aspect-ratio:1/.82;object-fit:cover;border-radius:12px;display:block}
.fr2-m{display:block;font:800 .95rem Fraunces,Georgia,serif;margin-bottom:4px}.fr2-g figure.ok{box-shadow:inset 0 0 0 2.5px #2F6B3F}.fr2-g figure.mid{box-shadow:inset 0 0 0 2.5px #E2A21C}
.fr2-g figure b{display:block;font-size:.86rem;margin-top:4px}.fr2-g em{display:inline-block;font-style:normal;font-size:.78rem;padding:2px 9px;border-radius:999px;margin-top:2px;background:#EEE6D8}.fr2-g em.mid{background:#FFE7B0;font-weight:700}.fr2-g em.ok{background:#E6F0DF;color:#2F6B3F;font-weight:800}
.fr2-rule{font-style:italic;background:#EEF2E6;border-radius:999px;padding:5px 12px;font-size:.84rem;margin:8px 0 12px}
.fr2-st{display:grid;grid-template-columns:1fr 1fr;gap:10px;padding-top:10px;border-top:1px solid #E2D3BC}.fr2-st div{background:#F3EDE2;border-radius:14px;padding:8px}.fr2-st b{display:block;white-space:nowrap;font:800 1.45rem/1.1 Fraunces,Georgia,serif;color:#2F6B3F}.fr2-st small{font-size:.8rem}
.fr2-cr{margin:8px 0 2px;font-size:.88rem}.fr2-pay{margin:0 0 10px}.fr2-pay summary{cursor:pointer;color:#2F6B3F;font-weight:800;list-style:none}.fr2-pay summary::after{content:' ⌄'}
.fr2-pay table{width:100%;border-collapse:collapse;margin-top:6px;font-size:.84rem;text-align:left}.fr2-pay th{background:#24563A;color:#fff;padding:5px 8px}.fr2-pay td{padding:5px 8px;border-bottom:1px solid #E2D3BC}.fr2-pay td:nth-child(2){text-align:center}.fr2-pay td:last-child,.fr2-pay th:last-child{text-align:right}.fr2-pay td:last-child{color:#2F6B3F;font-weight:800}.fr2-pay tr.me td{background:#E6F0DF}
html .fr2 .btn.fr2-next{background:#24563A!important;color:#fff!important;font:800 1.25rem Fraunces,Georgia,serif}.fr2-j{font-weight:800;color:#2F6B3F!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v45 ok')
