# Real Money build, step 28 (after rmv24.py): no "free $1 Final pick" bar on the Vote screen; coins menu row says "Free Final pick" (no $1 value).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA('${qsChipHTML()}${fbBarHTML()}', '${qsChipHTML()}')
RA('<b>Free $1 Final pick</b><small>The ${raceName(ppGame().sl)} Final', '<b>Free Final pick</b><small>The ${raceName(ppGame().sl)} Final')
open(d + 'yofi-real.html', 'w').write(s); print('rm v25 ok')
