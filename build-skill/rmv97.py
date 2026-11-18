# Real Money build, step 100 (after rmv96.py): the live Final is a race.
#  On the live pick page a race track replaces the standings list: six lanes, each finalist's photo runs toward a gold
#  finish line as the votes come in (smooth movement, updated every 1.2 s). Your picks wear gold/silver/bronze rings with
#  a "Your 1st pick" tag; each runner shows its current place. A commentary line calls the race ("Pine road takes the
#  lead!", "Your 2nd pick climbs to 2nd!", "Photo finish!"). In the last 20 seconds the track pulses "Photo finish".
#  The "Right now you'd win…" box above keeps the running cash.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA('${ppBoard(g, e)}<p class="pp-i">', '${e ? raceTrackHTML(g, e) : \'\'}${ppBoard(g, e)}<p class="pp-i">')
s = s.replace("function fcNotify() {", r"""const RT_ORD = ['1st', '2nd', '3rd', '4th', '5th', '6th'];
function raceTrackHTML(g, e) { window.__rtPrev = null; window.__rtSay = null;
  return `<div class="rtk" id="rtk" data-sl="${g.sl}"><p class="rtk-tick" id="rtkTick">🏁 And they’re off!</p><div class="rtk-track">${g.ph.map((p, i) => { const pk = e.picks.indexOf(i);
    return `<div class="rtk-lane ${pk >= 0 ? 'pk m' + pk : ''}" data-i="${i}"><span class="rtk-lab">${pk >= 0 ? `<u>Your ${RT_ORD[pk]} pick</u> ` : ''}${esc(p.t)}</span><span class="rtk-run" style="left:2%"><img src="${p.src}" alt="">${pk >= 0 ? `<i>${PP_MED[pk]}</i>` : ''}<b class="rtk-pos">–</b></span></div>`; }).join('')}<i class="rtk-fin"></i></div></div>`; }
function raceTick() { const el = document.getElementById('rtk'); if (!el || !el.closest('#coach.on')) return; const sl = +el.dataset.sl, g = ppGame(sl), e = (S.pp || {})[sl]; if (!e) return;
  const now = Date.now(), cp = 1 - (g.end - now) / PP_MS, prog = Math.min(1, Math.max(.04, Math.max(cp, (now - e.at) / PP_DEMO))), L = ppLive(g, prog), fin = Math.max(1, ...ppLive(g, 1).map(x => x.v)) * 1.04;
  const rank = {}; L.forEach((x, n) => { rank[x.i] = n + 1; });
  el.querySelectorAll('.rtk-lane').forEach(ln => { const i = +ln.dataset.i, x = L.find(z => z.i === i), r = ln.querySelector('.rtk-run'); r.style.left = `${Math.min(84, 2 + 82 * x.v / fin).toFixed(1)}%`; const b = r.querySelector('.rtk-pos'); b.textContent = RT_ORD[rank[i] - 1]; b.className = 'rtk-pos' + (rank[i] <= 3 ? ' top' : ''); ln.classList.toggle('lead', rank[i] === 1); });
  const pv = window.__rtPrev, rem = Math.max(0, ppDue(e) - now); let say = null;
  if (pv) { const lead = L[0].i; if (pv[lead] !== 1) say = `🔥 ${g.ph[lead].t} takes the lead!`;
    e.picks.forEach((i, k) => { if (say) return; if (rank[i] < pv[i]) say = rank[i] === k + 1 ? `✓ Your ${RT_ORD[k]} pick hits its exact spot!` : `⬆ Your ${RT_ORD[k]} pick climbs to ${RT_ORD[rank[i] - 1]}!`; else if (rank[i] > pv[i] && pv[i] <= 3 && rank[i] > 3) say = `⬇ Your ${RT_ORD[k]} pick drops out of the top 3`; }); }
  if (rem < 20000) { el.classList.add('fin'); say = `🏁 Photo finish! ${Math.ceil(rem / 1000)}s to go`; }
  window.__rtPrev = rank; const t = document.getElementById('rtkTick');
  if (say) { window.__rtSay = Date.now(); if (t.textContent !== say) { t.textContent = say; t.classList.remove('pop'); void t.offsetWidth; t.classList.add('pop'); } }
  else if (!window.__rtSay || Date.now() - window.__rtSay > 4000) { const tot = L.reduce((a, x) => a + x.v, 0), msgs = [`🗳️ ${tot.toLocaleString()} votes in · ${g.ph[L[0].i].t} leads`, `${g.ph[L[0].i].t} and ${g.ph[L[1].i].t} neck and neck`, `👀 ${g.players} players watching`]; t.textContent = msgs[Math.floor(now / 4000) % msgs.length]; t.classList.remove('pop'); } }
setInterval(raceTick, 1200);
function fcNotify() {""", 1)
s = s.replace('</style>', """.rtk{margin:4px 0 12px;border-radius:18px;background:#14213D;padding:10px 10px 12px;box-shadow:0 0 0 2px #D9AE4F}
.rtk-tick{margin:0 0 8px;padding:6px 10px;border-radius:999px;background:rgba(255,255,255,.08);color:#F3D98B;font-weight:800;font-size:.9rem;text-align:center;min-height:1.3em}
html body .ppop .rtk-tick{color:#F3D98B!important;-webkit-text-fill-color:#F3D98B}.rtk-tick.pop{animation:rtkPop .5s ease}@keyframes rtkPop{0%{transform:scale(.9);opacity:.3}60%{transform:scale(1.05)}100%{transform:none;opacity:1}}
.rtk-track{position:relative;display:flex;flex-direction:column;gap:6px;padding-right:10px}
.rtk-fin{position:absolute;top:-2px;bottom:-2px;right:0;width:10px;border-radius:3px;background:repeating-conic-gradient(#fff 0 25%,#14213D 0 50%) 0 0/10px 10px;box-shadow:0 0 0 1.5px #D9AE4F}
.rtk-lane{position:relative;height:58px;border-radius:12px;background:linear-gradient(90deg,rgba(255,255,255,.05),rgba(255,255,255,.12));box-shadow:inset 0 -1px 0 rgba(255,255,255,.08)}.rtk-lane.pk{background:linear-gradient(90deg,rgba(217,174,79,.12),rgba(217,174,79,.28))}
.rtk-lab{position:absolute;left:10px;top:3px;font-size:.66rem;font-weight:700;color:rgba(255,255,255,.7);white-space:nowrap;max-width:60%;overflow:hidden;text-overflow:ellipsis}html body .ppop .rtk-lab{color:rgba(255,255,255,.75)!important;-webkit-text-fill-color:rgba(255,255,255,.75)}.rtk-lab u{text-decoration:none;color:#F3D98B;-webkit-text-fill-color:#F3D98B}
.rtk-run{position:absolute;top:21px;display:flex;align-items:center;gap:4px;transition:left 1.15s cubic-bezier(.3,.8,.4,1)}.rtk-run img{width:32px;height:32px;border-radius:50%;object-fit:cover;box-shadow:0 0 0 2px #fff,0 3px 8px rgba(0,0,0,.5)}
.rtk-lane.m0 .rtk-run img{box-shadow:0 0 0 3px #E9B949,0 0 12px rgba(233,185,73,.8)}.rtk-lane.m1 .rtk-run img{box-shadow:0 0 0 3px #C9D1DB,0 0 12px rgba(201,209,219,.7)}.rtk-lane.m2 .rtk-run img{box-shadow:0 0 0 3px #C8834A,0 0 12px rgba(200,131,74,.7)}
.rtk-run i{position:absolute;left:21px;top:17px;font-style:normal;font-size:.8rem}
.rtk-pos{font-size:.7rem;font-weight:900;color:#14213D;background:rgba(255,255,255,.75);border-radius:999px;padding:1px 6px}.rtk-pos.top{background:#F3D98B}html body .ppop .rtk-pos{-webkit-text-fill-color:#14213D}
.rtk-lane.lead .rtk-run img{animation:rtkLead 1s ease-in-out infinite}@keyframes rtkLead{50%{transform:translateY(-3px)}}
.rtk.fin{animation:rtkFin 1s ease-in-out infinite}@keyframes rtkFin{50%{box-shadow:0 0 0 3px #F3D98B,0 0 22px rgba(243,217,139,.6)}}
html body #coach .rtk ~ .rb .rb-r{display:none}
@media (prefers-reduced-motion:reduce){.rtk-run{transition:none}.rtk.fin,.rtk-lane.lead .rtk-run img{animation:none}}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v97 ok')
