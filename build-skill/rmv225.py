# Real Money build, step 228 (after rmv224.py): one sign-up, right after framing (user choice).
#  - After a guest frames their first photo, sign-up is required (no "Later"): username, email, age group.
#    Title "Save your photo to start racing". Every later step (free first Final, cash entries, Cup) then has no wall.
#  - The later sign-up checks stay only as a fallback for old guest saves.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)
RA("if (S.user && S.user.guest && !S.suAsk) { S.suAsk = 1; save(); setTimeout(() => openSignup(() => setTimeout(done, 250), { locked: false, photo: 1 }), 250); return; }",
   "if (S.user && S.user.guest) { setTimeout(() => openSignup(() => setTimeout(done, 250), { locked: true, photo: 1 }), 250); return; }")
RA("opts.photo ? 'Save your photo' :", "opts.photo ? 'Save your photo to start racing' :")
RA("opts.photo ? 'Keep your framed photo and its prize record safe. ' :", "opts.photo ? 'One quick step: your photo, prizes and winnings are saved to your account. ' :")
open(d + 'yofi-real.html', 'w').write(s); print('rm v225 ok')
s = open(d + 'yofi-real.html').read()
a = "${opts.real ? '' : 'Create your account so nothing gets lost.'}"
assert s.count(a) == 1, s.count(a)
s = s.replace(a, "${opts.real || opts.photo ? '' : 'Create your account so nothing gets lost.'}")
open(d + 'yofi-real.html', 'w').write(s); print('trim ok')
