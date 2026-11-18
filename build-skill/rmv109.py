# Real Money build, step 112 (after rmv108.py): Final result order: result + cash line → prize pool, players who won
# cash and View payouts → "Your photo could win real cash" card → upsell / next steps.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("cb0 = document.querySelector('#coach .fr2-cash'); if (cw0 && cb0) cb0.insertAdjacentElement('afterend', cw0);",
   "cb0 = document.querySelector('#coach .fr2-pay') || document.querySelector('#coach .fr2-cash'); if (cw0 && cb0) cb0.insertAdjacentElement('afterend', cw0);")
RA("const cw = document.querySelector('#coach .cw2'), cb = document.querySelector('#coach .fr2-cash');",
   "const cw = document.querySelector('#coach .cw2'), cb = document.querySelector('#coach .fr2-pay') || document.querySelector('#coach .fr2-cash');")
open(d + 'yofi-real.html', 'w').write(s); print('rm v109 ok')
