# Real Money build, step 60 (after rmv56.py): qualifier pick screen from the user's mock-up:
# "WIN UP TO" pill + big gold coin "50 coins", then three prize cards (50 / 25 / 10 coins for 3 / 2 / 1 exact matches).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

COIN = '<i class="qz3-coin" aria-hidden="true"></i>'
RA('<h2 class="g2-h">Pick the top 3</h2>',
   '<div class="qz3-win"><span class="qz3-pill">Win up to</span><b class="qz3-big">' + COIN + '${GATE_COINS[3]} coins</b></div><h2 class="g2-h">Pick the top 3</h2>')
RA('<div class="g2-pz"><span>3 exact · <b>${GATE_COINS[3]}</b></span><span>2 exact · <b>${GATE_COINS[2]}</b></span><span>1 exact · <b>${GATE_COINS[1]}</b></span></div><p class="g2-n">Coins for every photo in its exact spot.</p>',
   '<div class="qz3-pz">${[3, 2, 1].map((k, n) => `<div class="${n ? \'\' : \'top\'}"><span class="qz3-amt">' + COIN + '<span class="qz3-n"><b>${GATE_COINS[k]}</b><small>coins</small></span></span><p>${k} exact match${k === 1 ? \'\' : \'es\'}</p></div>`).join(\'\')}</div>')
s = s.replace('</style>', """.qz3-win{margin:2px 0 0}.qz3-pill{display:inline-block;background:#1E3A6E;color:#fff;font-weight:900;letter-spacing:.14em;text-transform:uppercase;font-size:.82rem;padding:5px 22px;border-radius:999px}
.qz3-big{display:flex;align-items:center;justify-content:center;gap:10px;font:900 3.1rem/1 Fraunces,Georgia,serif;color:#1E3A6E;margin:6px 0 2px}
.qz3-coin{display:inline-block;flex:none;width:1em;height:1em;border-radius:50%;background:radial-gradient(circle at 35% 30%,#FFF1A6 0 18%,#F5C542 40%,#D9981C 75%,#B9780F);box-shadow:inset 0 0 0 .06em #C78A14,0 .08em .16em rgba(120,80,10,.35)}
.qz3-big .qz3-coin{width:1.05em;height:1.05em}
.qz3-pz{display:grid!important;grid-template-columns:repeat(3,1fr);gap:8px;margin:10px 0 12px}.qz3-pz>div{display:block!important;min-width:0;background:#FBF6EE;border-radius:16px;box-shadow:inset 0 0 0 1.5px #EAD7A8;padding:10px 6px 8px}
.qz3-pz>div.top{background:#FFF0C2;box-shadow:inset 0 0 0 2.5px #E2A21C}.qz3-amt{display:flex;align-items:center;justify-content:center;gap:6px;line-height:1}.qz3-amt .qz3-coin{font-size:1.45rem}.qz3-n{display:flex;flex-direction:column;align-items:center;line-height:.95}
.qz3-amt b{font:900 1.75rem/1 Fraunces,Georgia,serif;color:#1E3A6E}.qz3-amt small{display:block;font:800 .95rem Fraunces,Georgia,serif;color:#1E3A6E;margin:0}
.qz3-pz p{margin:8px 0 0;padding-top:6px;border-top:1px solid #EAD7A8;font-size:.82rem}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v57 ok')
