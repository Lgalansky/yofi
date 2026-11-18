# Real Money build, step 93 (after rmv89.py):
#  - First-pick guarantee removed ("Your next free pick is on us" after a losing first free pick).
#  - Every Final result: the "Your photo could win real cash" card sits straight under the result (You won / cash line),
#    and the prize split (pool, players who won cash, View payouts) follows below it. New players' first result keeps the
#    "Your turn: add a photo" label, next Final line, and no cash upsell.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("if (S.tut === 3 && e.free && !prize && !S.fg) {", "if (false) {")
RA("else if (S.tut === 3) { S.tut = 4; S.unlk = 1; save(); }", "if (S.tut === 3) { S.tut = 4; S.unlk = 1; save(); }")
RA("if (S.tut === 3) { const cw = document.querySelector('#coach .cw2'), cb = document.querySelector('#coach .fr2-cash'); if (cw && cb) {",
   "{ const cw0 = document.querySelector('#coach .cw2'), cb0 = document.querySelector('#coach .fr2-cash'); if (cw0 && cb0) cb0.insertAdjacentElement('afterend', cw0); }\n  if (S.tut === 3) { const cw = document.querySelector('#coach .cw2'), cb = document.querySelector('#coach .fr2-cash'); if (cw && cb) {")
open(d + 'yofi-real.html', 'w').write(s); print('rm v90 ok')
