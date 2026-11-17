# Real Money build, step 36 (after rmv32.py): landing page.
#  - Photo step 3: "Win a share of the prize · finalists' creators share 10% of the pool" (was "Pick the top 3 of 6").
#  - New section "Pick the winners every hour": the live Final, its pool and closing time, with "Pick the Final · from $2".
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)

RA('<b>Pick the top 3 of 6</b><small>In the hourly Final</small>', '<b>Win a share of the prize</b><small>Finalists’ creators share 10% of the pool</small>')
TROPHY = '<svg viewBox="0 0 64 56" width="62" height="54" fill="none" aria-hidden="true"><g stroke="#E8A21C" stroke-width="3" stroke-linecap="round"><path d="M46 6l3-5M53 12l5-3M55 20h6"/></g><path d="M18 6h28v12a14 14 0 0 1-28 0z" fill="#F2B21E" stroke="#7A1638" stroke-width="3" stroke-linejoin="round"/><path d="M18 10H9a8 8 0 0 0 9 10M46 10h9a8 8 0 0 1-9 10" stroke="#7A1638" stroke-width="3" stroke-linecap="round"/><path d="M32 32v8M22 48h20M26 40h12v8H26z" stroke="#7A1638" stroke-width="3" stroke-linejoin="round"/></svg>'
RA('<div class="lp2-sec"><div class="lp2-row"><span class="lp2-ic"><svg viewBox="0 0 64 56" width="62" height="54" fill="none" aria-hidden="true"><g stroke="#E8A21C" stroke-width="3" stroke-linecap="round"><path d="M38 5l2-5',
   '<div class="lp2-sec"><div class="lp2-row"><span class="lp2-ic">' + TROPHY + '</span><div><h2>Pick the winners every hour.</h2><p>A new Final every hour. Pick the top 3 of 6 with real cash, from $2. Score 15+ to win a share of the prize pool.</p></div></div>'
   '<div class="lp2-live" id="lpLive"></div><button class="lp-btn" onclick="rmPickNow()">Pick the Final · from $2 <span aria-hidden="true">→</span></button></div>'
   '<div class="lp2-sec"><div class="lp2-row"><span class="lp2-ic"><svg viewBox="0 0 64 56" width="62" height="54" fill="none" aria-hidden="true"><g stroke="#E8A21C" stroke-width="3" stroke-linecap="round"><path d="M38 5l2-5')
s = s.replace("function fcNotify() {", r"""setInterval(() => { try { const el = document.getElementById('lpLive'); if (!el || !S || $('#landing').style.display === 'none') return; const g = ppGame();
  const h = `<span class="lv">● Live now</span><b>${raceName(g.sl)} ${esc(showName(g.k))} Final</b><span>${ppPool(g.players)} pool · ${g.players} players · closes in <b>${tLeft(g.end)}</b></span>`; if (el.innerHTML !== h) el.innerHTML = h; } catch (e) {} }, 1000);
function fcNotify() {""", 1)
s = s.replace('</style>', """.lp2-live{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:center;gap:4px 8px;background:#FFFFFF;border-radius:14px;padding:10px 12px;margin:0 0 12px;box-shadow:inset 0 0 0 1px #EADCC6;color:#2B2320;font-size:.9rem}
.lp2-live .lv{color:#C8102E;font-weight:800;font-size:.8rem}.lp2-live>b{font:800 1rem Fraunces,Georgia,serif;color:#7A1638}.lp2-live>span:last-child{width:100%;text-align:center}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v33 ok')
