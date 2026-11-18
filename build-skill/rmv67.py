# Real Money build, step 70 (after rmv66.py):
#  - Qualifier pick screen opens on its own while you vote, so the next voting taps landed on its photos and picked a top 3
#    for you. Taps are now ignored for the first 900 ms after it opens, and it opens scrolled to the top.
#  - Coin icon looked like a yellow dot: now a minted coin (rim, inner ring, embossed star).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("function gateOpen() { const G = gateGame(), y = isYoungW(), keep = y ? 'Keep judging' : 'Keep voting', fin = raceName(G.ns), cw = y ? 'judges’' : 'crowd’s'; let picks = [];",
   "function gateOpen() { const G = gateGame(), y = isYoungW(), keep = y ? 'Keep judging' : 'Keep voting', fin = raceName(G.ns), cw = y ? 'judges’' : 'crowd’s'; let picks = [], first = true; const t0 = Date.now();")
RA("document.querySelectorAll('#coach [data-pp]').forEach(b => b.onclick = () => { const i = +b.dataset.pp, k = picks.indexOf(i); if (k >= 0) picks.splice(k, 1); else if (picks.length < 3) picks.push(i); draw(); });\n    document.querySelectorAll('#coach [data-gsl]')",
   "if (first) { first = false; const c = $('#coach'); [c, c.firstElementChild, document.querySelector('#coach .pp')].forEach(e => { if (e) e.scrollTop = 0; }); }\n    document.querySelectorAll('#coach [data-pp]').forEach(b => b.onclick = () => { if (Date.now() - t0 < 900) return; const i = +b.dataset.pp, k = picks.indexOf(i); if (k >= 0) picks.splice(k, 1); else if (picks.length < 3) picks.push(i); draw(); });\n    document.querySelectorAll('#coach [data-gsl]')")
s = s.replace('</style>', """html body .qz3-coin{position:relative;font-style:normal;background:radial-gradient(circle at 34% 28%,#FFF6C8 0 9%,#F7D35A 30%,#E7A928 62%,#C4861A 100%)!important;box-shadow:inset 0 0 0 .06em #A86E10,inset 0 0 0 .13em #F4CB55,inset 0 0 0 .16em #B97D16,0 .07em .14em rgba(110,70,10,.4)!important}
html body .qz3-coin::after{content:'★';position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:.5em;line-height:1;font-style:normal;color:#B57A14;-webkit-text-fill-color:#B57A14;text-shadow:0 .04em 0 #FFF0B0,0 -.03em 0 rgba(120,70,0,.45)}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v67 ok')
