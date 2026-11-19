# Real Money build, step 149 (after rmv145.py): newbie run-through #4 fixes.
#  1. Cash winnings unlock real games: with $0.50+ in the balance a player sees real games ("Rematch · $1"), even
#     without a deposit. Below $0.50 and never deposited → back to coin games + the deposit offer.
#  2. The starter photo is a dependable demo: it scores 72%, joins the Play Pool, and its first plays arrive within
#     a minute ("Your starter photo was played 8 times · +8 🟡").
#  3. A player's very first game is against a newcomer (prototype: simulated opponent at 32% accuracy).
#  4. No zeros on the earnings card: until a photo is in the Play Pool it says how to start earning, with "Add a photo".
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("const isCash = () => !!(S && S.cashMode), LG_COIN = 25;", "const isCash = () => !!(S && (S.cashMode || (S.cash || 0) >= 0.5)), LG_COIN = 25;")
RA("pct = Math.round(52 + r() * 28),", "pct = p.starter ? 72 : Math.round(52 + r() * 28),")
RA("p.pool = pct >= 60 ? Date.now() : 0; p.plAt = Date.now();", "p.pool = pct >= 60 ? Date.now() : 0; p.plAt = p.starter ? Date.now() - 40 * 60e3 : Date.now();")
RA("else if (r.cash >= 0.01) toast(`📷 Your photos earned ${money(r.cash)} · ${r.plays} plays`);",
   "else if (r.cash >= 0.01) toast(`📷 Your photos earned ${money(r.cash)} · ${r.plays} plays`); else if (r.coins) toast(`📷 Your starter photo was played ${r.plays} times · +${r.coins} 🟡`);")
RA("O = gmOpps(g.n - 1, (S.gmN || 0) < 1 ? Math.max(.3, eye - .25) : eye, r),", "O = gmOpps(g.n - 1, eye, r).map(o => (S.gmN || 0) < 1 ? Object.assign(o, { acc: .32 }) : o),")
RA("function earnHeadHTML() { const P = (S.photos || []).filter(p => p.pool); if (!(S.photos || []).length) return '';",
   "function earnHeadHTML() { const P = (S.photos || []).filter(p => p.pool); if (!(S.photos || []).length) return '';\n  if (!P.length) return `<div class=\"ern\"><p class=\"ern-k\">💵 Start earning from your photos</p><p class=\"ern-top\">Photos picked by <b>60%+ of voters</b> join the Play Pool and earn every time they’re played in a real game.</p><button class=\"btn block db-go\" onclick=\"finPick()\">📷 Add a photo</button></div>`;")
open(d + 'yofi-real.html', 'w').write(s); print('rm v146 ok')
s = open(d + 'yofi-real.html').read()
RA('<div class="ern-row"><div><b>${money(+week.toFixed(2))}</b><small>this week</small></div>', '<div class="ern-row"><div><b>${week || !coins ? money(+week.toFixed(2)) : coins + \' 🟡\'}</b><small>${week || !coins ? \'this week\' : \'earned\'}</small></div>')
open(d + 'yofi-real.html', 'w').write(s); print('rm v146 pass2 ok')
