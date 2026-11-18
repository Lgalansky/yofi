# Real Money build, step 78 (after rmv74.py): qualifier result = headline + the photo card + Keep voting.
#  The reveal already showed what was won, so the exact-spot line, YOU WON box and coin line go; the user also removed
#  "Through to the Final" and the free-pick coins note.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("""<p class="rv-sub2">${right} of 3 in the exact spot</p>${pay ? `<div class="rv-won"><span>You won</span><b>+${pay} coins</b></div>` : ''}""", '')
RA("""<span class="g2-earn ${pay ? 'won' : ''}">${pay ? `Your coins: ${Math.floor(S.gems - pay)} → <b>${Math.floor(S.gems)}</b>` : `No coins this time · 1 exact spot pays ${GATE_COINS[1]} coins`}</span>""", '')
RA("""<div class="g2-thru"><span>${top.slice(0, 2).map(p => `<img src="${G.ph[p].src}" alt="">`).join('')}</span><div><b>Through to the ${fin} Final</b><small>The ${cw.toLowerCase()} top 2 qualify · picks open at ${raceName(G.ns - 1)}</small></div></div>""", '')
RA("in your category’s qualifier, like these two.", "in your category’s qualifier.", 0) if False else None
s = s.replace('</style>', """.gq2:has(.gq-cw) .g2-prog{display:none!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v75 ok')
