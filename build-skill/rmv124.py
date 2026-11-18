# Real Money build, step 127 (after rmv123.py): pick screens keep their place; bigger badges.
#  - Tapping a photo (or a stake) on the Top 3 or Winner pick screen redrew the pop and jumped back to the top.
#    The redraw now keeps the scroll position.
#  - Pick medals (🥇🥈🥉 / 🏆) on the photos are bigger, with a white disc behind them; Form chips are bigger.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
# popOpen: keep scroll when asked (window.__keepScroll set just before a redraw)
RA("function popOpen(html) { if ($('#sheet').classList.contains('on')) closeSheet(); const c = $('#coach'); c.innerHTML =",
   "function popOpen(html) { if ($('#sheet').classList.contains('on')) closeSheet(); const c = $('#coach'), keep = window.__keepScroll && c.classList.contains('on'); window.__keepScroll = 0; const sy = keep ? [c.scrollTop, (c.querySelector('.ppop') || {}).scrollTop || 0] : null; c.innerHTML =")
RA("c.classList.add('on', 'cr'); c.onclick = e => { if (e.target === c) popClose(); }; }",
   "c.classList.add('on', 'cr'); c.onclick = e => { if (e.target === c) popClose(); }; if (sy) { c.scrollTop = sy[0]; const pp = c.querySelector('.ppop'); if (pp) pp.scrollTop = sy[1]; } }")
RA("if (n >= 0) picks.splice(n, 1); else if (picks.length < 3) picks.push(i); draw(); });",
   "if (n >= 0) picks.splice(n, 1); else if (picks.length < 3) picks.push(i); window.__keepScroll = 1; draw(); });", 3)
RA("b.onclick = () => { stake = +b.dataset.rst; S.raceSt = stake; save(); draw(); });",
   "b.onclick = () => { stake = +b.dataset.rst; S.raceSt = stake; save(); window.__keepScroll = 1; draw(); });")
RA("b.onclick = () => { pick = +b.dataset.wp; draw(); });", "b.onclick = () => { pick = +b.dataset.wp; window.__keepScroll = 1; draw(); });")
RA("b.onclick = () => { stake = +b.dataset.wst; S.raceSt = stake; save();", "b.onclick = () => { stake = +b.dataset.wst; S.raceSt = stake; save(); window.__keepScroll = 1;")
s = s.replace('</style>', """html body .pp-g .pp-b{font-size:3.4rem!important;width:76px;height:76px;display:grid;place-items:center;border-radius:50%;background:rgba(255,255,255,.92);box-shadow:0 4px 14px rgba(20,33,61,.35)}
html body .pp-g.g9 .pp-b{font-size:2.6rem!important;width:58px;height:58px}
html body .rf b{min-width:21px!important;height:21px!important;font-size:.8rem!important;border-radius:5px!important}
html body .rf .rf-l{font-size:.72rem}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v124 ok')
# keep "🔥 13%" on one line next to the bigger Form chips
s = open(d + 'yofi-real.html').read()
s = s.replace('</style>', """html body .pp-g [data-pp]{position:relative}
html body .pp-g [data-pp] .pp-cap .pop{position:absolute!important;right:6px;top:6px;margin:0!important;display:inline-flex!important;align-items:center;gap:2px;white-space:nowrap;font-style:normal;font-weight:900;font-size:.85rem!important;padding:3px 8px;border-radius:999px;background:#14213D!important;color:#F3D98B!important;-webkit-text-fill-color:#F3D98B;box-shadow:0 0 0 1.5px #D9AE4F}
html body .pp-cap .rf{gap:4px!important;white-space:nowrap}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v124 pass2 ok')
