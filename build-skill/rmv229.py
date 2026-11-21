# Real Money build, step 232 (after rmv228.py): first Final is free only (user choice).
#  - No "Play for Real" popup or paid options at the first Final: one "Enter free" button.
#  - The welcome offer popup (deposit $10, get $5 free) now shows when the player reaches their next Final.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
a = "if (!p || S.paidCash || S.bonusGot || p.woSeen || window.__woSkip)"
assert s.count(a) == 1, s.count(a)
s = s.replace(a, "if (!p || !S.coinFin || S.paidCash || S.bonusGot || p.woSeen || window.__woSkip)")
open(d + 'yofi-real.html', 'w').write(s); print('rm v229 ok')
