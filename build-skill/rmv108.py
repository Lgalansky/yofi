# Real Money build, step 111 (after rmv107.py): Coming-up strip while a pick is live just says "Your pick is live"
# (no Final name or running position); the "results in N min" button stays.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
a = "t: `<b>Your pick is live · ${raceName(m.g.sl)} ${esc(showName(m.g.k))} Final</b> · your 1st pick is running ${ppOrd(m.pos[0])}`"
assert s.count(a) == 1; s = s.replace(a, "t: `<b>Your pick is live</b>`")
open(d + 'yofi-real.html', 'w').write(s); print('rm v108 ok')
