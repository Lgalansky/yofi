# Real Money build, step 184 (after rmv180.py): the owner's navy & gold mock-ups for the three big moments.
#  1. Live qualifier "Race to 11": navy full screen over a blurred backdrop of your photo, LIVE QUALIFIER pill,
#     "Winner advances to the <category> Final.", two big photo cards (yours gold-framed) with a big vote count,
#     "of 11 votes" and an 11-pip bar; a voter line; a gold goal pill "3 more votes to qualify". 3-2-1 intro kept.
#  2. "You're in the final!": confetti, big gold-framed photo with the FINALIST rosette, "Iceland wins 11–6",
#     "Against Pool with a view", "+50 coins", green "Meet your finalists", Later. Goes straight to the Final lobby.
#  3. Final lobby: "<Category> Final", trophy box "1st wins $7.00 / 2nd wins $3.20", "Meet the 6 finalists" grid
#     (YOU tag, name bars), "Choose your entry" ($2/$5/$10/$20, selected in green), "Each finalist pays $2. Crowd
#     votes decide the winners.", green "Enter the final · $2", Later.
#  "So close" result restyled to match. Simulated: rival, crowd votes, other finalists. Labelled.
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
s = s.replace("function fcNotify() {", r"""const nvPips = (n, cls) => Array.from({ length: QR_WIN }, (_, i) => `<i class="${i < n ? cls : ''}"></i>`).join('');
function qlRace(p) { const q = p.ql; if (!q || q.done) return; window.__qlLive = p.id; window.__nudgeAt = Date.now();
  const nm = esc(rcName(p)), o = qlOpp(p), oh = '@' + QS_NAMES[Math.floor(Math.random() * QS_NAMES.length)], fn = esc(showName(photoShow(p) || 'pets'));
  const st = qlStrength(p), pw = p.bo ? .9 : Math.max(.35, Math.min(.85, .55 + (st - 62) / 50)), won = Math.random() < pw;
  const loseV = 6 + Math.floor(Math.random() * 5), W = won ? 1 : 0, seq = [...Array(QR_WIN - 1).fill(W), ...Array(loseV).fill(1 - W)];
  for (let i = seq.length - 1; i > 0; i--) { const k = Math.floor(Math.random() * (i + 1)); [seq[i], seq[k]] = [seq[k], seq[i]]; } seq.push(W);
  popOpen(`<div class="pp qfx qrx nv qr2"><div class="nv-bg" style="background-image:url('${p.src}')"></div><p class="nv-brand">PhotoPicks</p>
    <div class="nv-pillrow"><span class="nv-pill">Live qualifier</span></div><h2 class="nv-h">Race to ${QR_WIN}</h2><p class="nv-s">Winner advances to the<br>${fn} Final.</p>
    <div class="qr2-c me" id="qrCA"><div class="qr2-im"><img src="${p.src}" alt=""><span class="qr2-n">${nm} · <b>You</b></span></div><div class="qr2-r"><b id="qrAv">0</b><small>of ${QR_WIN} votes</small><span class="qr2-p" id="qrAp">${nvPips(0, 'on')}</span></div></div>
    <div class="qr2-c" id="qrCB"><div class="qr2-im"><img src="${o.src}" alt=""><span class="qr2-n">${esc(o.t)}</span></div><div class="qr2-r"><b id="qrBv">0</b><small>of ${QR_WIN} votes</small><span class="qr2-p" id="qrBp">${nvPips(0, 'on')}</span></div></div>
    <p class="qr2-v" id="qrV">🗳️ The crowd is voting…</p><div class="nv-goal" id="qrG"><b>${QR_WIN}</b> votes to qualify</div><p class="nv-sim">Demo · simulated votes · rival ${esc(oh)}</p></div>`);
  const run = () => { let i = 0, A = 0, B = 0; const iv = setInterval(() => { if (!document.getElementById('qrG')) { clearInterval(iv); window.__qlLive = 0; return; }
      const me = seq[i++]; if (me) A++; else B++; const vh = '@' + QS_NAMES[Math.floor(Math.random() * QS_NAMES.length)];
      $('#qrAv').textContent = A; $('#qrBv').textContent = B; $('#qrAp').innerHTML = nvPips(A, 'on'); $('#qrBp').innerHTML = nvPips(B, 'on');
      const c = document.getElementById(me ? 'qrCA' : 'qrCB'); c.classList.remove('hit'); void c.offsetWidth; c.classList.add('hit');
      $('#qrV').innerHTML = `🗳️ <b>${vh}</b> voted for <b class="${me ? 'me' : ''}">${me ? nm : esc(o.t)}</b>`;
      const g = $('#qrG'), left = QR_WIN - A; g.innerHTML = left > 0 ? `<b>${left}</b> more vote${left === 1 ? '' : 's'} to qualify` : '<b>🏁</b> Qualified!'; g.classList.toggle('hot', left <= 2 && left > 0);
      if (i < seq.length) return; clearInterval(iv); window.__qlLive = 0; q.live = 0; q.shown = 1; q.w = A; q.l = B; q.last = { win: won, t: o.t, src: o.src };
      setTimeout(() => photoFinish(() => won ? qlWon(p, o, A, B) : qlLost(p, o, A, B)), 600); }, 1000); };
  qrCount(p, o, oh, run); }
function qlWon(p, o, A, B) { const q = p.ql, nm = esc(rcName(p)); q.done = 'q'; rzAdd(p, 3); S.gems = (S.gems || 0) + 50; p.qc = (p.qc || 0) + 50; p.fin = 1; p.cashOK = 1; p.fr = { s: QS_STEPS, go: 1 }; save();
  popOpen(`<div class="pp qfx nv qw"><p class="nv-brand">PhotoPicks</p><h2 class="nv-big">You’re in<br>the final!</h2><i class="nv-sw"></i>
    <div class="qw-ph"><img src="${p.src}" alt=""><i class="qw-rz">${rosette('f')}</i></div>
    <p class="qw-r">${nm} wins ${A}–${B}</p><p class="qw-o">Against ${esc(o.t)}</p><p class="qw-c"><span>🪙</span> +50 coins</p>
    <button class="btn block nv-go" id="qlvGo">Meet your finalists</button><div style="text-align:center"><button class="link nv-later" id="qlvL">Later</button></div></div>`);
  try { paintGems(); rvConfetti(document.querySelector('.qw'), 90); } catch (e) {}
  $('#qlvGo').onclick = () => qfStart(p); $('#qlvL').onclick = () => { popClose(); try { renderJudge(); } catch (e) {} }; }
function qlLost(p, o, A, B) { const q = p.ql, nm = esc(rcName(p)); q.done = 'x'; q.at = Date.now(); save();
  popOpen(`<div class="pp qfx nv qw"><p class="nv-brand">PhotoPicks</p><h2 class="nv-big sm">So close</h2><i class="nv-sw"></i>
    <div class="qw-ph out"><img src="${p.src}" alt=""></div><p class="qw-r">${esc(o.t)} wins ${B}–${A}</p><p class="qw-o">${nm} gets a free tune-up, then train it for Cash Races</p>
    <button class="btn block nv-go" data-trn="${p.id}">🏋️ Tune up & train · free</button><button class="btn block nv-go2" id="qlvE">📷 Enter another photo</button><div style="text-align:center"><button class="link nv-later" id="qlvL">Back to voting</button></div></div>`);
  $('#qlvE').onclick = () => { popClose(); setTimeout(finPick, 200); }; $('#qlvL').onclick = () => { popClose(); try { renderJudge(); } catch (e) {} }; }
function qfPick(p, fee) { const R = qfRivals(p), k = photoShow(p); fee = fee || 2;
  const tile = (x, me) => `<div class="qf2-t ${me ? 'me' : ''}"><img src="${x.src}" alt="">${me ? '<em>YOU</em>' : ''}<span>${esc(me ? rcName(p) : x.t)}</span></div>`;
  popOpen(`<div class="pp qfx nv qf2"><p class="nv-brand">PhotoPicks</p><h2 class="nv-h2">${k ? esc(showName(k)) + ' Final' : 'The Final'}</h2>
    <div class="qf2-win"><span class="qf2-cup">🏆</span><div><b>1st wins ${money(fee * QF_PAY[0])}</b><small>2nd wins ${money(fee * QF_PAY[1])}</small></div></div>
    <p class="nv-rule"><span>Meet the 6 finalists</span></p><div class="qf2-g">${tile({ src: p.src }, 1)}${R.map(x => tile(x, 0)).join('')}</div>
    <p class="nv-rule"><span>Choose your entry</span></p><div class="qf2-f">${QF_FEES.map(f => `<button data-qff="${f}" class="${f === fee ? 'on' : ''}"><b>$${f}</b><small>1st ${money(f * QF_PAY[0]).replace('.00', '')}</small></button>`).join('')}</div>
    <p class="qf2-s">Each finalist pays $${fee}. Crowd votes decide the winners.</p>
    <button class="btn block nv-go" id="qfpGo">Enter the final · $${fee}</button><div style="text-align:center"><button class="link nv-later" id="qfpL">Later</button></div>
    <p class="nv-sim">You have ${money(S.cash || 0)} · demo: other finalists simulated</p></div>`);
  document.querySelectorAll('[data-qff]').forEach(b => b.onclick = () => { window.__keepScroll = 1; qfPick(p, +b.dataset.qff); });
  $('#qfpL').onclick = () => popClose();
  $('#qfpGo').onclick = () => { window.__qfFee = fee; popClose(); payCash(fee, `A $${fee} Final entry`, () => setTimeout(() => qfRace(p, [{ src: p.src, t: rcName(p), h: 'You', me: 1, st: qlStrength(p) }].concat(R)), 250)); }; }
function fcNotify() {""", 1)
s = s.replace('</style>', """html body #coach:has(.nv) .ppop{background:radial-gradient(120% 70% at 50% 0%,#22325A 0%,#14213D 55%,#0E1830 100%)!important;color:#E8EDF7;box-shadow:none!important;border:0!important}
.nv{position:relative;text-align:center;color:#E8EDF7}.nv-bg{position:absolute;left:-16px;right:-16px;top:-30px;height:260px;background-size:cover;background-position:center;filter:blur(2px) brightness(.45);-webkit-mask-image:linear-gradient(#000 40%,transparent);mask-image:linear-gradient(#000 40%,transparent);z-index:0}
.nv>*{position:relative;z-index:1}.nv-brand{margin:0 0 8px;font:800 1.15rem Fraunces,Georgia,serif;color:#F3D98B}
.nv-pillrow{display:flex;align-items:center;gap:12px;margin:2px 0 6px}.nv-pillrow::before,.nv-pillrow::after{content:'';flex:1;height:1.5px;background:linear-gradient(90deg,transparent,#D9AE4F)}.nv-pillrow::after{background:linear-gradient(90deg,#D9AE4F,transparent)}
.nv-pill{padding:5px 16px;border-radius:999px;box-shadow:inset 0 0 0 2px #D9AE4F;font:900 .82rem Nunito,system-ui;letter-spacing:.12em;text-transform:uppercase;color:#F3D98B;background:rgba(20,33,61,.6)}
.nv-h{margin:0;font:900 3rem/1.05 Fraunces,Georgia,serif;color:#FBF3DC}.nv-s{margin:6px 0 14px;font:700 1.02rem/1.35 Nunito,system-ui;color:#E8EDF7}
.qr2-c{display:grid;grid-template-columns:1fr 112px;margin:0 0 12px;border-radius:18px;overflow:hidden;background:#1B2A4C;box-shadow:0 0 0 2px #8C9AB5;text-align:left;transition:transform .2s}.qr2-c.me{box-shadow:0 0 0 3px #E9B949,0 0 22px rgba(233,185,73,.35)}
.qr2-c.hit{animation:qrHit .45s ease-out}@keyframes qrHit{40%{transform:scale(1.025)}}
.qr2-im{position:relative;min-height:128px}.qr2-im img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}.qr2-n{position:absolute;left:0;right:0;bottom:0;padding:18px 12px 8px;background:linear-gradient(transparent,rgba(10,16,32,.85));font:800 1.05rem Fraunces,Georgia,serif;color:#fff}.qr2-n b{color:#F3D98B}
.qr2-r{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;padding:8px 6px;background:#14213D}.qr2-r>b{font:900 2.7rem/1 Fraunces,Georgia,serif;color:#F3D98B}.qr2-c:not(.me) .qr2-r>b{color:#FBF3DC}
.qr2-r small{font:700 .8rem Nunito,system-ui;color:#C9D3E6}.qr2-p{display:flex;gap:2px;margin-top:5px}.qr2-p i{width:6px;height:12px;border-radius:2px;background:#3A4766}.qr2-p i.on{background:#E9B949}
.qr2-v{min-height:1.4em;margin:2px 0 10px;font:700 .9rem Nunito,system-ui;color:#C9D3E6}.qr2-v b{color:#fff}.qr2-v b.me{color:#F3D98B}
.nv-goal{display:inline-block;padding:9px 22px;border-radius:999px;box-shadow:inset 0 0 0 2px #D9AE4F;background:rgba(20,33,61,.8);font:800 1.15rem Fraunces,Georgia,serif;color:#FBF3DC}.nv-goal b{font-size:1.5rem;color:#F3D98B;margin-right:4px}.nv-goal.hot{animation:pvPulse 1s ease-in-out infinite}
.nv-sim{margin:10px 0 0;font:600 .74rem Nunito,system-ui;color:#8C9AB5}
.nv-big{margin:4px 0 0;font:900 2.9rem/1 Fraunces,Georgia,serif;color:#FBF3DC}.nv-big.sm{font-size:2.4rem}.nv-sw{display:block;width:150px;height:4px;margin:8px auto 14px;border-radius:2px;background:#E9B949;transform:rotate(-2deg)}
.qw-ph{position:relative;width:92%;margin:0 auto 12px;padding:6px;border-radius:16px;background:linear-gradient(135deg,#F3D98B,#C9963A 45%,#F6E3A6 70%,#B8862E);box-shadow:0 8px 24px rgba(0,0,0,.4)}.qw-ph img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:11px}.qw-ph.out img{filter:grayscale(.6)}
.qw-rz{position:absolute;top:-22px;right:-16px;width:96px;transform:rotate(8deg);filter:drop-shadow(0 4px 6px rgba(0,0,0,.4))}.qw-rz svg{width:100%;height:auto;display:block}
.qw-r{margin:4px 0 0;font:900 2rem/1.1 Fraunces,Georgia,serif;color:#FBF3DC}.qw-o{margin:2px 0 6px;font:700 1rem Nunito,system-ui;color:#E8EDF7}.qw-c{margin:4px 0 14px;font:900 1.8rem Fraunces,Georgia,serif;color:#F3D98B}.qw-c span{font-size:1.6rem;margin-right:6px}
html body .nv .nv-go{min-height:56px!important;border-radius:999px!important;background:linear-gradient(180deg,#3FAE4F,#1F7A33)!important;color:#fff!important;font:900 1.3rem Fraunces,Georgia,serif!important;box-shadow:0 0 0 2px #E9B949,0 6px 16px rgba(0,0,0,.35)!important;margin:6px 0 0!important}
html body .nv .nv-go2{min-height:48px!important;border-radius:999px!important;background:transparent!important;color:#FBF3DC!important;box-shadow:inset 0 0 0 2px #8C9AB5!important;font:800 1rem Nunito,system-ui!important;margin:10px 0 0!important}
html body .nv .nv-later{margin-top:10px;color:#FBF3DC!important;font:700 1rem Nunito,system-ui;text-decoration:underline}
.nv-h2{margin:0 0 10px;font:900 1.75rem/1.15 Fraunces,Georgia,serif;color:#FBF3DC}
.qf2-win{display:flex;align-items:center;justify-content:center;gap:16px;margin:0 0 12px;padding:10px 14px;border-radius:16px;box-shadow:inset 0 0 0 2px #E9B949;background:rgba(10,16,32,.45)}.qf2-cup{font-size:2.4rem;padding-right:16px;border-right:1.5px solid #D9AE4F}
.qf2-win b{display:block;font:900 1.9rem/1.1 Fraunces,Georgia,serif;color:#F3D98B;text-align:left}.qf2-win small{display:block;font:800 1.05rem Nunito,system-ui;color:#FBF3DC;text-align:left}
.nv-rule{display:flex;align-items:center;gap:10px;margin:6px 0 8px}.nv-rule::before,.nv-rule::after{content:'';flex:1;height:1.5px;background:#D9AE4F;opacity:.7}.nv-rule span{font:800 1.1rem Fraunces,Georgia,serif;color:#FBF3DC}
.qf2-g{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:7px;margin-bottom:8px}.qf2-t{position:relative;border-radius:10px;overflow:hidden;background:#FBF6EE;box-shadow:0 0 0 1.5px #EADCC6}.qf2-t.me{box-shadow:0 0 0 3px #E9B949}
.qf2-t img{display:block;width:100%;aspect-ratio:1.15;object-fit:cover}.qf2-t span{display:block;padding:4px 4px 5px;font:800 .78rem Fraunces,Georgia,serif;color:#14213D;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.qf2-t em{position:absolute;top:6px;left:6px;padding:1px 7px;border-radius:5px;background:#14213D;color:#F3D98B;font:900 .66rem Nunito,system-ui;font-style:normal;box-shadow:0 0 0 1.5px #E9B949}
.qf2-f{display:grid;grid-template-columns:repeat(4,1fr);gap:7px}.qf2-f button{padding:9px 2px;border:0;border-radius:12px;background:#FBF6EE;cursor:pointer;font:inherit;box-shadow:0 0 0 1.5px #EADCC6}
.qf2-f b{display:block;font:900 1.4rem Fraunces,Georgia,serif;color:#14213D}.qf2-f small{font:800 .74rem Nunito,system-ui;color:#14213D}.qf2-f button.on{background:linear-gradient(180deg,#2F8A3F,#1F6A2E);box-shadow:0 0 0 2.5px #E9B949}.qf2-f button.on b,.qf2-f button.on small{color:#fff}
.qf2-s{margin:10px 0 2px;font:700 .86rem Nunito,system-ui;color:#E8EDF7}
html body #coach:has(.nv) .qr-cd{background:radial-gradient(120% 70% at 50% 0%,#22325A,#14213D)}html body #coach:has(.nv) .qr-cd .pp-k,html body #coach:has(.nv) .qr-num{color:#F3D98B}html body #coach:has(.nv) .qr-vs b{color:#FBF3DC}html body #coach:has(.nv) .qr-vs small,html body #coach:has(.nv) .qr-sub{color:#C9D3E6}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v181 ok')
# pass 2: headings stay light on navy; screens start at the top; tighter race cards; category fallback
s = open(d + 'yofi-real.html').read()
s = s.replace("fn = esc(showName(photoShow(p) || 'pets'))", "fn = esc(showName(photoShow(p) || finCatOf(p) || 'pets'))", 1)
s = s.replace('</style>', """html body .nv h2.nv-h,html body .nv h2.nv-big,html body .nv h2.nv-h2{color:#FBF3DC!important;-webkit-text-fill-color:#FBF3DC!important;text-shadow:0 2px 12px rgba(0,0,0,.35)}
html body #coach:has(.nv) .ppop>.pp.nv{margin:0 auto!important}html body #coach:has(.nv) .ppop{justify-content:flex-start!important;padding-top:calc(env(safe-area-inset-top) + 12px)!important}
html body .qr2-im{min-height:104px}html body .nv-h{font-size:2.7rem}html body .qr2-c{margin-bottom:10px}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v181 pass2 ok')
# pass 3: backdrop stays behind (absolute); light entry tiles
s = open(d + 'yofi-real.html').read()
s = s.replace('</style>', """html body .nv>.nv-bg{position:absolute!important;z-index:0}
html body .qf2-f button{background:#FBF6EE!important;box-shadow:0 0 0 1.5px #EADCC6!important}html body .qf2-f button b,html body .qf2-f button small{color:#14213D!important}
html body .qf2-f button.on{background:linear-gradient(180deg,#2F8A3F,#1F6A2E)!important;box-shadow:0 0 0 2.5px #E9B949!important}html body .qf2-f button.on b,html body .qf2-f button.on small{color:#fff!important}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v181 pass3 ok')
