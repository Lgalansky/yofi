# Real Money build, step 42 (after rmv38.py): third new-player journey, "Place a pick".
# Landing "Pick the Final · from $2" goes straight to the live Final's picker with the cash options ($2-$50),
# even for a guest. They choose their 1st/2nd/3rd and amount, then sign up and add cash before paying; the pick is kept.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("function rmPickNow() { rmWatch(); setTimeout(() => { try { popClose(); } catch (e) {} ppOpen(); }, 300); }",
   "function rmPickNow() { rmWatch(); setTimeout(() => { try { popClose(); } catch (e) {} window.__ppCash = 1; ppOpen(); }, 300); }")
RA("function ppOpen() { const g = ppGame(), e = (S.pp || {})[g.sl], own = g.ph.some(p => p.mine), cash = isCash()",
   "function ppOpen() { const pc = window.__ppCash; window.__ppCash = 0; const g = ppGame(), e = (S.pp || {})[g.sl], own = g.ph.some(p => p.mine), cash = isCash() || !!pc")
RA("<p class=\"pk-rem\"><b>${ppPool(g.players)}</b> cash prize pool</p>",
   "<p class=\"pk-rem\"><b>${ppPool(g.players)}</b> cash prize pool</p>${pc && S.user && S.user.guest ? '<p class=\"pk-note\">Choose your picks and amount. You’ll create your account and add cash before you pay.</p>' : ''}")
s = s.replace('</style>', ".pk .pk-note{font-size:.84rem;opacity:.85;margin:-2px 0 8px}\n</style>", 1)
# after paying, show the "Your pick is in" screen (wait for the cash animation) and end the tutorial for cash pickers
RA("toast(free ? '🎟️ Free pick in! Watch it live.' : `🎀 ${money(st)} entry in! Watch it live.`); setTimeout(ppOpen, 300);",
   "toast(free ? '🎟️ Free pick in! Watch it live.' : `🎀 ${money(st)} pick in! Watch it live.`); if (!free && (S.tut || 9) < 9) { S.tut = 9; save(); } (function sh(t) { setTimeout(() => { if (($('#coach').classList.contains('on') || $('#sheet').classList.contains('on') || document.querySelector('.cashx, .gemx')) && t < 12) sh(t + 1); else ppOpen(); }, t ? 700 : 300); })(0);")
open(d + 'yofi-real.html', 'w').write(s); print('rm v39 ok')
