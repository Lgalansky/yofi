# Real Money build, step 174 (after rmv170.py): your votes unlock the qualifier; the qualifier is a live 2-horse race.
#  - A new photo needs 10 of YOUR votes to start its qualifier. Its card fills as you vote ("6 of 10 votes · 4 to go").
#  - At 10: full screen "Qualifier race · live" — your photo vs a rival on two lanes, crowd votes land one by one and move
#    the horses, a caller, first to 11 votes wins (21 votes max). Win = Qualified! (finalist rosette, +50 🟡, cash-ready).
#    Lose = "So close" with the free tune-up & training, or enter another photo.
#  - Wording everywhere: "10 votes to start · a live 2-horse race".
#  Simulated: the rival and the crowd's votes. Labelled.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
def RA(a, b, n=1):
    global s; assert s.count(a) == n, (a[:90], s.count(a), n); s = s.replace(a, b)
RA("The crowd gives it <b>15 votes</b>, each against another photo. Win 8 and it races in a 6-photo Final for cash.${first ? ' Your first entry is free.' : ' Entry is free.'}",
   "Vote 10 times and it starts its qualifier: a live 2-horse race decided by the crowd. Win it and it races in a 6-photo Final for cash. Entry is free.")
RA("Its qualifier is 15 crowd votes judged by the crowd: win 8 and it races in a Final for cash.", "Vote 10 times to start its qualifier: a live 2-horse race. Win it and it races in a Final for cash.")
RA('<div class="qls-r"><div><b>15</b><small>crowd votes</small></div><div><b>8</b><small>wins to the Final</small></div><div><b>+5 🟡</b><small>per win</small></div></div>',
   '<div class="qls-r"><div><b>10</b><small>of your votes to start</small></div><div><b>2</b><small>horse live race</small></div><div><b>🏁</b><small>win = the Final</small></div></div>')
RA("⚖️ <b>Each vote you make moves it forward.</b> Reach 🏁 and it races in a Final for cash.", "⚖️ <b>Your votes start its qualifier.</b> At 10 votes you watch it race a rival live. Win and it’s in the Final.")
s = s.replace("Enter another photo. Win 8 of 15 crowd votes and it races in a cash Final.", "Enter another photo. 10 votes start its qualifier race.")
s = s.replace("Win 8 of 15 crowd votes to reach a Final.", "10 of your votes start a photo’s qualifier: a live 2-horse race. Win it to reach a Final.")
s = s.replace("15 crowd votes. Win 8 to reach a Final.", "Vote 10 times to start its qualifier race.")
s = s.replace("The crowd gives it 15 votes. Win 8 and it races in a 6-photo Final for real cash.", "Vote to start its qualifier: a live race against a rival. Win and it races in a 6-photo Final for real cash.")
s = s.replace("function fcNotify() {", r"""const QV_NEED = 10, QR_WIN = 11;
function qlStep(p) { const q = p.ql; if (!q || q.done || q.live || !window.__myVote) return; q.got = (q.got || 0) + 1;
  if (q.got >= QV_NEED) { q.live = 1; save(); setTimeout(function tm() { if (document.querySelector('#coach.on, #sheet.on, #flow.on, #finPick.on, #ageGate.on, .chx') || window.__qlLive) { setTimeout(tm, 1000); return; } qlRace(p); }, 900); }
  save(); }
function qlRace(p) { const q = p.ql; if (!q || q.done) return; window.__qlLive = p.id; window.__nudgeAt = Date.now(); const nm = esc(rcName(p)), o = qlOpp(p), oh = '@' + QS_NAMES[Math.floor(Math.random() * QS_NAMES.length)];
  const st = qlStrength(p), pw = p.bo ? .9 : Math.max(.35, Math.min(.85, .55 + (st - 62) / 50)), won = Math.random() < pw;
  const loseV = 6 + Math.floor(Math.random() * 5), W = won ? 1 : 0, seq = [...Array(QR_WIN - 1).fill(W), ...Array(loseV).fill(1 - W)];
  for (let i = seq.length - 1; i > 0; i--) { const k = Math.floor(Math.random() * (i + 1)); [seq[i], seq[k]] = [seq[k], seq[i]]; } seq.push(W);
  popOpen(`<div class="pp qfx qrx"><p class="pp-k">🎀 Qualifier race · live</p><h2 class="db-h" id="qrH">${nm} vs ${esc(o.t)}</h2><p class="qr-s">First to ${QR_WIN} votes goes to the Final</p>
    <div class="qr-trk"><div class="qr-ln me"><span class="qr-nm">You</span><span class="qr-rail"><img id="qrA" src="${p.src}" alt=""></span><b id="qrAv">0</b></div>
      <div class="qr-ln"><span class="qr-nm">${esc(oh)}</span><span class="qr-rail"><img id="qrB" src="${o.src}" alt=""></span><b id="qrBv">0</b></div><i class="qf-fin"></i></div>
    <p class="db-com" id="qrC">🗳️ The crowd is voting…</p><p class="qr-n" id="qrN">0 votes in</p><div id="qrR"></div><p class="db-sim">Prototype: the rival and the crowd’s votes are simulated</p></div>`);
  let i = 0, A = 0, B = 0; const pos = v => `calc(${Math.min(1, v / QR_WIN)} * (100% - 44px))`;
  const iv = setInterval(() => { if (!document.getElementById('qrN')) { clearInterval(iv); window.__qlLive = 0; return; } if (seq[i++]) A++; else B++;
    $('#qrA').style.left = pos(A); $('#qrB').style.left = pos(B); $('#qrAv').textContent = A; $('#qrBv').textContent = B; $('#qrN').textContent = `${A + B} votes in`;
    const c = $('#qrC'); c.textContent = A === B ? '⚖️ Neck and neck!' : A > B ? (A >= QR_WIN - 2 ? `🔥 ${rcName(p)} is nearly home!` : `${rcName(p)} leads by ${A - B}`) : (B >= QR_WIN - 2 ? `😬 ${o.t} is closing in on the line` : `${o.t} leads by ${B - A}`);
    if (i < seq.length) return; clearInterval(iv); window.__qlLive = 0; q.live = 0; q.shown = 1; q.w = A; q.l = B; q.last = { win: won, t: o.t, src: o.src };
    const R = document.getElementById('qrR'), H = document.getElementById('qrH');
    setTimeout(() => photoFinish(() => { if (won) { q.done = 'q'; rzAdd(p, 3); S.gems = (S.gems || 0) + 50; p.qc = (p.qc || 0) + 50; p.fin = 1; p.cashOK = 1; save();
        popOpen(`<div class="pp qfx qlv"><p class="pp-k">🎀 Qualifier race · ${A}–${B}</p><h2 class="db-h qlv-win">Qualified!</h2><div class="qlv-ph"><img src="${p.src}" alt=""><i class="qlv-rz">${rosette('f')}</i></div>
          <p class="re-rzl">🎀 Finalist rosette · +50 🟡 · 💵 cash-ready</p><p class="db-s">${nm} beat “${esc(o.t)}” ${A}–${B} and is through to the Final.</p>
          <button class="btn block db-go cashb" id="qlvGo">🏁 See your rivals & race</button><div style="text-align:center"><button class="link pc-later" id="qlvL">Later</button></div></div>`);
        try { paintGems(); gemExplosion(50, { label: 'Qualified!' }); rvConfetti(document.querySelector('.qlv'), 70); } catch (e) {}
        $('#qlvGo').onclick = () => qfStart(p); $('#qlvL').onclick = () => { popClose(); try { renderJudge(); } catch (e) {} }; }
      else { q.done = 'x'; q.at = Date.now(); save();
        popOpen(`<div class="pp qfx qlv"><p class="pp-k">🎀 Qualifier race · ${A}–${B}</p><h2 class="db-h">So close</h2><div class="qlv-ph out"><img src="${p.src}" alt=""></div>
          <p class="db-s">“${esc(o.t)}” took it ${B}–${A}. Send ${nm} to your stable: a free tune-up, then train it to make it cash-ready.</p>
          <button class="btn block db-go cashb" data-trn="${p.id}">🏋️ Tune up & train · free</button><button class="btn block db-go quiet" id="qlvE">📷 Enter another photo</button><div style="text-align:center"><button class="link pc-later" id="qlvL">⚖️ Back to voting</button></div></div>`);
        $('#qlvE').onclick = () => { popClose(); setTimeout(finPick, 200); }; $('#qlvL').onclick = () => { popClose(); try { renderJudge(); } catch (e) {} }; } }), 500); }, 380); }
(() => { const pc = pvCard; pvCard = function (p) { const q = p.ql; if (!q || q.done || p.tr) return pc.apply(this, arguments); const g = Math.min(QV_NEED, q.got || 0), pos = g / QV_NEED, left = QV_NEED - g;
  return `<div class="pv-c" data-pid="${p.id}"><div class="pv-t"><b>${esc(rcName(p))}</b><span class="pv-st">${q.live ? '<i>●</i> Qualifier race · live' : '🎀 Qualifier'}</span><em>🟡 +${p.qc || 0}</em></div>
    <div class="pv-tr"><div class="pv-rail">${Array.from({ length: QV_NEED - 1 }, (_, i) => `<i style="left:${(i + 1) / QV_NEED * 100}%"></i>`).join('')}<u style="width:${pos * 100}%"></u></div>
      <img class="pv-hz" src="${p.src}" alt="" style="left:calc(${pos} * (100% - 40px))"><span class="pv-fl">🏁</span></div>
    <div class="pv-n"><span class="w">⚖️ ${g} of ${QV_NEED} votes</span><span class="pv-need">${q.live ? '<b>Race starting…</b>' : `<b>${left} more vote${left === 1 ? '' : 's'}</b> to start its qualifier race`}</span></div>
    <p class="pv-l">⚖️ Your votes power it to the start line</p></div>`; }; })();
function fcNotify() {""", 1)
s = s.replace('</style>', """.qr-s{margin:-4px 0 8px;font:700 .86rem Nunito,system-ui;color:#5B4A3F}
.qr-trk{position:relative;background:#14213D;border-radius:16px;padding:12px 12px;margin:6px 0 10px;box-shadow:inset 0 0 0 2px #D9AE4F}
.qr-ln{display:grid;grid-template-columns:52px 1fr 34px;align-items:center;gap:8px;height:84px}.qr-ln+.qr-ln{border-top:1px dashed rgba(255,255,255,.18)}
.qr-nm{font:800 .72rem Nunito,system-ui;color:#C9D3E6;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;text-align:left}.qr-ln.me .qr-nm{color:#F3D98B}
.qr-rail{position:relative;height:70px}.qr-rail img{position:absolute;top:13px;left:0;width:44px;height:44px;border-radius:50%;object-fit:cover;box-shadow:0 0 0 3px #fff;transition:left .35s ease-out}
.qr-ln.me .qr-rail img{box-shadow:0 0 0 3px #F3D98B,0 0 14px #F3D98B}.qr-ln>b{font:900 1.5rem Fraunces,Georgia,serif;color:#fff;text-align:right}.qr-ln.me>b{color:#F3D98B}
.qrx .qf-fin{right:46px}.qr-n{margin:2px 0 0;font:700 .8rem Nunito,system-ui;color:#8A7B6C}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v171 ok')
# pass 2: wider name column on the race lanes
s = open(d + 'yofi-real.html').read()
s = s.replace('</style>', """html body .qr-ln{grid-template-columns:84px 1fr 34px}html body .qr-nm{font-size:.7rem}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v171 pass2 ok')
