# Real Money build, step 114 (after rmv110.py): the Coming-up strip no longer shows your photo ("Sterling · next
# qualifier" / "Sterling · in the ring now"): the photo journey card under the streak bar already shows it.
# The strip shows the next game or your live pick only.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("if (hp) it.push({ ic: '📷', t: `<b>${esc(rcName(hp))}</b> · next qualifier`", "if (false && hp) it.push({ ic: '📷', t: `<b>${esc(rcName(hp))}</b> · next qualifier`")
RA("if (p) return { ic: '🎀', t: `<b>${esc(rcName(p))}</b> · ", "if (false && p) return { ic: '🎀', t: `<b>${esc(rcName(p))}</b> · ")
open(d + 'yofi-real.html', 'w').write(s); print('rm v111 ok')
