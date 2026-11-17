# Real Money build, step 38 (after rmv34.py): keep your Final picks through sign-up.
# A guest who picks then taps the free pick is asked to sign up; after sign-up the pick screen reopens with the same
# picks and the free pick is placed straight away.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("let picks = e ? e.picks.slice() : [], stake",
   "const kp = !e && window.__ppKeep && window.__ppKeep.sl === g.sl ? window.__ppKeep : null; let picks = e ? e.picks.slice() : kp ? kp.picks.slice() : [], stake")
RA("if (S.user && S.user.guest) { popClose(); openSignup(() => ppOpen(), { locked: false }); return; }",
   "if (S.user && S.user.guest) { window.__ppKeep = { sl: g.sl, picks: picks.slice(), auto: 1 }; popClose(); openSignup(() => setTimeout(ppOpen, 200), { locked: false }); return; }")
RA("    bind(); };\n  draw(); }",
   "    bind(); };\n  draw(); if (kp) { window.__ppKeep = null; if (kp.auto && picks.length === 3 && !(S.user && S.user.guest)) setTimeout(() => { const b = document.getElementById('ppFree'); if (b && !b.disabled) b.click(); }, 400); } }")
open(d + 'yofi-real.html', 'w').write(s); print('rm v35 ok')
