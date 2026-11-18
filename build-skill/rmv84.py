# Real Money build, step 87 (after rmv83.py):
#  - Free pick → live pick page was ~9 s: the pick screen stayed open, so the "wait until nothing is open" loop retried
#    12 times. Now, when the pick screen itself is showing, the live page replaces it straight away.
#  - Live status explains the rule from the player's own picks: "Right now: no cash yet" + "1 of your picks in the top 3 ·
#    0 in its exact spot" + "Needs 1 more in the top 3 and 1 in its exact spot". Each highlighted row says where that pick
#    needs to finish ("Your 2nd pick · needs 2nd") or "✓ exact".
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("(function sh(t) { setTimeout(() => { if (($('#coach').classList.contains('on')",
   "if (document.querySelector('#coach.on #ppFree, #coach.on #ppGo, #coach.on #ppReal')) { setTimeout(ppOpen, 120); return; } (function sh(t) { setTimeout(() => { if (($('#coach').classList.contains('on')")
RA("""return `<div class="rb-st ${T.prize ? 'win' : ''}"><b>${T.prize ? `If it ended now: you’d win ~${money(T.prize)}` : 'If it ended now: no cash yet'}</b><small>${ex ? `${ex} of your picks in the exact spot` : 'Needs 2 in the top 3, 1 in its exact spot'}</small></div>`; }""",
   """const inT = pos.filter(x => x >= 1 && x <= 3).length, nd = []; if (inT < 2) nd.push(`${2 - inT} more in the top 3`); if (ex < 1) nd.push('1 in its exact spot');
  return `<div class="rb-st ${T.prize ? 'win' : ''}"><b>${T.prize ? `Right now you’d win ~${money(T.prize)}` : 'Right now: no cash yet'}</b><small>${inT} of your picks in the top 3 · ${ex} in the exact spot${!T.prize && nd.length ? `<br><b class="rb-need">Needs ${nd.join(' and ')}</b>` : ''}</small></div>`; }""")
RA("${pk >= 0 ? `<u>Your ${['1st', '2nd', '3rd'][pk]} pick</u>` : ''}",
   "${pk >= 0 ? `<u>Your ${['1st', '2nd', '3rd'][pk]} pick${n === pk ? ' · ✓ exact' : ` · needs ${['1st', '2nd', '3rd'][pk]}`}</u>` : ''}")
s = s.replace('</style>', """.rb-need{display:block;margin-top:2px;font-weight:800;color:#14213D}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v84 ok')
