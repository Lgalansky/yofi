# Real Money build, step 98 (after rmv94.py): every new player gets the free-pick journey once.
#  Framing a photo (or placing a paid pick) used to end the new-player journey on the spot, so players who started with
#  "Enter your photo" never saw "Free pick unlocked" after 10 votes. Now the journey only ends with the first free-pick
#  result, whichever way the player came in.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("S.firstEntry = 1; if ((S.tut || 9) < 9) S.tut = 9;", "S.firstEntry = 1;")
RA("if (!free && (S.tut || 9) < 9) { S.tut = 9; save(); }", "")
open(d + 'yofi-real.html', 'w').write(s); print('rm v95 ok')
