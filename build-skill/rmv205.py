# Real Money build, step 208 (after rmv204.py): the + on the cash balance opens the "Your cash" sheet (Add cash /
#  Withdraw) for everyone, instead of an old "Earn coins by voting" screen for players who haven't paid yet.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
a = "if (!w || e.target.closest('.gplus')) return; if (!S || !S.user) return; e.preventDefault(); e.stopImmediatePropagation(); e.stopPropagation(); cashSheet(); }, true);"
assert s.count(a) == 1
s = s.replace(a, "if (!w) return; if (!S || !S.user) return; e.preventDefault(); e.stopImmediatePropagation(); e.stopPropagation(); cashSheet(); }, true);")
open(d + 'yofi-real.html', 'w').write(s); print('rm v205 ok')
