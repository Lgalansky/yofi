# Real Money build, step 166 (after rmv162.py): watch your photo qualify, full screen.
#  - When a photo reaches 7 wins (one away), the deciding votes play out full screen: big framed photo, its horse on the
#    track, "Vote 11 of 15", each vote landing with the rival's photo (✓ beat / ✕ lost to), every ~1.3 s.
#  - 8th win: "Qualified!" — the horse crosses the line, finalist rosette, +50 🟡, confetti, "🏁 See your rivals & race".
#    If it runs out of losses instead: "So close" and "📷 Enter another photo".
#  Simulated: the crowd's votes. Labelled.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("  if (q.w >= QF_WIN) q.done = 'q'; else if (q.l > QF_N - QF_WIN) q.done = 'x';\n  if (q.done) setTimeout(function tr() { if (q.shown) return;",
   "  if (q.w >= QF_WIN) q.done = 'q'; else if (q.l > QF_N - QF_WIN) q.done = 'x';\n  if (!q.done && q.w === QF_WIN - 1 && !q.mp && !window.__qlLive) { q.mp = 1; setTimeout(function tm() { if (document.querySelector('#coach.on, #sheet.on, #flow.on, #finPick.on, #ageGate.on, .chx') || window.__qlLive) { setTimeout(tm, 1000); return; } qlLive(p); }, 1600); }\n  if (q.done && !window.__qlLive) setTimeout(function tr() { if (q.shown) return;")
s = s.replace("function fcNotify() {", r"""function qlLiveTrack(p) { const q = p.ql, pos = Math.min(1, q.w / QF_WIN);
  return `<div class="pv-tr ql-tr"><div class="pv-rail">${Array.from({ length: QF_WIN - 1 }, (_, i) => `<i style="left:${(i + 1) / QF_WIN * 100}%"></i>`).join('')}<u style="width:${pos * 100}%"></u></div><img class="pv-hz" id="qlHz" src="${p.src}" alt="" style="left:calc(${pos} * (100% - 40px))"><span class="pv-fl">🏁</span></div>`; }
function qlLive(p) { const q = p.ql; if (!q || q.done) return; window.__qlLive = p.id; window.__nudgeAt = Date.now(); const nm = esc(rcName(p));
  popOpen(`<div class="pp qfx qlv"><p class="pp-k">🎀 Qualifier · match point</p><h2 class="db-h" id="qlvH">${nm} needs 1 more win</h2>
    <div class="qlv-ph"><img src="${p.src}" alt=""><i class="qlv-rz" id="qlvRz"></i></div>${qlLiveTrack(p)}
    <p class="qlv-c" id="qlvC"><b>${q.w}</b> won · <b>${q.l}</b> lost · ${QF_N - QF_WIN + 1 - q.l} loss${QF_N - QF_WIN + 1 - q.l === 1 ? '' : 'es'} to spare</p>
    <div class="qlv-f" id="qlvF"><p class="qlv-w">🗳️ The crowd is voting…</p></div><div id="qlvB"></div><p class="db-sim">Prototype: the crowd’s votes are simulated</p></div>`);
  const iv = setInterval(() => { if (!document.getElementById('qlvF')) { clearInterval(iv); window.__qlLive = 0; return; }
    window.__myVote = 1; try { qlStep(p); } finally { window.__myVote = 0; }
    const L = q.last, f = document.getElementById('qlvF'); f.insertAdjacentHTML('afterbegin', `<p class="qlv-v ${L.win ? 'w' : 'l'}"><img src="${L.src}" alt=""><span>Vote ${q.w + q.l} · ${L.win ? `✓ A voter picked <b>${nm}</b> over “${esc(L.t)}”` : `✕ A voter picked “${esc(L.t)}”`}</span></p>`);
    [...f.querySelectorAll('.qlv-v')].slice(3).forEach(x => x.remove()); const w0 = f.querySelector('.qlv-w'); if (w0) w0.remove();
    const pos = Math.min(1, q.w / QF_WIN), hz = document.getElementById('qlHz'), u = document.querySelector('.qlv .pv-rail u'); if (hz) hz.style.left = `calc(${pos} * (100% - 40px))`; if (u) u.style.width = pos * 100 + '%';
    document.getElementById('qlvC').innerHTML = `<b>${q.w}</b> won · <b>${q.l}</b> lost${q.done ? '' : ` · ${QF_N - QF_WIN + 1 - q.l} loss${QF_N - QF_WIN + 1 - q.l === 1 ? '' : 'es'} to spare`}`;
    if (!q.done) { if (!L.win) { const h = document.getElementById('qlvH'); h.textContent = QF_N - QF_WIN + 1 - q.l === 1 ? `Last chance: ${rcName(p)} needs this one` : `${rcName(p)} still needs 1 more win`; } return; }
    clearInterval(iv); q.shown = 1; window.__qlLive = 0; const h = document.getElementById('qlvH'), B = document.getElementById('qlvB');
    if (q.done === 'q') { rzAdd(p, 3); S.gems = (S.gems || 0) + 50; p.qc = (p.qc || 0) + 50; p.fin = 1; save();
      setTimeout(() => { h.textContent = 'Qualified!'; h.classList.add('qlv-win'); document.querySelector('.qlv .pp-k').textContent = `🎀 Qualifier · ${q.w} wins, ${q.l} losses`; document.getElementById('qlvRz').innerHTML = rosette('f');
        B.innerHTML = `<p class="re-rzl">🎀 Finalist rosette · +50 🟡</p><button class="btn block db-go cashb" id="qlvGo">🏁 See your rivals & race</button><div style="text-align:center"><button class="link pc-later" id="qlvL">Later</button></div>`;
        try { paintGems(); gemExplosion(50, { label: 'Qualified!' }); rvConfetti(document.querySelector('.qlv'), 70); } catch (e) {}
        $('#qlvGo').onclick = () => qfStart(p); $('#qlvL').onclick = () => { popClose(); try { renderJudge(); } catch (e) {} }; }, 700); }
    else { save(); setTimeout(() => { h.textContent = 'So close'; document.querySelector('.qlv .pp-k').textContent = `🎀 Qualifier · ${q.w} wins, ${q.l} losses`; document.querySelector('.qlv-ph').classList.add('out');
        B.innerHTML = `<p class="db-s">One win short. Bright, close-up shots tend to win.</p><button class="btn block db-go" id="qlvE">📷 Enter another photo</button><div style="text-align:center"><button class="link pc-later" id="qlvL">⚖️ Back to voting</button></div>`;
        $('#qlvE').onclick = () => { popClose(); setTimeout(finPick, 200); }; $('#qlvL').onclick = () => { popClose(); try { renderJudge(); } catch (e) {} }; }, 700); } }, 1300); }
function fcNotify() {""", 1)
s = s.replace('</style>', """.qlv-ph{position:relative;width:min(72%,300px);margin:6px auto 10px;padding:5px;border-radius:14px;background:linear-gradient(135deg,#F3D98B,#C9963A 45%,#F6E3A6 70%,#B8862E);box-shadow:0 4px 14px rgba(120,80,20,.25)}
.qlv-ph img{display:block;width:100%;aspect-ratio:1;object-fit:cover;border-radius:10px}.qlv-ph.out img{filter:grayscale(.6)}.qlv-rz{position:absolute;top:-16px;right:-18px;width:84px;transform:rotate(8deg)}.qlv-rz svg{width:100%;height:auto;display:block;animation:cdPop .5s ease-out both}
.ql-tr{margin:4px 0}.qlv-c{margin:4px 0 8px;font:700 .9rem Nunito,system-ui;color:#3D4A5C}.qlv-c b{color:#14213D;font-size:1.05rem}
.qlv-f{display:grid;gap:5px;min-height:96px;text-align:left}.qlv-w{margin:0;text-align:center;font:700 .86rem Nunito,system-ui;color:#8A7B6C}
.qlv-v{display:flex;align-items:center;gap:8px;margin:0;padding:6px 9px;border-radius:10px;font:700 .82rem/1.3 Nunito,system-ui;animation:qmFl .35s ease-out both}.qlv-v img{width:28px;height:28px;border-radius:7px;object-fit:cover;flex:none}
.qlv-v.w{background:#F1F6EC;color:#22502F}.qlv-v.l{background:#F9ECE8;color:#A6402F}.qlv-v b{color:#14213D}.qlv-v:not(:first-child){opacity:.6}
.qlv-win{color:#2F6B3F!important;animation:cdPop .5s ease-out both}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v163 ok')
# pass 2: vote feed box sized to its content
s = open(d + 'yofi-real.html').read()
s = s.replace('</style>', """html body .qlv-f{min-height:0}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v163 pass2 ok')
