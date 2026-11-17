# Real Money build, step 40 (after rmv36.py): Final pick screen from the user's mock-up.
# Big "Win a share of $X · CASH PRIZE POOL" header, "Pick your 1st, 2nd & 3rd", pool reminder above the button,
# disabled button reads "Choose your top 3" until 3 photos are picked.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

RA("""popOpen(`<div class="pp">${head}<h2 class="pp-h">Pick the top 3 of 6</h2>
      <p class="pp-m"><b>${ppPool(g.players)}</b> pool · ${g.players} players · closes ${frTime(g.end)}</p>
      <p class="rc-jp">🎯 Get 1 or more in the right place to win cash</p>
      <p class="pp-leg">🔥 Popularity: % of players picking it to win</p>""",
   """popOpen(`<div class="pp pk">${head}<h2 class="pk-h">Win a share of</h2><b class="pk-amt">${ppPool(g.players)}</b><p class="pk-lab"><span>Cash prize pool</span></p>
      <p class="pk-meta">${g.players} players · Closes ${frTime(g.end)}</p>
      <p class="rc-jp">🎯 Get 1 or more picks in the right place to win cash</p>
      <h3 class="pk-h3">Pick your 1st, 2nd &amp; 3rd</h3><p class="pk-sub">Choose from the 6 photos below</p>
      <p class="pp-leg">🔥 Popularity: picked to win</p>""")
RA("""<p class="pp-i">${n3 ? 'Your podium is set. Tap a photo to change it.' : `Tap your <b>${['1st', '2nd', '3rd'][picks.length]}</b> place photo`}</p>
      ${cash ?""",
   """<p class="pp-i">${n3 ? 'Your top 3 is set. Tap a photo to change it.' : `Tap your <b>${['1st', '2nd', '3rd'][picks.length]}</b> place photo`}</p>
      <p class="pk-rem"><b>${ppPool(g.players)}</b> cash prize pool</p>
      ${cash ?""")
RA("<button class=\"btn block pc-go\" id=\"ppGo\" ${n3 ? '' : 'disabled'}>🎀 Pick for ${money(stake)}</button>",
   "<button class=\"btn block pc-go pk-go\" id=\"ppGo\" ${n3 ? '' : 'disabled'}>${n3 ? `Pick for ${money(stake)}` : 'Choose your top 3'}</button>")
RA("<button class=\"btn block pc-go\" id=\"ppFree\" ${n3 && freeOk ? '' : 'disabled'}>${S.tut === 2 ? '🎟️ Your first Final pick · free' : `🎟️ Free pick · ${FREE_BET_COINS} 🟡`}",
   "<button class=\"btn block pc-go pk-go\" id=\"ppFree\" ${n3 && freeOk ? '' : 'disabled'}>${!n3 ? 'Choose your top 3' : S.tut === 2 ? '🎟️ Your first Final pick · free' : `🎟️ Free pick · ${FREE_BET_COINS} 🟡`}")
s = s.replace('</style>', """.pk .pk-h{font:800 2.1rem/1 Fraunces,Georgia,serif;margin:4px 0 0}.pk .pk-amt{display:block;font:900 4.4rem/1 Fraunces,Georgia,serif;color:#2F6B3F;margin:2px 0}
.pk .pk-lab{display:flex;align-items:center;gap:12px;margin:2px 0 4px;font-weight:900;letter-spacing:.18em;text-transform:uppercase;color:#2F6B3F;font-size:.9rem}.pk .pk-lab::before,.pk .pk-lab::after{content:'';flex:1;height:1.5px;background:#D9B65A}
.pk .pk-meta{margin:0 0 10px}.pk .pk-h3{font:800 1.75rem/1.1 Fraunces,Georgia,serif;margin:12px 0 2px}.pk .pk-sub{margin:0 0 6px}
.pk .pk-rem{border-top:1.5px solid #D9B65A;padding-top:10px;margin:10px 0 8px;font-size:1.05rem}.pk .pk-rem b{font:900 1.6rem Fraunces,Georgia,serif;color:#2F6B3F}
html .pk .btn.pk-go{background:linear-gradient(#3B7A4C,#24563A)!important;color:#fff!important;font:800 1.35rem Fraunces,Georgia,serif!important}html .pk .btn.pk-go:disabled{opacity:1!important;filter:none!important}
html.yg .pk .pk-amt,html.yg .pk .pk-lab,html.yg .pk .pk-rem b{color:#21C77A}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v37 ok')
