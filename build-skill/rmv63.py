# Real Money build, step 66 (after rmv62.py): qualifier reveal and result speak the same language.
#  - Qualifiers only pay for exact spots, so the reveal summary says "X of 3 in the exact spot" (no "in the top 3" count),
#    the subtitle says "Top 2 go through to the Xpm Final", and the coin line says what 1 exact spot pays.
#  - Result headline matches: "X of 3 in the exact spot"; the "See the full result" fold (a repeat of the reveal) is gone.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

RA("""$('#rvMe').innerHTML = `<b class="rv-sum">${inT} of your photos in the top 3 · ${ex} in the exact spot</b>""",
   """$('#rvMe').innerHTML = `<b class="rv-sum">${o.qual ? `${ex} of 3 in the exact spot` : `${inT} of your photos in the top 3 · ${ex} in the exact spot`}</b>""")
RA("res: { won: !!pay, txt: pay ? `+${pay} coins` : 'No coins this time' }, kicker: `Group ${G.gi + 1} of 3 · qualifier`, title: `${isYoungW() ? 'Judges' : 'The crowd'} decide who goes through` },",
   "qual: 1, res: { won: !!pay, txt: pay ? `+${pay} coins` : `No coins · 1 exact spot pays ${GATE_COINS[1]} coins` }, kicker: `Group ${G.gi + 1} of 3 · qualifier`, title: `Top 2 go through to the ${raceName(G.ns)} Final` },")
RA('<h2 class="g2-h">${right} of 3 matched</h2><p class="g2-s">${sub}</p>', '<h2 class="g2-h">${right} of 3 in the exact spot</h2>')
RA("`0 coins · get 1 photo in its exact spot to win`", "`No coins this time · 1 exact spot pays ${GATE_COINS[1]} coins`")
i = s.index('<details class="g2-more">'); j = s.index('</details>', i) + len('</details>')
s = s[:i] + s[j:].lstrip('\n')
open(d + 'yofi-real.html', 'w').write(s); print('rm v63 ok')
