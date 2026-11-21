# Real Money build, step 230 (after rmv226.py): no coin bonus at sign-up (user choice).
#  - The "Welcome bonus · 150 coins" box and the coins it paid are removed. Coins come from voting.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)
RA("${!opts.real && (opts.bonus || !S.giftEn) ?", "${false ?")
RA("const wb = !S.giftEn ? CFG.FIRST_WIN + CFG.SIGNUP : CFG.SIGNUP;", "const wb = 0;")
RA("gemExplosion(wb, { label: `Welcome bonus · @${h}` })", "(wb && gemExplosion(wb, { label: `Welcome bonus · @${h}` }))", 2)
open(d + 'yofi-real.html', 'w').write(s); print('rm v227 ok')
