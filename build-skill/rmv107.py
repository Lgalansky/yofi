# Real Money build, step 110 (after rmv106.py): your photo's journey, shown visually.
#  Track: Framed → Qualifiers (3 tries, each dot shows its place) → Finalist → Final → Paid, with the framed thumbnail on
#  the current stage.
#  - Vote screen: slim journey row under the streak bar while a photo is racing ("Next qualifier in 4 votes" with a gold
#    bar that fills as you vote). Coming-up strip unchanged.
#  - Moving-forward moment: when a qualifier runs, the row lights up with a sparkle and "3rd in its qualifier · 2 tries
#    left" or "🎀 Through to the 7pm Final!" (replaces the old toasts; the Through-to-the-Final pop stays).
#  - Gallery: each framed photo card shows the full track.
#  - Live race: your own photo's lane is marked "📷 Your photo" with a glow; the race also shows when your photo is a
#    finalist and you haven't picked.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("r.ha = Date.now(); r.f.push({ k: 'h', pl });", "r.ha = Date.now(); r.f.push({ k: 'h', pl }); S.jMove = { pid: id, pl, at: Date.now() };")
RA("""${rec.form.length ? `<p class="gl-form">Form <span class="rf">${formHTML(rec.form)}</span></p>` : ''}</div></div>${st}</div>`; };""",
   """${rec.form.length ? `<p class="gl-form">Form <span class="rf">${formHTML(rec.form)}</span></p>` : ''}</div></div>${journeyHTML(p)}${st}</div>`; };""")
# race lanes: own photo + no-pick case
RA("${e ? raceTrackHTML(g, e) : ''}${ppBoard(g, e)}", "${e || own ? raceTrackHTML(g, e) : ''}${ppBoard(g, e)}")
RA("""${g.ph.map((p, i) => { const pk = e.picks.indexOf(i);
    return `<div class="rtk-lane ${p""", """${g.ph.map((p, i) => { const pk = e ? e.picks.indexOf(i) : -1;
    return `<div class="rtk-lane ${p.mine ? 'own ' : ''}${p""")
RA("""<span class="rtk-lab">${pk >= 0 ? `<u>Your ${RT_ORD[pk]} pick</u> ` : ''}""", """<span class="rtk-lab">${p.mine ? '<u>📷 Your photo</u> ' : ''}${pk >= 0 ? `<u>Your ${RT_ORD[pk]} pick</u> ` : ''}""")
RA("const sl = +el.dataset.sl, g = ppGame(sl), e = (S.pp || {})[sl]; if (!e) return;", "const sl = +el.dataset.sl, g = ppGame(sl), e = (S.pp || {})[sl] || { picks: [], at: Date.now() - PP_DEMO / 2, sl, nop: 1 };")
RA("pv = window.__rtPrev, rem = Math.max(0, ppDue(e) - now);", "pv = window.__rtPrev, rem = Math.max(0, (e.nop ? g.end : ppDue(e)) - now);")
s = s.replace("function fcNotify() {", r"""function jStage(p) { const r = rcRec(p.id), cur = ppSlot(); if (r.st === 'heats') return 1; if (r.st === 'q') return r.sl === cur ? 3 : 2; return (r.f || []).some(z => z.k === 'r') ? 4 : 1; }
function jDots(p) { const f = rcRec(p.id).f || []; let i = f.length; while (i > 0 && f[i - 1].k === 'h') i--; const run = f.slice(i).map(z => z.pl);
  return [0, 1, 2].map(k => run[k] ? `<i class="jd ${run[k] <= 2 ? 'ok' : 'x'}">${run[k] <= 2 ? '✓' : ppOrd(run[k])}</i>` : '<i class="jd"></i>').join(''); }
function journeyHTML(p, compact) { const st = jStage(p), r = rcRec(p.id), last = r.last, labs = ['Framed', 'Qualifiers', 'Finalist', 'Final', 'Paid'];
  const sub = st === 1 ? (r.st === 'heats' ? `Next qualifier in <b>${Math.max(1, HEAT_EVERY - (S.hN || 0))} votes</b>` : 'Ready to race again') : st === 2 ? `In the <b>${raceName(r.sl)} Final</b>` : st === 3 ? '<b>Racing now</b> · watch it live' : last ? `Finished <b>${ppOrd(last.pl)}</b> · earned <b>${money(finShare(last.sl, last.pl))}</b>` : 'Ready to race again';
  return `<div class="jy ${compact ? 'jy-c' : ''}" data-pid="${p.id}"><div class="jy-tr">${labs.map((l, k) => `<span class="jy-s ${k < st ? 'done' : k === st ? 'now' : ''} ${k === 3 && st === 3 ? 'live' : ''}">${k === st ? `<img src="${p.src}" alt="">` : `<b>${k < st ? '✓' : ''}</b>`}<small>${l}</small>${k === 1 ? `<span class="jy-dots">${jDots(p)}</span>` : ''}</span>`).join('<em class="jy-ln"></em>')}</div>
    <p class="jy-sub">${sub}</p>${st === 1 && r.st === 'heats' ? `<div class="jy-bar"><i style="width:${Math.min(100, 100 * (S.hN || 0) / HEAT_EVERY)}%"></i></div>` : ''}</div>`; }
function jRowHTML() { const P = (S.photos || []).filter(p => p.framed && ['heats', 'q'].includes(rcRec(p.id).st)); if (!P.length) return '';
  const mv = S.jMove && Date.now() - S.jMove.at < 9000 ? S.jMove : null, p = (mv && P.find(x => x.id === mv.pid)) || P[0], r = rcRec(p.id);
  let chip = ''; if (mv && mv.pid === p.id) { chip = mv.pl <= 2 ? `🎀 Through to the ${raceName(r.sl)} Final!` : `${ppOrd(mv.pl)} in its qualifier · ${Math.max(0, HEAT_RUNS - (r.runs || 0))} ${HEAT_RUNS - (r.runs || 0) === 1 ? 'try' : 'tries'} left`; S.jMove = null; save(); }
  return `<button class="jrow ${chip ? 'mv' : ''}" id="jRow"><span class="jrow-h"><b>📷 ${esc(rcName(p))}</b>${chip ? `<em class="jrow-chip">${chip}</em>` : ''}</span>${journeyHTML(p, true)}${chip ? `<span class="cfx-sp">${[...Array(12)].map((_, k) => `<i style="--a:${k * 30}deg;--d:${(k % 3) * .06}s"></i>`).join('')}</span>` : ''}</button>`; }
try { const _rj0 = renderJudge; renderJudge = function () { const out = _rj0.apply(this, arguments); try { const st = document.querySelector('#judge .stk'); const old = document.getElementById('jRow'); if (old) old.remove(); if (st) { st.insertAdjacentHTML('afterend', jRowHTML()); const b = document.getElementById('jRow'); if (b) b.onclick = () => myShow(); } } catch (e) {} return out; }; } catch (e) {}
function fcNotify() {""", 1)
s = s.replace('</style>', """.jy{margin:10px 0 4px;padding:10px 8px 8px;border-radius:14px;background:#fff;box-shadow:inset 0 0 0 1.5px #EADCC6}
.jy-tr{display:flex;align-items:flex-start}.jy-ln{flex:1;height:3px;margin-top:15px;background:#E2D3BC;border-radius:2px}.jy-s.done+.jy-ln{background:#D9AE4F}
.jy-s{position:relative;display:flex;flex-direction:column;align-items:center;width:44px;flex:none}.jy-s>b{display:grid;place-items:center;width:30px;height:30px;border-radius:50%;background:#F3EDE2;box-shadow:inset 0 0 0 2px #E2D3BC;color:#fff;font-size:.85rem}
.jy-s.done>b{background:#D9AE4F;box-shadow:none}.jy-s img{width:34px;height:34px;object-fit:cover;border-radius:6px;margin-top:-2px;box-shadow:0 0 0 3px #C9962E,0 0 0 5px #F3D98B,0 4px 10px rgba(0,0,0,.3);animation:jyIn .6s cubic-bezier(.2,1.4,.4,1)}
.jy-s.live img{box-shadow:0 0 0 3px #C8102E,0 0 14px rgba(200,16,46,.6);animation:jyLive 1s ease-in-out infinite}@keyframes jyLive{50%{transform:scale(1.08)}}@keyframes jyIn{from{transform:translateX(-30px) scale(.6);opacity:0}}
.jy-s small{margin-top:4px;font-size:.62rem;font-weight:800;color:#6B5E55;text-align:center;line-height:1.1}.jy-s.now small{color:#14213D}
.jy-dots{display:flex;gap:2px;margin-top:3px}.jd{width:13px;height:13px;border-radius:50%;background:#EEE6D8;font-style:normal;font-size:.48rem;font-weight:900;display:grid;place-items:center;color:#6B5E55}.jd.ok{background:#2F6B3F;color:#fff}.jd.x{background:#E2D3BC}
.jy-sub{margin:8px 0 0;text-align:center;font-size:.86rem;color:#2B2320}.jy-sub b{color:#14213D}.jy-bar{height:7px;margin:6px 6px 0;border-radius:4px;background:#F3EDE2;overflow:hidden}.jy-bar i{display:block;height:100%;background:linear-gradient(90deg,#E9B949,#C9962E);border-radius:4px;transition:width .6s ease}
html body #judge .jrow{position:relative;display:block;width:100%;margin:10px 0 0;padding:10px 10px 8px;border:0;border-radius:16px;background:#FBF6EE;box-shadow:inset 0 0 0 1.5px #E2C27A;font:inherit;text-align:left;cursor:pointer;overflow:visible}
.jrow-h{display:flex;align-items:center;justify-content:space-between;gap:6px}.jrow-h b{font-size:.9rem;color:#14213D}.jrow .jy{margin:6px 0 0;box-shadow:none;background:transparent;padding:4px 0 0}
.jrow-chip{font-style:normal;font-weight:800;font-size:.78rem;padding:3px 10px;border-radius:999px;background:#14213D;color:#F3D98B;white-space:nowrap;animation:rtkPop .6s ease}
html body #judge .jrow.mv{animation:cfxGlow .9s ease-in-out 2}.jrow .cfx-sp{left:50%;top:55%}
.rtk-lane.own{box-shadow:inset 0 0 0 2px #F3D98B}.rtk-lane.own .rtk-run img{box-shadow:0 0 0 3px #F3D98B,0 0 16px rgba(243,217,139,.9)}
@media (prefers-reduced-motion:reduce){.jy-s img,.jy-s.live img{animation:none}}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v107 ok')
