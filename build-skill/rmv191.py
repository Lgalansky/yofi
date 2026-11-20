# Real Money build, step 194 (after rmv190.py): the free first Final is switched off (owner: keep it off for now).
#  Every Final entry is paid ($2–$20); finalist card shows the normal entry line.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("const free = !S.fin1; if (free) fee = 2;", "const free = false;")
RA("${S.fin1 ? `Pick your entry ($2–$20) · 1st wins up to ${money(20 * QF_PAY[0])}` : '🎁 Your first Final is free · 1st wins $7.00'}", "Pick your entry ($2–$20) · 1st wins up to ${money(20 * QF_PAY[0])}")
open(d + 'yofi-real.html', 'w').write(s); print('rm v191 ok')
