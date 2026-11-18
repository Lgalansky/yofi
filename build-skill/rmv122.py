# Real Money build, step 125 (after rmv121.py): version number on the account page.
#  "PhotoPicks v122" under Reset prototype, so a screenshot shows which build it came from. The number is the
#  newest rmvN.py in the build folder, so it moves on by itself with every new step.
import os, re
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
here = os.path.dirname(os.path.abspath(__file__))
v = max(int(m.group(1)) for f in os.listdir(here) for m in [re.fullmatch(r'rmv(\d+)\.py', f)] if m)
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA('<button class="link" id="mR" style="margin-top:6px">Reset prototype</button></div>`);',
   '<button class="link" id="mR" style="margin-top:6px">Reset prototype</button><p class="pf-ver">PhotoPicks v%d</p></div>`);' % v)
s = s.replace('</style>', '.pf-ver{text-align:center;font-size:.72rem;opacity:.55;margin:6px 0 0;letter-spacing:.04em}\n</style>', 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v122 ok (v%d)' % v)
