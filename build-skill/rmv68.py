# Real Money build, step 71 (after rmv67.py):
#  - Reveal drops the crowd's 1st, then 2nd, then 3rd (was 3rd → 1st).
#  - Qualifier pick screen: the 50-coin prize card is no longer highlighted (all three cards equal).
#  - Qualifier result is a full page carrying the reveal over: headline ("Spot on!" / "Not this time") + exact-spot line,
#    navy "YOU WON +10 coins" box on a win, the crowd's top 3 (Finalist badges on the top 2, "Your Nth pick" tags,
#    "✓ Exact match" chips), Your picks with ✓/✗ tags, then Through to the Final, free-pick info and Keep voting.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA('[2, 1, 0].forEach((k, n) => at(1900', '[0, 1, 2].forEach((k, n) => at(1900')
RA("""qz3-pz">${[3, 2, 1].map((k, n) => `<div class="${n ? '' : 'top'}">""", """qz3-pz">${[3, 2, 1].map((k, n) => `<div>""")
RA('<h2 class="g2-h">${right} of 3 in the exact spot</h2>',
   '<h2 class="g2-h gq-h">${pay ? \'Spot on!\' : \'Not this time\'}</h2><p class="rv-sub2">${right} of 3 in the exact spot</p>${pay ? `<div class="rv-won"><span>You won</span><b>+${pay} coins</b></div>` : \'\'}')
RA('<div class="g2-thru">', r"""<p class="rv-lab rv-rule"><span>${cw} top 3</span></p>
    <div class="gq-pod">${top.map((p, i) => `<figure class="${picks[i] === p ? 'hit' : ''}"><img src="${G.ph[p].src}" alt="">${picks.includes(p) ? `<i class="rv-you ${picks[i] === p ? 'ok' : ''}">Your ${GQ_ORD[picks.indexOf(p)]} pick</i>` : ''}<b>${GQ_MED[i]} ${GQ_ORD[i]}</b></figure>`).join('')}</div>
    <div class="gq-sub">${top.map((p, i) => `<span>${picks[i] === p ? '<em class="ok">✓ Exact match</em>' : ''}${i < 2 ? '<em class="fin">→ Finalist</em>' : ''}</span>`).join('')}</div>
    <p class="rv-yp-h rv-rule"><span>Your picks</span></p>
    <span class="rv-yp">${picks.map((p, i) => `<span class="${top[i] === p ? 'ex' : ''}"><img src="${G.ph[p].src}" alt=""><b>Picked ${GQ_ORD[i]}</b>${top[i] === p ? '<em class="ok">✓ Exact match</em>' : `<em class="no">✗ ${top.includes(p) ? `Finished ${GQ_ORD[top.indexOf(p)]}` : 'Not in top 3'}</em>`}</span>`).join('')}</span>
    <div class="g2-thru">""")
RA("${pay ? `<b>+${pay} coins</b> · ${Math.floor(S.gems - pay)} → ${Math.floor(S.gems)} coins`", "${pay ? `Your coins: ${Math.floor(S.gems - pay)} → <b>${Math.floor(S.gems)}</b>`")
s = s.replace('</style>', """html body .ppop .gq2 .rv-won b{font-size:2.7rem}html:not(.yg) body .ppop .gq2 .gq-h{font:800 2.3rem/1.02 Fraunces,Georgia,serif!important;color:#14213D!important;-webkit-text-fill-color:#14213D;margin:4px 0 0}
.gq-pod{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.gq-pod figure{position:relative;margin:0;border-radius:14px;overflow:hidden;aspect-ratio:1/1.1;box-shadow:inset 0 0 0 1.5px #E2D3BC}
.gq-pod figure.hit{box-shadow:0 0 0 3px #D9AE4F,0 0 16px rgba(217,174,79,.5)}.gq-pod img{width:100%;height:100%;object-fit:cover;display:block}
.gq-pod b{position:absolute;bottom:6px;left:50%;transform:translateX(-50%);background:rgba(255,255,255,.93);border-radius:999px;padding:2px 10px;white-space:nowrap;font:800 .95rem Fraunces,Georgia,serif;color:#14213D}
.gq-sub{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:6px 0 4px}.gq-sub span{display:flex;flex-direction:column;align-items:center;gap:4px}
.gq-sub em{font-style:normal;font-weight:800;font-size:.76rem;padding:2px 9px;border-radius:999px}html body .ppop .gq-sub em.ok{background:#E3F0DE;color:#2F6B3F!important;-webkit-text-fill-color:#2F6B3F}html body .ppop .gq-sub em.fin{background:#E3EAF5;color:#1E3A6E!important;-webkit-text-fill-color:#1E3A6E}
.gq2 .rv-yp{margin-bottom:12px}.gq2 .rv-won{margin-top:8px}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v68 ok')
