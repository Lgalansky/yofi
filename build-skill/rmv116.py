# Real Money build, step 119 (after rmv115.py): one journey for new players.
#  Landing: the main button is "Start playing" (judge photos → free pick → result → add your photo). The photo section
#  keeps its explainer but its big button becomes a small "Got a photo? Enter it now ›" link. The green
#  "Pick the Final · from $2" stays for players who arrive ready to pay.
#  The first result already pushes "Your turn: add a photo"; after framing, "Vote to watch it race" brings the player
#  back to voting with the journey card.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA('<h2>Judge photos. Get a free pick.</h2><p>Judge photos to earn a free pick. Pick the winner and win real cash.</p>',
   '<h2>Start here: judge photos.</h2><p>Judge 10 photos to earn a free pick in the hourly Final. Then add your own photo and race it.</p>')
RA('<button class="lp-btn" onclick="rmStartVote()">Judge photos <span aria-hidden="true">→</span></button>',
   '<button class="lp-btn" onclick="rmStartVote()">Start playing <span aria-hidden="true">→</span></button>')
RA('<button class="lp-btn" onclick="rmEnterOwn()">Enter your photo <span aria-hidden="true">→</span></button>',
   '<button class="lp-lnk lp-up" onclick="rmEnterOwn()">Got a photo? Enter it now ›</button>')
s = s.replace('</style>', """html body #landing .lp-up{display:block;margin:12px auto 0;font:800 1rem Nunito,system-ui,sans-serif}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v116 ok')
