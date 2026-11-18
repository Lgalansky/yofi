# Real Money build, step 102 (after rmv98.py):
#  - The pick-3-of-5 coin game is called "Coin Pick" (was "Qualifier"): pick screen chip, Coming-up strip, reveal
#    kicker, result header and win label. (A creator's photo still "qualifies for the Final"; that wording is unchanged.)
#  - Call the crowd: no shading over the photos after a vote (percentages only, with a shadow to stay readable).
#  - "The crowd went the other way" without the ✕.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA('g2-chip">Qualifier · Group ${G.gi + 1} of 3', 'g2-chip">Coin Pick · Round ${G.gi + 1} of 3')
RA("kicker: `Group ${G.gi + 1} of 3 · qualifier`", "kicker: `Coin Pick · Round ${G.gi + 1} of 3`")
RA("Group ${G.gi + 1} of 3 · results", "Coin Pick · Round ${G.gi + 1} of 3")
s = s.replace("label: 'Qualifier win'", "label: 'Coin Pick win'")
RA("<b>Upcoming qualifier · ${esc(showName(ppGame(ppSlot() + 1).k))}</b> · pick 3 of", "<b>Coin Pick · ${esc(showName(ppGame(ppSlot() + 1).k))}</b> · pick 3 of")
RA("'✕ The crowd went the other way'", "'The crowd went the other way'")
s = s.replace('</style>', """html body #judge .tot-c .cfx-fill i{display:none!important}html body #judge .tot-c.other,html body #judge .tot-c:not(.win),html body #judge .tot-c.other img,html body #judge .tot-c:not(.win) img{opacity:1!important;filter:none!important}html body #judge .tot-c::after{display:none!important}html body #judge .tot-c .cfx-fill b{text-shadow:0 2px 10px rgba(0,0,0,.7),0 0 2px rgba(0,0,0,.6)}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v99 ok')
