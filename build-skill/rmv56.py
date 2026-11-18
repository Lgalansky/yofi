# Real Money build, step 59 (after rmv55.py): Final results match the reveal and partial picks pay.
#  - New payout line: "2 in the top 3" (any order, none exact) now wins a small share (weight 0.6).
#    Rule everywhere: "Win with 1+ photo in its exact spot, or 2+ photos in the top 3."
#  - Reveal ends with a summary in the same words as the result screen ("2 in the top 3 · 0 in the exact spot · you won $X").
import os, re
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

RA("{ k: 'o', w: 1.2, lab: 'All 3 in the top 3, other order' }];", "{ k: 'o', w: 1.2, lab: 'All 3 in the top 3, other order' }, { k: 'p2', w: .6, lab: '2 in the top 3' }];")
RA("return e || (p.every(x => top.includes(x)) ? 'o' : 0); };", "const t = p.filter(x => top.includes(x)).length; return e || (t === 3 ? 'o' : t === 2 ? 'p2' : 0); };")
RA("${t.k === 'o' ? 'Top 3, different order'", "${t.k === 'p2' ? '2 in the top 3, any order' : t.k === 'o' ? 'Top 3, different order'")
RA("Win with at least 1 exact position, or all 3 photos in any order.", "Win with 1+ photo in its exact spot, or 2+ photos in the top 3.")
RA("Get 1 or more picks in the right place to win cash", "Win with 1 photo in its exact spot, or 2 in the top 3")
s = s.replace("Get 1 or more in the right place to win cash", "Win with 1 in its exact spot or 2 in the top 3")
RA("Get 1 or more in the right place to win a share of the prize pool.", "Get 1 photo in its exact spot, or 2 in the top 3, to win a share of the prize pool.")
# near-miss chip only when it really was a miss (1 photo in the top 3, none exact)
RA("const chip = !prize && inT ?", "const chip = !prize && inT === 1 ?")
RA("One photo in its exact spot would have paid about", "One more photo in the top 3 would have paid about")
# reveal summary + win amount on the final reveal
RA("  at(1900 + 3 * 1300 + 400, () => { const g = $('#rvGo'), k = $('#rvSkip');",
   "  at(1900 + 3 * 1300 + 300, () => { if (!picks.length) return; const top = ord.slice(0, 3), ex = picks.filter((p, i) => top[i] === p).length, inT = picks.filter(p => top.includes(p)).length;\n    $('#rvMe').innerHTML = `<b class=\"rv-sum\">${inT} of your photos in the top 3 · ${ex} in the exact spot</b>${o.res ? `<span class=\"rv-res ${o.res.won ? 'won' : ''}\">${o.res.txt}</span>` : ''}`; });\n  at(1900 + 3 * 1300 + 400, () => { const g = $('#rvGo'), k = $('#rvSkip');")
RA("revealSeq({ ph: g.ph, ord: g.ord, picks: e.picks, kicker: `${raceName(g.sl)} Final · ${esc(showName(g.k))}`,",
   "revealSeq({ ph: g.ph, ord: g.ord, picks: e.picks, res: { won: !!prize, txt: prize ? `You won ${money(prize)}` : 'No cash this time' }, kicker: `${raceName(g.sl)} Final · ${esc(showName(g.k))}`,")
RA("revealSeq({ ph: G.ph, ord: G.ord, picks, kicker:", "revealSeq({ ph: G.ph, ord: G.ord, picks, res: { won: !!pay, txt: pay ? `+${pay} coins` : 'No coins this time' }, kicker:")
s = s.replace('</style>', """.rv-sum{display:block;color:#1E3A6E}.rv-res{display:inline-block;margin-top:6px;padding:4px 14px;border-radius:999px;background:#EEE6D8;font-weight:800}.rv-res.won{background:#E6F0DF;color:#2F6B3F}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v56 ok')
