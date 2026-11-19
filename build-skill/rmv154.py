# Real Money build, step 157 (after rmv153.py): watch your photo's qualifier matches live while you vote.
#  - Each qualifier match is 7 crowd votes (majority wins). The live box at the top of the Vote screen shows your
#    photo vs its rival, the vote count and tug bar moving, "⏱ 3 votes to go", then the verdict
#    ("✅ Rex wins 5–2 · +5 🟡") before the next match starts.
#  - Votes arrive with each of your votes (2) and every 2.5 s while you're on the Vote screen (1).
#  - Underneath: wins bar to 8 with ✓ won / ✕ lost and what's still needed. Other photos stay as compact rows.
#  Simulated: the other voters' votes (by photo strength). Labelled in the box.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
s = s.replace("function fcNotify() {", r"""const QM_V = 7;
function qlOpp(p) { const q = p.ql, seen = q.seen || [], k = photoShow(p), all = SEED.filter(x => x.src && finCatOf(x) === k && x.src !== p.src),
    pool = all.filter(x => !seen.includes(x.src)), L = pool.length ? pool : all, o = L[Math.floor(Math.random() * L.length)] || { title: 'A rival', src: p.src };
  q.seen = seen.concat(o.src).slice(-12); return { src: o.src, t: o.title || 'A rival' }; }
function qlStep(p, n) { const q = p.ql; if (!q || q.done) return; n = n || 2; if (!q.m) { q.m = { o: qlOpp(p), a: 0, b: 0 }; }
  const pv = Math.max(.34, Math.min(.68, .5 + (qlStrength(p) - 62) / 110));
  for (let i = 0; i < n && !q.done; i++) { const m = q.m; if (Math.random() < pv) m.a++; else m.b++;
    if (m.a + m.b >= QM_V) { const win = m.a > m.b;
      if (win) { q.w++; p.qc = (p.qc || 0) + 5; S.gems = (S.gems || 0) + 5; try { paintGems(); } catch (e) {} } else q.l++;
      q.last = { win, t: m.o.t, src: m.o.src, a: m.a, b: m.b }; q.fl = Date.now();
      if (q.w >= QF_WIN) q.done = 'q'; else if (q.l > QF_N - QF_WIN) q.done = 'x';
      q.m = q.done ? null : { o: qlOpp(p), a: 0, b: 0 }; break; } }
  save(); }
function qlLiveHTML(p) { const q = p.ql, m = q.m || { o: { t: '…', src: '' }, a: 0, b: 0 }, tot = m.a + m.b, pa = tot ? Math.round(m.a / tot * 100) : 50,
    fl = q.last && Date.now() - (q.fl || 0) < 2200 ? q.last : null, need = QF_WIN - q.w, spare = QF_N - QF_WIN + 1 - q.l;
  return `<div class="qm" id="qm-${p.id}"><div class="qm-h"><span class="qm-live">● LIVE</span><b>Qualifier match ${Math.min(QF_N, q.w + q.l + 1)} of ${QF_N}</b><em>🟡 +${p.qc || 0}</em></div>
    <div class="qm-vs"><div class="qm-p me"><img src="${p.src}" alt=""><small>${esc(rcName(p))}</small></div>
      <div class="qm-mid"><div class="qm-sc"><b class="qm-a">${m.a}</b><span>votes</span><b class="qm-b">${m.b}</b></div>
        <div class="qm-bar"><i class="qm-ba" style="width:${pa}%"></i></div><p class="qm-left">${fl ? '' : `⏱ <b>${QM_V - tot}</b> vote${QM_V - tot === 1 ? '' : 's'} to go`}</p></div>
      <div class="qm-p"><img src="${m.o.src}" alt=""><small>${esc(m.o.t)}</small></div>
      ${fl ? `<div class="qm-fl ${fl.win ? 'w' : 'l'}">${fl.win ? `✅ ${esc(rcName(p))} wins ${fl.a}–${fl.b}<small>+5 🟡 · ${need > 0 ? `${need} more win${need === 1 ? '' : 's'} to the Final` : 'into the Final!'}</small>` : `✕ “${esc(fl.t)}” won ${fl.b}–${fl.a}<small>${q.done === 'x' ? 'qualifier over' : `${spare} loss${spare === 1 ? '' : 'es'} to spare · next match starting`}</small>`}</div>` : ''}</div>
    <div class="qm-ft"><span class="w">✓ ${q.w}</span><span class="l">✕ ${q.l}</span><div class="qv-bar"><i style="width:${Math.min(100, q.w / QF_WIN * 100)}%"></i><u>🏁</u></div><span class="qm-need">${need > 0 ? `${need} to the Final` : 'Finalist!'}</span></div>
    <p class="qm-sim">Prototype: other voters are simulated</p></div>`; }
(() => { const qs = qlStripHTML; qlStripHTML = function () { let h = qs.apply(this, arguments); const L = (S.photos || []).find(p => p.ql && !p.ql.done);
  if (!L || h.indexOf('id="qlS"></div>') > -1 && h.length < 30) return h;
  const div = document.createElement('div'); div.innerHTML = h; const box = div.firstElementChild, rows = [...box.querySelectorAll('.qv-r')], P = (S.photos || []).filter(p => p.ql && (!p.ql.done || !p.ql.shown || p.fin || p.raced || p.ql.done === 'x'));
  const i = rows.findIndex(r => r.querySelector('img') && r.querySelector('img').getAttribute('src') === L.src); if (i < 0) return h;
  rows[i].outerHTML = qlLiveHTML(L); box.classList.remove('cmp'); if (box.querySelectorAll('.qv-r').length) box.classList.add('cmp', 'has-l');
  const hd = box.querySelector('.qv-h'); if (hd) hd.remove(); return box.outerHTML; }; })();
function qlPaint() { const e = document.getElementById('qlS'); if (!e) return; const L = (S.photos || []).find(p => p.ql && !p.ql.done), m = L && L.ql.m, x = L && document.getElementById('qm-' + L.id);
  if (x && m && !(L.ql.last && Date.now() - (L.ql.fl || 0) < 2200) && !x.querySelector('.qm-fl') && x.dataset.mo === m.o.src) {
    const tot = m.a + m.b, A = x.querySelector('.qm-a'), B = x.querySelector('.qm-b');
    if (A.textContent != m.a) { A.textContent = m.a; A.classList.remove('bp'); void A.offsetWidth; A.classList.add('bp'); }
    if (B.textContent != m.b) { B.textContent = m.b; B.classList.remove('bp'); void B.offsetWidth; B.classList.add('bp'); }
    x.querySelector('.qm-ba').style.width = (tot ? Math.round(m.a / tot * 100) : 50) + '%';
    x.querySelector('.qm-left').innerHTML = `⏱ <b>${QM_V - tot}</b> vote${QM_V - tot === 1 ? '' : 's'} to go`; return; }
  e.outerHTML = qlStripHTML(); const y = L && document.getElementById('qm-' + L.id); if (y && m) y.dataset.mo = m.o.src;
  if (L && L.ql.last && Date.now() - (L.ql.fl || 0) < 2200) { clearTimeout(window.__qmT); window.__qmT = setTimeout(qlPaint, 2300); } }
setInterval(() => { try { if (!S || !$('#app').classList.contains('on') || document.querySelector('#coach.on')) return; const e = document.getElementById('qlS'); if (!e || !e.offsetParent) return;
  const L = (S.photos || []).find(p => p.ql && !p.ql.done); if (!L || (L.ql.fl && Date.now() - L.ql.fl < 2600)) return; qlStep(L, 1); qlPaint(); } catch (e) {} }, 2500);
function fcNotify() {""", 1)
# the per-vote hook now adds 2 votes to the live match (qlStep default) and repaints in place
s = s.replace('</style>', """html body .qm{padding:2px 0 6px;text-align:left}.qv.has-l .qm{border-bottom:1px solid #E6EFE2;margin-bottom:2px}
.qm-h{display:flex;align-items:center;gap:8px;margin:0 0 6px}.qm-h b{font:900 .78rem Nunito,system-ui;letter-spacing:.04em;text-transform:uppercase;color:#14213D}
.qm-live{font:900 .66rem Nunito,system-ui;letter-spacing:.06em;color:#fff;background:#C0533F;border-radius:999px;padding:2px 7px;animation:qmPulse 1.4s ease-in-out infinite}
@keyframes qmPulse{50%{opacity:.55}}.qm-h em{margin-left:auto;font-style:normal;font:900 .78rem Nunito,system-ui;color:#9A6B12;background:#FFF1C9;border-radius:999px;padding:2px 8px}
.qm-vs{position:relative;display:grid;grid-template-columns:62px 1fr 62px;gap:8px;align-items:center}
.qm-p{display:flex;flex-direction:column;align-items:center;gap:3px;min-width:0}.qm-p img{width:56px;height:56px;border-radius:12px;object-fit:cover;box-shadow:0 0 0 2px #EADCC6}.qm-p.me img{box-shadow:0 0 0 3px #2F6B3F}
.qm-p small{max-width:62px;font:800 .66rem Nunito,system-ui;color:#3D4A5C;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.qm-p.me small{color:#22502F}
.qm-sc{display:flex;justify-content:space-between;align-items:baseline}.qm-sc b{font:900 1.5rem Fraunces,Georgia,serif;line-height:1}.qm-a{color:#2F6B3F}.qm-b{color:#A6402F}.qm-sc span{font:800 .62rem Nunito,system-ui;text-transform:uppercase;letter-spacing:.06em;color:#8A7B6C}
.qm-sc b.bp{animation:qmBp .45s ease-out}@keyframes qmBp{40%{transform:scale(1.45)}}
.qm-bar{height:12px;margin:5px 0 4px;border-radius:6px;background:#E7A595;overflow:hidden}.qm-ba{display:block;height:100%;background:linear-gradient(90deg,#7FC48E,#2F6B3F);transition:width .45s ease-out;border-right:2px solid #fff}
.qm-left{margin:0;text-align:center;font:700 .74rem Nunito,system-ui;color:#3D4A5C}.qm-left b{color:#14213D}
.qm-fl{position:absolute;inset:-2px 58px;display:flex;flex-direction:column;align-items:center;justify-content:center;border-radius:12px;font:900 .9rem/1.2 Nunito,system-ui;text-align:center;animation:cdPop .4s ease-out both}
.qm-fl.w{background:#2F6B3F;color:#fff}.qm-fl.l{background:#F6E4DF;color:#A6402F;box-shadow:inset 0 0 0 1.5px #C0533F}.qm-fl small{font:700 .7rem Nunito,system-ui;opacity:.9;margin-top:2px}
.qm-ft{display:flex;align-items:center;gap:8px;margin-top:8px;font:800 .74rem Nunito,system-ui}.qm-ft .w{color:#2F6B3F}.qm-ft .l{color:#B0473A}.qm-ft .qv-bar{flex:1;height:9px}.qm-ft .qv-bar u{font-size:.75rem}.qm-need{color:#14213D;white-space:nowrap;margin-left:4px}
.qm-sim{margin:4px 0 0;font:600 .62rem Nunito,system-ui;color:#9A8F80;text-align:right}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v154 ok')
# pass 2: no votes land during the 2 s verdict beat; the finalist / out moment opens ~1 s after the deciding match
s = open(d + 'yofi-real.html').read()
RA("function qlStep(p, n) { const q = p.ql; if (!q || q.done) return; n = n || 2;", "function qlStep(p, n) { const q = p.ql; if (!q || q.done || (q.fl && Date.now() - q.fl < 2400)) return; n = n || 2;")
RA("q.m = q.done ? null : { o: qlOpp(p), a: 0, b: 0 }; break; } }",
   "q.m = q.done ? null : { o: qlOpp(p), a: 0, b: 0 };\n      if (q.done) setTimeout(function tr() { if (q.shown) return; if (document.querySelector('#coach.on, #sheet.on, #flow.on, #finPick.on, #ageGate.on, .chx')) { setTimeout(tr, 1200); return; } qlDone(p); }, 1100); break; } }")
open(d + 'yofi-real.html', 'w').write(s); print('rm v154 pass2 ok')
# pass 3: tighter box so the vote pair stays on screen; solid verdict banner over the whole matchup; no "stakes" note
#  while your own match is live; simulated label moved into the header.
s = open(d + 'yofi-real.html').read()
RA('<b>Qualifier match ${Math.min(QF_N, q.w + q.l + 1)} of ${QF_N}</b><em>', '<b>Match ${Math.min(QF_N, q.w + q.l + 1)} of ${QF_N}</b><i class="qm-s">simulated</i><em>')
RA('\n    <p class="qm-sim">Prototype: other voters are simulated</p></div>`; }', '</div>`; }')
s = s.replace('</style>', """html body .qm-h{margin:0 0 4px}html body .qm-h b{font-size:.72rem}.qm-s{font-style:normal;font:700 .6rem Nunito,system-ui;color:#A89C8C}
html body .qm-vs{grid-template-columns:50px 1fr 50px;gap:8px}html body .qm-p img{width:46px;height:46px;border-radius:10px}html body .qm-p small{max-width:54px;font-size:.62rem}
html body .qm-sc b{font-size:1.25rem}html body .qm-bar{height:10px;margin:3px 0 3px}html body .qm-ft{margin-top:5px}
html body .qm-fl{inset:-3px -4px;animation:qmFl .35s ease-out both;font-size:.86rem}html body .qm-fl.l{background:#F6E4DF}
@keyframes qmFl{0%{opacity:0;transform:scale(1.15)}100%{opacity:1;transform:none}}
html body #judge:has(.qm) .vr-stake{display:none}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v154 pass3 ok')
