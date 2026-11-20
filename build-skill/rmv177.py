# Real Money build, step 180 (after rmv176.py): the "Qualified!" screen links the win to the money:
#  a gold box "🏆 In the Nature & landscapes Final · 1st could win up to $70" under the result line.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA('<p class="db-s">${nm} beat “${esc(o.t)}” ${A}–${B} and is through to the Final.</p>',
   '<p class="db-s">${nm} beat “${esc(o.t)}” ${A}–${B}.</p><div class="qr-stake ql-win">🏆 ${nm} is in the <b>${esc(showName(photoShow(p) || "pets"))} Final</b><small>1st could win up to <b>${money(20 * QF_PAY[0])}</b> · from a $2 entry, 1st wins ${money(2 * QF_PAY[0])}</small></div>')
s = s.replace('</style>', """.ql-win{animation:cdPop .5s .4s ease-out both}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v177 ok')
