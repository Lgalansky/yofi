# Real Money build, step 75 (after rmv71.py): the "Your photo could win real cash" card (enter your own photo) shows on every
# Final result. It used to hide once you had a photo racing, which also brought back the repeated "Winner:" line.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("${S.tut === 3 || !(S.photos || []).some(p => ['heats', 'q'].includes(rcRec(p.id).st)) ? `<div class=\"cw2\">", "${true ? `<div class=\"cw2\">")
RA("Enter your photo${frameFree() ? ' — free' : ''}</button>", "${frameFree() ? 'Enter your photo — free' : (S.photos || []).some(p => p.framed) ? 'Enter another photo' : 'Enter your photo'}</button>")
open(d + 'yofi-real.html', 'w').write(s); print('rm v72 ok')
