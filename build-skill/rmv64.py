# Podium now reads 1st · 2nd · 3rd left to right, lined up with Your picks (Picked 1st · 2nd · 3rd).
# Real Money build, step 67 (after rmv63.py): qualifier picks that are not in their exact spot read as misses.
#  In a qualifier only the exact spot pays, so "Finished 3rd" in a yellow chip looked like a win. Now non-exact picks show
#  a muted "✗ Finished 3rd" / "✗ Outside top 3" and exact ones "✓ Exact · +coins". (The Final keeps its yellow "Finished 2nd",
#  because being in the top 3 counts there.)
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("""const O = ['1st', '2nd', '3rd'], tg = (p, i) => top[i] === p ? '<em class="ok">✓ Exact</em>' : top.includes(p) ? `<em class="mid">Finished ${O[top.indexOf(p)]}</em>` : '<em>Outside top 3</em>';""",
   """const O = ['1st', '2nd', '3rd'], tg = (p, i) => top[i] === p ? '<em class="ok">✓ Exact</em>' : o.qual ? `<em class="no">✗ ${top.includes(p) ? `Finished ${O[top.indexOf(p)]}` : 'Outside top 3'}</em>` : top.includes(p) ? `<em class="mid">Finished ${O[top.indexOf(p)]}</em>` : '<em>Outside top 3</em>';""")
RA('<div class="rv-pod" id="rvPod">${[2, 1, 0].map(k =>', '<div class="rv-pod" id="rvPod">${[0, 1, 2].map(k =>')
RA("? `Finished ${O[top.indexOf(p)]}` : 'Outside top 3'}</em>`", "? `Finished ${O[top.indexOf(p)]}` : 'Not in top 3'}</em>`")
s = s.replace('</style>', """html body .ppop .rv-yp em.no{background:#F1E4E1!important;color:#8A3B32!important;-webkit-text-fill-color:#8A3B32}html body .ppop .rv-yp>span:not(.ex) img{opacity:.75}.rv-yp em{white-space:nowrap}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v64 ok')
