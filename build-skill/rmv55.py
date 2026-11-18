# Real Money build, step 58 (after rmv54.py): "play for real" upsells, always green; picker first, deposit after.
#  - Free Final pick WIN (coin player): gold box "A $10 pick would have won $X" with $2/$5/$10 tiles + green
#    "Pick the next Final for real · from $2" (at most once every 30 min; otherwise a plain green second button).
#  - Free Final pick LOSS: quiet green outline "Pick the next Final · from $2" under "View next Final".
#  - The green button opens the live Final's picker with cash amounts; sign-up / add cash happen when they pay.
#  - Quick Sprint (coins): after a win, "Same game for real: $2 wins $3.20"; after a loss, no box (button stays).
#  - Every real-money button is green (pc-real, depositor qualifier button, wallet/cash picks).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

RA('<button class="btn block fr2-next" id="ppNext">View next Final →</button>',
   '${frUpsell(e, prize, st)}<button class="btn block fr2-next" id="ppNext">View next Final →</button>${e.free && !prize && !isCash() ? \'<button class="btn block up-ghost" id="ppReal2">Pick the next Final · from $2</button>\' : \'\'}')
RA("$('#ppNext').onclick = () => { popClose(); raceCard(); };",
   "$('#ppNext').onclick = () => { popClose(); raceCard(); }; document.querySelectorAll('#ppReal1, #ppReal2').forEach(b => b.onclick = () => { popClose(); setTimeout(() => { window.__ppCash = 1; ppOpen(); }, 250); });")
s = s.replace("function fcNotify() {", r"""function frUpsell(e, prize, st) { if (!e.free || !prize || isCash()) return ''; const now = Date.now(), big = !S.upAt || now - S.upAt > 30 * 60000, x = v => money(prize * v / (st || 2)), g = ppGame();
  if (!big) return '<button class="btn block up-go" id="ppReal1">💵 Pick the next Final for real · from $2</button>';
  S.upAt = now; save();
  return `<div class="up-box"><p class="up-t">A $10 pick would have won <b>${x(10)}</b></p><small>Same picks, real stake. The ${raceName(g.sl)} ${esc(showName(g.k))} Final is open now.</small>
    <div class="up-rows"><span>$2 pick<b>${x(2)}</b></span><span>$5 pick<b>${x(5)}</b></span><span>$10 pick<b>${x(10)}</b></span></div></div>
    <button class="btn block up-go" id="ppReal1">💵 Pick the next Final for real · from $2</button>`; }
function fcNotify() {""", 1)
# Quick Sprint coin result: win-only box
RA("const up = pr ? `<div class=\"qs3-up\"><span class=\"qs3-upi\">🎯</span><div><b>Ready for real cash?</b><small>$2 entry · 1 vs 1 · winner gets <b>${qsM(qsPay(2)[0])}</b></small></div></div>`",
   "const up = pr ? (won ? `<div class=\"qs3-up up-box\"><span class=\"qs3-upi\">💵</span><div><b>Same game for real: $2 wins ${qsM(qsPay(2)[0])}</b><small>1 v 1 against a real player · up to $20 wins ${qsM(qsPay(20)[0])}</small></div></div>` : '')")
RA("<button class=\"btn block qs3-real\" id=\"qsReal\">💵 Play for real · win ${qsM(qsPay(2)[0])}</button>", "<button class=\"btn block qs3-real\" id=\"qsReal\">💵 Play for real · $2</button>")

G = '#2F6B3F'
P = 'html:not(.yg) body'
s = s.replace('</style>', f"""{P} .ppop .btn.pc-real,{P} .ppop .btn.up-go,{P} .btn.qs3-real,{P} .ppop .btn.g2-fin.cashb,{P} #coach .btn.pk-go.cashb{{background:{G}!important;background-image:none!important;color:#fff!important;-webkit-text-fill-color:#fff!important;box-shadow:0 6px 16px -8px rgba(47,107,63,.7)!important}}
{P} .ppop .btn.up-ghost{{background:transparent!important;color:{G}!important;-webkit-text-fill-color:{G};box-shadow:inset 0 0 0 2px {G}!important;font-size:1rem!important}}
.up-box{{border-radius:18px;padding:12px 14px;margin:6px 0 10px;text-align:left;background:#FFF6DC;box-shadow:inset 0 0 0 1.5px #E8C46A}}.up-t{{font:800 1.12rem/1.2 Fraunces,Georgia,serif;margin:0 0 4px;color:#2B2320}}.up-t b{{color:{G}}}.up-box small{{display:block;font-size:.84rem;opacity:.85}}
.up-rows{{display:flex;gap:6px;margin:8px 0 2px}}.up-rows span{{flex:1;background:#fff;border-radius:10px;padding:6px 4px;text-align:center;font-size:.78rem;box-shadow:inset 0 0 0 1px #EADCC6}}.up-rows b{{display:block;font:800 1rem Fraunces,Georgia,serif;color:{G}}}
.qs3-up.up-box b{{color:#2B2320}}
</style>""", 1)
# depositor qualifier button + cash pick buttons get the green class
RA("if (isCash()) return `<button class=\"btn block g2-fin\" id=\"gtFin\">", "if (isCash()) return `<button class=\"btn block g2-fin cashb\" id=\"gtFin\">")
RA("<button class=\"btn block pc-go pk-go\" id=\"ppGo\"", "<button class=\"btn block pc-go pk-go cashb\" id=\"ppGo\"")
open(d + 'yofi-real.html', 'w').write(s); print('rm v55 ok')
