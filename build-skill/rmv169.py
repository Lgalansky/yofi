# Real Money build, step 172 (after rmv168.py): cleanup from the owner's play-through.
#  - The old qualifier system (heats → "Through to the Final! … 10% of the prize pool") and its old hourly-race results
#    are switched off for good, including for photos left over in saved games.
#  - "Your rivals": big photo tiles (3 across) so you can see who you're racing.
#  - Vote screen: the coin countdown bar is gone. Coins show in the wallet; the entry cost appears when you enter a photo.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
s = s.replace("function fcNotify() {", r"""function rcHeat() { return; }
function rcQualPop() { return; }
function raceOwnResult() { return; }
try { if (S) { S.rcPop = null; S.races = {}; (S.photos || []).forEach(p => { try { const r = rcRec(p.id); if (r && (r.st === 'heats' || r.st === 'q')) r.st = null; } catch (e) {} }); save(); } } catch (e) {}
function vrQuiet(n, ok, pay) { try { paintGems(); gemExplosion(pay, { label: 'Round bonus' }); } catch (e) {}
  setTimeout(() => { try { vrPaint(); } catch (e) {} const top = document.getElementById('vrTop'); if (!top) return; const o = document.getElementById('vrQ'); if (o) o.remove();
    top.insertAdjacentHTML('afterend', `<div class="vrqb" id="vrQ">✓ <b>+${pay} 🟡 round bonus</b></div>`);
    setTimeout(() => { const e = document.getElementById('vrQ'); if (e) { e.classList.add('bye'); setTimeout(() => e.remove(), 400); } }, 3200); }, 50); }
function fcNotify() {""", 1)
s = s.replace('</style>', """html body #vrTop{display:none!important}
html body .qfp-l{grid-template-columns:repeat(3,1fr);gap:8px}html body .qfp-l>div{flex-direction:column;align-items:stretch;gap:4px;padding:6px;text-align:center}
html body .qfp-l img{width:100%;height:auto;aspect-ratio:1;border-radius:10px}html body .qfp-l b{font-size:.86rem;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
html body .qfp-l small{display:block;font-size:.66rem;line-height:1.3}html body .qfp-l>div.me img{box-shadow:0 0 0 3px #D9AE4F}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v169 ok')
# pass 2: even rival tiles — equal columns, short captions ("@handle · 8–2")
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("<small>You · qualified ${me.w}–${me.l}</small>", "<small>You · ${me.w}–${me.l}</small>")
RA("<small>${esc(x.h)} · qualified ${x.w}–${x.l}</small>", "<small>${esc(x.h)} · ${x.w}–${x.l}</small>")
s = s.replace('</style>', """html body .qfp-l{grid-template-columns:repeat(3,minmax(0,1fr))}html body .qfp-l small{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v169 pass2 ok')
