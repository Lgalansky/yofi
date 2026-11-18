# Real Money build, step 120 (after rmv116.py): all your picks on one race.
#  - Race lanes carry every tag you have on that photo: "Your 1st pick" (Top 3), "🏆 Your winner", "📷 Your photo".
#  - Under the race, "Your picks in this Final" updates live: Top 3 (stake, "right now ~$X" or what it still needs),
#    Winner (photo, stake, odds, running position), your photo (running position).
#  - If you only have one kind of pick, a button adds the other ("🏆 Add a winner pick" / "🎯 Add a Top 3 pick").
#  Same panel on the Top 3 live page and the Winner live page.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("${e || own ? raceTrackHTML(g, e) : ''}", "${e || own ? raceTrackHTML(g, e) + '<div class=\"myp\" id=\"myPk\"></div>' : ''}")
RA("${raceTrackHTML(g, { picks: [w.pick], win: 1 })}", "${raceTrackHTML(g, { picks: [w.pick], win: 1 })}<div class=\"myp\" id=\"myPk\"></div>")
RA("<span class=\"rtk-lab\">${p.mine ? '<u>📷 Your photo</u> ' : ''}${pk >= 0 ? `<u>${e && e.win ? 'Your winner pick' : `Your ${RT_ORD[pk]} pick`}</u> ` : ''}",
   "<span class=\"rtk-lab\">${laneTags(g.sl, i, p)}")
RA('return `<div class="rtk-lane ${p.mine ? \'own \' : \'\'}${pk >= 0 ? \'pk m\' + pk : \'\'}"',
   'return `<div class="rtk-lane ${p.mine ? \'own \' : \'\'}${pk >= 0 ? \'pk m\' + pk : (S.pw || {})[g.sl] && S.pw[g.sl].pick === i ? \'pk m0\' : \'\'}"')
RA("window.__rtPrev = rank; const t = document.getElementById('rtkTick');", "window.__rtPrev = rank; myPicksPaint(g, L); const t = document.getElementById('rtkTick');")
s = s.replace("function fcNotify() {", r"""function laneTags(sl, i, p) { const T = (S.pp || {})[sl], W = (S.pw || {})[sl], k = T ? T.picks.indexOf(i) : -1, t = [];
  if (p.mine) t.push('📷 Your photo'); if (k >= 0) t.push(`Your ${RT_ORD[k]} pick`); if (W && W.pick === i) t.push('🏆 Your winner');
  return t.length ? `<u>${t.join(' · ')}</u> ` : ''; }
function myPicksPaint(g, L) { const el = document.getElementById('myPk'); if (!el) return; const sl = g.sl, T = (S.pp || {})[sl], W = (S.pw || {})[sl], rank = {}; L.forEach((x, n) => { rank[x.i] = n + 1; });
  const own = g.ph.findIndex(p => p.mine), rows = [];
  if (T) { const gl = Object.assign({}, g, { ord: L.map(x => x.i) }), TR = ppTiers(T, gl), pos = T.picks.map(i => rank[i]), ex = T.picks.filter((p, k) => pos[k] === k + 1).length, inT = pos.filter(x => x <= 3).length;
    rows.push(`<div class="myp-r ${TR.prize ? 'w' : ''}"><span class="myp-i">🎯</span><span class="myp-t"><b>Top 3 · ${T.free ? 'free pick' : money(T.stake || 2)}</b><small>${T.picks.map((i, k) => `${PP_MED[k]} ${esc(g.ph[i].t)} <em>${RT_ORD[rank[i] - 1]}</em>`).join(' · ')}</small></span><em class="myp-s">${TR.prize ? `~${money(TR.prize)}` : `${inT}/3 top · ${ex} exact`}</em></div>`); }
  if (W) { const r = rank[W.pick], od = winOdds(g)[W.pick];
    rows.push(`<div class="myp-r ${r === 1 ? 'w' : ''}"><span class="myp-i">🏆</span><span class="myp-t"><b>Winner · ${esc(g.ph[W.pick].t)}</b><small>${W.free ? 'Free pick' : money(W.stake || 2)} · ${od}× now</small></span><em class="myp-s">${r === 1 ? `Leading · ~${money((W.stake || 2) * od)}` : `Running ${RT_ORD[r - 1]}`}</em></div>`); }
  if (own >= 0) rows.push(`<div class="myp-r ${rank[own] <= 3 ? 'w' : ''}"><span class="myp-i">📷</span><span class="myp-t"><b>Your photo · ${esc(g.ph[own].t)}</b><small>Finalists’ creators share 10% of the pool</small></span><em class="myp-s">Running ${RT_ORD[rank[own] - 1]}</em></div>`);
  const add = !W ? '<button class="btn block myp-add" data-myw>🏆 Add a winner pick</button>' : !T && own < 0 ? '<button class="btn block myp-add" data-myt>🎯 Add a Top 3 pick</button>' : '';
  const h = rows.length ? `<p class="myp-h">Your picks in this Final</p>${rows.join('')}${add}` : '';
  if (el.__h !== h) { el.__h = h; el.innerHTML = h; const bw = el.querySelector('[data-myw]'), bt = el.querySelector('[data-myt]'); if (bw) bw.onclick = () => winOpen(true); if (bt) bt.onclick = () => { popClose(); window.__ppCash = 1; setTimeout(ppOpen, 150); }; } }
function fcNotify() {""", 1)
s = s.replace('</style>', """.myp{margin:0 0 10px}.myp-h{margin:4px 0 6px;font-weight:900;letter-spacing:.1em;text-transform:uppercase;font-size:.76rem;color:#14213D;text-align:left}
.myp-r{display:flex;align-items:center;gap:10px;padding:9px 10px;margin:0 0 6px;border-radius:12px;background:#fff;box-shadow:inset 0 0 0 1.5px #EADCC6;text-align:left}.myp-r.w{box-shadow:inset 0 0 0 2px #2F6B3F;background:#F1F6EC}
.myp-i{font-size:1.3rem;flex:none}.myp-t{flex:1;min-width:0;display:flex;flex-direction:column}html body #coach .myp-t b{font:800 .95rem Nunito,system-ui,sans-serif!important;color:#14213D!important;-webkit-text-fill-color:#14213D}.myp-t small{font-size:.74rem;line-height:1.35}.myp-t small em{font-style:normal;font-weight:800;color:#1E3A6E}
.myp-s{font-style:normal;font-weight:900;font-size:.82rem;color:#14213D;white-space:nowrap}.myp-r.w .myp-s{color:#2F6B3F}
html body .ppop .btn.myp-add{background:#2F6B3F!important;color:#fff!important;margin-top:4px}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v117 ok')
