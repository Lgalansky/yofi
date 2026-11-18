# Real Money build, step 103 (after rmv99.py):
#  - Back to "Qualifier" for the pick-3-of-5 coin game (one name with the photo side: "Qualifier · Round 1 of 3").
#  - Call the crowd: no percentages on the photo tiles; the banner carries the result
#    ("You called it! · 57% agreed · +5 coins · 🔥 2 in a row" / "The crowd went the other way · 60% picked the other photo").
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA('g2-chip">Coin Pick · Round ${G.gi + 1} of 3', 'g2-chip">Qualifier · Round ${G.gi + 1} of 3')
RA("kicker: `Coin Pick · Round ${G.gi + 1} of 3`", "kicker: `Qualifier · Round ${G.gi + 1} of 3`")
RA("Coin Pick · Round ${G.gi + 1} of 3", "Qualifier · Round ${G.gi + 1} of 3")
s = s.replace("label: 'Coin Pick win'", "label: 'Qualifier win'")
RA("<b>Coin Pick · ${esc(showName(ppGame(ppSlot() + 1).k))}</b> · pick 3 of", "<b>Upcoming qualifier · ${esc(showName(ppGame(ppSlot() + 1).k))}</b> · pick 3 of")
RA("${agree ? `${earn ? `+${earn} coins · ` : ''}🔥 ${combo} in a row`", "${agree ? `${mine}% agreed · ${earn ? `+${earn} coins · ` : ''}🔥 ${combo} in a row`")
s = s.replace('</style>', """html body #judge .tot-c .cfx-fill{display:none!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v100 ok')
