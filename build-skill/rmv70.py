# Real Money build, step 73 (after rmv69.py): live pick page highlights the ticket, the prize and the countdown.
#  - Ticket-style confirmation: "🎟️ Free pick confirmed" / "Your free $2.00 pick is in!" with your 1st/2nd/3rd thumbnails.
#  - Two big tiles: green cash prize pool (+ players) and a ticking "Results in m:ss".
#  - Results now open from this page when the countdown hits 0 (before, results waited for the pop to close, so it sat at 0:00).
#  - Duplicate "results in" in the status box and the stale "Results at 13:39" line removed.
import os, re
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("""<h2 class="pp-h">${e ? (e.free ? `Your free ${money(e.stake || 1)} pick is in!` : `Your ${money(e.stake || 1)} pick is in!`) : 'Your photo is in the ring!'}</h2><p class="pp-m"><b>${ppPool(g.players)}</b> pool · ${g.players} players · ends ${frTime(g.end)}</p>""",
   """${e ? `<div class="lk-tk"><span class="lk-k">🎟️ ${e.free ? 'Free pick confirmed' : 'Pick confirmed'}</span><b class="lk-h">${e.free ? `Your free ${money(e.stake || 2)} pick is in!` : `Your ${money(e.stake || 2)} pick is in!`}</b>
        <span class="lk-ph">${e.picks.map((p, i) => `<i><img src="${g.ph[p].src}" alt=""><em>${PP_MED[i]} ${['1st', '2nd', '3rd'][i]}</em></i>`).join('')}</span></div>
        <div class="lk-row"><div class="lk-pz"><small>Cash prize pool</small><b>${ppPool(e.players || g.players)}</b><span>${e.players || g.players} players</span></div><div class="lk-cd"><small>Results in</small><b class="rb-cd" data-due="${ppDue(e)}" data-sl="${e.sl}">${(() => { const r = Math.max(0, ppDue(e) - Date.now()); return `${Math.floor(r / 60000)}:${String(Math.floor(r / 1000) % 60).padStart(2, '0')}`; })()}</b><span>${raceName(g.sl)} Final</span></div></div>`
        : `<h2 class="pp-h">Your photo is in the ring!</h2><p class="pp-m"><b>${ppPool(g.players)}</b> pool · ${g.players} players · ends ${frTime(g.end)}</p>`}""")
RA("""${e ? `Results at ${frTime(ppDue(e))} <small>(demo: about 2 min)</small>` :""", """${e ? `<small>Demo: results arrive about 2 minutes after you pick.</small>` :""")
i = s.index("function rbStatus"); j = s.index("</small></div>`; }", i)
seg = s[i:j]; k = seg.index(" · results in <span class=\"rb-cd\""); s = s[:i] + seg[:k] + s[j:]
RA("""setInterval(() => { document.querySelectorAll('.rb-cd').forEach(el => { const r = Math.max(0, +el.dataset.due - Date.now()); el.textContent = `${Math.floor(r / 60000)}:${String(Math.floor(r / 1000) % 60).padStart(2, '0')}`; }); }, 1000);""",
   """setInterval(() => { document.querySelectorAll('.rb-cd').forEach(el => { const r = Math.max(0, +el.dataset.due - Date.now()); el.textContent = r ? `${Math.floor(r / 60000)}:${String(Math.floor(r / 1000) % 60).padStart(2, '0')}` : 'Now!';
    if (!r && el.dataset.sl && el.closest('#coach.on')) { const e = (S.pp || {})[el.dataset.sl]; if (e && !e.done && !e.__rv) { el.removeAttribute('data-sl'); setTimeout(() => { popClose(); window.__uiT = 0; setTimeout(() => ppResult(e), 300); }, 900); } } }); }, 1000);""")
s = s.replace('</style>', """.lk-tk{position:relative;margin:6px 0 10px;padding:12px 14px 12px;border-radius:16px;background:#FFF6DF;box-shadow:inset 0 0 0 2px #D9AE4F;text-align:center}
.lk-tk::before,.lk-tk::after{content:'';position:absolute;top:50%;width:18px;height:18px;margin-top:-9px;border-radius:50%;background:#FBF7F0;box-shadow:inset 0 0 0 2px #D9AE4F}.lk-tk::before{left:-9px}.lk-tk::after{right:-9px}
.lk-k{display:block;font-weight:900;letter-spacing:.12em;text-transform:uppercase;font-size:.78rem;color:#2F6B3F}html body .ppop .lk-h{display:block;font:800 1.65rem/1.1 Fraunces,Georgia,serif;color:#14213D!important;-webkit-text-fill-color:#14213D;margin:4px 0 8px}
.lk-ph{display:flex;justify-content:center;gap:8px}.lk-ph i{position:relative;width:72px;font-style:normal}.lk-ph img{width:72px;height:56px;object-fit:cover;border-radius:10px;display:block}.lk-ph em{display:block;font-style:normal;font-weight:800;font-size:.76rem;margin-top:2px;color:#14213D}
.lk-row{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:0 0 10px}.lk-row>div{border-radius:16px;padding:10px 6px;text-align:center}.lk-row small{display:block;font-weight:900;letter-spacing:.1em;text-transform:uppercase;font-size:.7rem}.lk-row span{display:block;font-size:.82rem;margin-top:2px}
.lk-pz{background:#E6F0DF;box-shadow:inset 0 0 0 2px #2F6B3F}html body .ppop .lk-pz small,html body .ppop .lk-pz b{color:#2F6B3F!important;-webkit-text-fill-color:#2F6B3F}.lk-pz b{display:block;font:900 2.2rem/1.05 Fraunces,Georgia,serif}
.lk-cd{background:#1E3A6E}html body .ppop .lk-cd small,html body .ppop .lk-cd span{color:#DCE5F4!important;-webkit-text-fill-color:#DCE5F4}html body .ppop .lk-cd b{display:block;font:900 2.2rem/1.05 Fraunces,Georgia,serif;color:#F3D98B!important;-webkit-text-fill-color:#F3D98B;font-variant-numeric:tabular-nums}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v70 ok')
