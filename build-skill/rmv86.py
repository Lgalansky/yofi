# Real Money build, step 89 (after rmv85.py): make the streak boxes visible on the Vote screen.
#  The streak bar said "WINS ×1 🎁×3 🎁×6 🎁×10" and was hidden for new players. Now it reads
#  "🔥 2 in a row · 1 more for a Bronze box" with Bronze / Silver / Gold markers in their colours, and shows for everyone
#  (new players still get the coins without the box pop).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA('<div class="stk"><div class="stk-row"><span class="stk-lab" aria-label="Your wins are multiplied by your streak"><small>Wins</small><b class="stk-x">×${streakX(combo)}</b></span>',
   '<div class="stk"><p class="stk-nx">${(() => { const c = Math.min(combo, 10), nx = [3, 6, 10].find(k => k > c), nm = { 3: \'Bronze\', 6: \'Silver\', 10: \'Gold\' }; return nx ? `🔥 <b>${c} in a row</b> · ${nx - c} more for a <b class="t${nx}">${nm[nx]} box</b>` : \'🔥 <b>10 in a row!</b> Gold box earned\'; })()}</p><div class="stk-row">')
RA("${i === 2 ? '<u>🎁</u>×3' : i === 5 ? '<u>🎁</u>×6' : i === 9 ? '<u class=\"bx10\">🎁</u>×10' : ''}",
   "${i === 2 ? '<u class=\"bxt b3\">🎁</u>' : i === 5 ? '<u class=\"bxt b6\">🎁</u>' : i === 9 ? '<u class=\"bxt b10\">🎁</u>' : ''}")
s = s.replace('html.nbx #judge .jfoot,html.nbx #judge p.eye{display:none!important}', 'html.nbx #judge p.eye{display:none!important}')
s = s.replace('</style>', """html:not(.yg) #judge .stk-nx{margin:0 0 6px;text-align:center;font-size:.92rem;color:#2B2320}html:not(.yg) #judge .stk-nx b{color:#14213D}
#judge .stk-nx b.t3{color:#B87333!important}#judge .stk-nx b.t6{color:#7D8796!important}#judge .stk-nx b.t10{color:#B8862E!important}
html:not(.yg) #judge .bxt{border-radius:8px;padding:1px 3px;text-decoration:none}html:not(.yg) #judge .bxt.b3{box-shadow:0 0 0 2px #B87333}html:not(.yg) #judge .bxt.b6{box-shadow:0 0 0 2px #9AA4B2}html:not(.yg) #judge .bxt.b10{box-shadow:0 0 0 2px #D9AE4F}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v86 ok')
# readable photo names on the voting cards (dark text was on a dark strip)
s = open(d + 'yofi-real.html').read()
s = s.replace('</style>', """html:not(.yg) body #judge .tot-c .tot-o{color:#fff!important;-webkit-text-fill-color:#fff;background:rgba(20,33,61,.62)!important;text-shadow:0 1px 2px rgba(0,0,0,.4)}html:not(.yg) body #judge .tot-c .tot-o *{color:#fff!important;-webkit-text-fill-color:#fff}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v86 names ok')
