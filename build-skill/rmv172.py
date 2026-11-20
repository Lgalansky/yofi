# Real Money build, step 175 (after rmv171.py): voting streaks move your photos; 3-2-1 before the qualifier race.
#  - Your photo moves 1 step only when you vote 3 correct (with the crowd) in a row. 3 steps to the start line.
#    The card shows 3 streak dots (filled per correct vote, reset on a miss) and "Step 2 of 3" instead of text.
#  - Start line reached → full screen: your photo vs the rival, "3 · 2 · 1 · GO!", then the live 2-horse race.
#  - Once qualified, the same streak steps (3) take the photo to its Final; then the rivals & entry screen opens.
#    Any Final entry (stable, My Photos) goes through these steps.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA('<button class="btn block db-go cashb" id="qlvGo">🏁 See your rivals & race</button>', '<button class="btn block db-go cashb" id="qlvGo">⚖️ Vote your way to the Final</button>', 2)
RA("const iv = setInterval(() => { if (!document.getElementById('qrN'))", "const run = () => { const iv = setInterval(() => { if (!document.getElementById('qrN'))")
RA("}), 500); }, 380); }", "}), 500); }, 380); }; qrCount(p, o, oh, run); }")
s = s.replace("function fcNotify() {", r"""const QS_STEPS = 3, QS_RUN = 3;
try { (S.photos || []).forEach(p => { const q = p.ql; if (q && !q.done && !q.gv) { q.got = Math.min(QS_STEPS - 1, Math.floor((q.got || 0) * QS_STEPS / 10)); q.gv = 2; q.live = 0; } }); } catch (e) {}
function qlStep() { return; }
const qsWhenFree = fn => setTimeout(function tm() { if (document.querySelector('#coach.on, #sheet.on, #flow.on, #finPick.on, #ageGate.on, .chx') || window.__qlLive) { setTimeout(tm, 1000); return; } fn(); }, 1000);
(() => { const cf = callFx; callFx = function (pick, pct, agree) { const r = cf.apply(this, arguments); try {
  S.stk = agree ? (S.stk || 0) + 1 : 0;
  if (S.stk >= QS_RUN) { S.stk = 0; let moved = 0;
    (S.photos || []).forEach(p => { const q = p.ql;
      if (q && !q.done && !q.live && !p.tr) { q.got = (q.got || 0) + 1; moved++; if (q.got >= QS_STEPS) { q.live = 1; qsWhenFree(() => qlRace(p)); } }
      else if (p.fin && p.fr && !p.fr.go) { p.fr.s = (p.fr.s || 0) + 1; moved++; if (p.fr.s >= QS_STEPS) { p.fr.go = 1; qsWhenFree(() => qfStart(p)); } } });
    if (moved) { try { toast('🐎 3 in a row · your photo moves on!'); } catch (e) {} } }
  save(); qlPaint(); } catch (e) {} return r; }; })();
(() => { const qs = qfStart; qfStart = function (p) { if (!p) return; if (!(p.fr && p.fr.s >= QS_STEPS)) { p.fin = 1; p.fr = p.fr || { s: 0 }; save(); try { popClose(); } catch (e) {} try { closeFlow(); } catch (e) {}
    go('judge'); renderJudge(); toast(`🏁 Vote 3 in a row to move ${rcName(p)} on · ${QS_STEPS - (p.fr.s || 0)} steps to the Final`); return; }
  return qs.apply(this, arguments); }; })();
(() => { const qr = qfResult; qfResult = function (p) { p.fr = null; return qr.apply(this, arguments); }; })();
function qrCount(p, o, oh, run) { const box = document.querySelector('.qrx'); if (!box) { run(); return; }
  box.insertAdjacentHTML('beforeend', `<div class="qr-cd" id="qrCd"><p class="pp-k">🎀 Qualifier race</p><div class="qr-vs"><div><img src="${p.src}" alt=""><b>${esc(rcName(p))}</b><small>You</small></div><span>VS</span><div><img src="${o.src}" alt=""><b>${esc(o.t)}</b><small>${esc(oh)}</small></div></div><b class="qr-num" id="qrNum">3</b><p class="qr-sub">First to ${QR_WIN} votes goes to the Final</p></div>`);
  let n = 3; const t = setInterval(() => { const e = document.getElementById('qrNum'); if (!e) { clearInterval(t); return; } n--; e.textContent = n > 0 ? n : 'GO!'; e.classList.remove('go'); void e.offsetWidth; e.classList.add('go');
    if (n <= 0) { clearInterval(t); setTimeout(() => { const c = document.getElementById('qrCd'); if (c) { c.classList.add('bye'); setTimeout(() => c.remove(), 350); } run(); }, 650); } }, 850); }
function pvStep(p, s, fin) { const pos = Math.min(1, s / QS_STEPS), k = S.stk || 0;
  return `<div class="pv-tr"><div class="pv-rail">${Array.from({ length: QS_STEPS - 1 }, (_, i) => `<i style="left:${(i + 1) / QS_STEPS * 100}%"></i>`).join('')}<u style="width:${pos * 100}%"></u></div>
      <img class="pv-hz" src="${p.src}" alt="" style="left:calc(${pos} * (100% - 40px))"><span class="pv-fl">🏁</span></div>
    <div class="pv-k"><span class="pv-dots">${[0, 1, 2].map(i => `<i class="${i < k ? 'on' : ''}"></i>`).join('')}</span><b>Step ${Math.min(QS_STEPS, s)} of ${QS_STEPS}${fin ? ' to the Final' : ''}</b></div>`; }
(() => { const pc = pvCard; pvCard = function (p) { const q = p.ql;
  if (q && !q.done && !p.tr) return `<div class="pv-c" data-pid="${p.id}"><div class="pv-t"><b>${esc(rcName(p))}</b><span class="pv-st">${q.live ? '<i>●</i> Qualifier race · live' : '🎀 Qualifier'}</span><em>🟡 +${p.qc || 0}</em></div>${pvStep(p, q.got || 0, 0)}</div>`;
  if (p.fin) { p.fr = p.fr || { s: 0 }; return `<div class="pv-c fin" data-pid="${p.id}"><div class="pv-t"><b>${esc(rcName(p))}</b><span class="pv-st">🏆 Finalist</span><em>🟡 +${p.qc || 0}</em></div>${pvStep(p, p.fr.s || 0, 1)}</div>`; }
  return pc.apply(this, arguments); }; })();
function fcNotify() {""", 1)
s = s.replace('</style>', """.pv-k{display:flex;align-items:center;gap:10px;margin-top:2px}.pv-k b{margin-left:auto;font:800 .78rem Nunito,system-ui;color:#14213D}
.pv-dots{display:flex;gap:6px}.pv-dots i{width:14px;height:14px;border-radius:50%;background:#E6EFE2;box-shadow:inset 0 0 0 1.5px #B9CDB2;transition:background .2s,transform .2s}.pv-dots i.on{background:#2F6B3F;box-shadow:none;transform:scale(1.12)}
.pv-c.fin .pv-dots i.on{background:#D9AE4F}
.qrx{position:relative}.qr-cd{position:absolute;inset:0;z-index:5;display:flex;flex-direction:column;align-items:center;justify-content:center;background:#FBF6EE;border-radius:inherit;transition:opacity .35s}.qr-cd.bye{opacity:0}
.qr-vs{display:grid;grid-template-columns:1fr auto 1fr;gap:10px;align-items:center;width:100%;margin:8px 0}.qr-vs>div{display:flex;flex-direction:column;align-items:center;gap:4px;min-width:0}
.qr-vs img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:14px;box-shadow:0 0 0 3px #EADCC6}.qr-vs>div:first-child img{box-shadow:0 0 0 3px #D9AE4F}
.qr-vs b{font:800 .9rem Fraunces,Georgia,serif;color:#14213D;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.qr-vs small{font:700 .72rem Nunito,system-ui;color:#5B4A3F}
.qr-vs>span{font:900 1rem Fraunces,Georgia,serif;color:#fff;background:#14213D;border-radius:50%;width:40px;height:40px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 3px #D9AE4F}
.qr-num{display:block;font:900 4.5rem/1 Fraunces,Georgia,serif;color:#14213D;margin:8px 0 4px}.qr-num.go{animation:cdPop .6s ease-out both}.qr-sub{margin:0;font:700 .86rem Nunito,system-ui;color:#5B4A3F}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v172 ok')
