# Real Money build, step 57 (after rmv53.py): qualifier wins add up and the result screen carries the reveal through.
#  - Every exact match pays: 1 exact 10 coins, 2 exact 25, 3 exact 50 (same rule as the Final: 1+ exact wins).
#  - Result screen leads with the win and the coin total ("+10 coins · 195 → 205 coins"), the photo comparison folds away
#    under "See the full result" (it was just shown in the reveal).
import os, re
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

RA("GATE_COINS = [0, 0, 20, 50]", "GATE_COINS = [0, 10, 25, 50]")
RA("3 exact · <b>${GATE_COINS[3]} coins</b></span><span>2 exact · <b>${GATE_COINS[2]} coins</b></span>",
   "3 exact · <b>${GATE_COINS[3]}</b></span><span>2 exact · <b>${GATE_COINS[2]}</b></span><span>1 exact · <b>${GATE_COINS[1]}</b></span>")
RA("Only the correct positions count.", "Coins for every photo in its exact spot.")
RA("`0 coins earned · 2 matches needed`", "`0 coins · get 1 photo in its exact spot to win`")
RA("${pay ? `+${pay} coins earned` :", "${pay ? `<b>+${pay} coins</b> · ${Math.floor(S.gems - pay)} → ${Math.floor(S.gems)} coins` :")
RA('<div class="g2-cmp"><span></span>', '<details class="g2-more"><summary>See the full result</summary><div class="g2-cmp"><span></span>')
RA("${picks.map((p, i) => `<figure class=\"${top[i] === p ? 'ok' : ''}\"><img src=\"${G.ph[p].src}\" alt=\"\">${tag(p, i)}</figure>`).join('')}</div>",
   "${picks.map((p, i) => `<figure class=\"${top[i] === p ? 'ok' : ''}\"><img src=\"${G.ph[p].src}\" alt=\"\">${tag(p, i)}</figure>`).join('')}</div></details>")
s = s.replace('</style>', """.g2-pz span{font-size:.84rem!important}.g2-earn{font-size:1rem!important;padding:8px 16px!important}.g2-earn b{font-size:1.15rem}
.g2-more{margin:0 0 10px}.g2-more summary{cursor:pointer;list-style:none;font-weight:800;color:#1E3A6E;padding:6px}.g2-more summary::after{content:' ⌄'}.g2-more[open] summary::after{content:' ⌃'}
</style>""", 1)
RA('<div class="g2-prog"><p>${pay ? `<b>+${pay} coins</b> · ` : \'\'}', '<div class="g2-prog"><p>')
RA('<div class=\"g2-prog ready\"><p>${pay ? `<b>+${pay} coins</b> · ` : \'\'}${Math.floor(S.gems)} coins</p>', '<div class=\"g2-prog ready\">')
open(d + 'yofi-real.html', 'w').write(s); print('rm v54 ok')
