# Real Money build, step 186 (after rmv182.py): head-to-head in the owner's mock-up style.
#  Live: PhotoPicks bar with ✕, "● LIVE · $5 HEAD-TO-HEAD", a headline that tells the story ("The crowd decides",
#  "You're in front", "Fight back!", "Neck and neck", "One vote from victory", "They need one more…"),
#  italic gold "Winner takes $8.50", photos side by side with VS, "Iceland · You" / "@handle", big scores,
#  a counting bar "8 of 15 votes counted". All 15 votes are counted (majority wins), one a second.
#  Result: "$5 HEAD-TO-HEAD · FINAL", "You won" + big gold "$8.50" with confetti, WINNER ribbon on the winning photo,
#  scores, "All 15 votes counted", "$5 entry · $3.50 net win", green "New challenge · $5", Back to stable.
#  Loss: "Not this time" + "$5 entry · lost". Training uses the same screens ("Training win" / dots).
import os
d = os.environ.get('YOFI_DIR', os.path.dirname(os.path.abspath(__file__)) + '/')
s = open(d + 'yofi-real.html').read()
s = s.replace("function fcNotify() {", r"""const H3_V = 15, H3_WIN = 8;
function h3Shell(p, o, oh, fee, A, B, tag, head, sub, foot, res) { const nm = esc(rcName(p)), cash = fee > 0, n = A + B;
  return `<div class="pp qfx qrx h3 ${res ? 'res' : ''}"><div class="h3-top"><span class="h3-br">🖼️ PhotoPicks</span><button class="h3-x" data-h3x aria-label="Close">✕</button></div>
    <p class="h3-tag">${tag}</p><h2 class="h3-h" id="h3H">${head}</h2>${sub}
    <div class="h3-vs"><div class="h3-c me ${res === 'w' ? 'win' : ''}" id="qrCA"><div class="h3-im"><img src="${p.src}" alt="">${res === 'w' ? '<em class="h3-rib">🏆 WINNER</em>' : ''}</div><span>${nm} · You</span><b id="qrAv">${A}</b></div>
      <i class="h3-x2">VS</i><div class="h3-c ${res === 'l' ? 'win' : ''}" id="qrCB"><div class="h3-im"><img src="${o.src}" alt="">${res === 'l' ? '<em class="h3-rib">🏆 WINNER</em>' : ''}</div><span>${esc(oh)}</span><b id="qrBv">${B}</b></div></div>
    ${foot}<p class="h3-sim">Demo · Simulated votes</p></div>`; }
function h2hLive(p, R, fee) { const cash = fee > 0, prize = +(fee * H2H_PAY).toFixed(2), o = { src: R.src, t: R.title || R.t || 'A rival' }, oh = R.h || '@rival', T = p.tq || { w: 0, l: 0 };
  const st = qlStrength(p), rs = cash ? st + (Math.random() - .5) * 14 : st - 4 - Math.random() * 8, pv = Math.max(.3, Math.min(.72, .5 + (st - rs) / 60)), won = Math.random() < (cash ? Math.max(.35, Math.min(.62, pv)) : pv);
  const wv = H3_WIN + Math.floor(Math.random() * 4), seq = [...Array(wv).fill(won ? 1 : 0), ...Array(H3_V - wv).fill(won ? 0 : 1)];
  for (let i = seq.length - 1; i > 0; i--) { const k = Math.floor(Math.random() * (i + 1)); [seq[i], seq[k]] = [seq[k], seq[i]]; }
  const tag = `<i class="h3-dot"></i>LIVE · ${cash ? `$${fee} head-to-head` : 'Training match'}`, sub = `<p class="h3-sub">${cash ? `Winner takes ${money(prize)}` : `Win = training win ${Math.min(TQ_WIN, T.w + 1)} of ${TQ_WIN}`}</p>`;
  const foot = `<div class="h3-bar"><i id="h3B" style="width:0%"></i><span id="h3P">0%</span></div><p class="h3-n" id="h3N">0 of ${H3_V} votes counted</p><p class="qr2-v h3-v" id="qrV">🗳️ The crowd is voting…</p>`;
  popOpen(h3Shell(p, o, oh, fee, 0, 0, tag, 'The crowd decides', sub, foot, ''));
  const close = () => { popClose(); finalsTab(); }; document.querySelectorAll('[data-h3x]').forEach(b => b.onclick = close);
  const run = () => { let i = 0, A = 0, B = 0, dec = 0; const step = () => { if (!document.getElementById('h3N')) return;
      const me = seq[i++]; if (me) A++; else B++; const vh = '@' + QS_NAMES[Math.floor(Math.random() * QS_NAMES.length)];
      $('#qrAv').textContent = A; $('#qrBv').textContent = B; const pc = Math.round((A + B) / H3_V * 100); $('#h3B').style.width = pc + '%'; $('#h3P').textContent = pc + '%'; $('#h3N').textContent = `${A + B} of ${H3_V} votes counted`;
      const c = document.getElementById(me ? 'qrCA' : 'qrCB'); c.classList.remove('hit'); void c.offsetWidth; c.classList.add('hit');
      $('#qrV').innerHTML = `🗳️ <b>${vh}</b> voted for <b class="${me ? 'me' : ''}">${me ? esc(rcName(p)) : esc(oh)}</b>`;
      const H = $('#h3H'); let h;
      if (A >= H3_WIN) h = 'Victory!'; else if (B >= H3_WIN) h = 'They’ve taken it'; else if (A === H3_WIN - 1 && B === H3_WIN - 1) h = 'Next vote wins it!'; else if (A === H3_WIN - 1) h = 'One vote from victory'; else if (B === H3_WIN - 1) h = 'They need one more…';
      else if (A === B) h = 'Neck and neck'; else if (A > B) h = A - B >= 4 ? 'Pulling away!' : 'You’re in front'; else h = 'Fight back!';
      if (H.textContent !== h) { H.textContent = h; H.classList.remove('pop'); void H.offsetWidth; H.classList.add('pop'); }
      if (!dec && (A >= H3_WIN || B >= H3_WIN)) dec = 1;
      if (i < H3_V) { setTimeout(step, dec ? 350 : 1000); return; } setTimeout(() => photoFinish(() => h3Done(p, o, oh, fee, won, A, B)), 500); };
    step(); };
  qrCount(p, o, oh, run, cash ? `💵 $${fee} head-to-head` : '🏋️ Training match', cash ? `Most votes of ${H3_V} wins ${money(prize)}` : `Most votes of ${H3_V} wins`); }
function h3Done(p, o, oh, fee, won, A, B) { const cash = fee > 0, prize = +(fee * H2H_PAY).toFixed(2), H = p.h2h = p.h2h || { w: 0, l: 0, cash: 0 }, T = p.tq = p.tq || { w: 0, l: 0 }; let head, foot, fresh = false;
  if (won) H.w++; else H.l++;
  if (cash) { if (won) { H.cash = +(H.cash + prize).toFixed(2); S.cash = +((S.cash || 0) + prize).toFixed(2); try { earnAdd({ kind: 'h2', pid: p.id, t: p.title, amt: prize }); } catch (e) {} }
    head = won ? `<h2 class="h3-h">You won</h2><div class="h3-amt">${money(prize)}</div>` : '<h2 class="h3-h">Not this time</h2>';
    foot = `<p class="h3-n">All ${H3_V} votes counted</p><p class="h3-net">$${fee} entry · ${won ? `${money(prize - fee)} net win` : 'lost'}</p><button class="btn block nv-go" id="h2Ag">New challenge · $${fee}</button>`; }
  else { if (won) { T.w++; p.form = Math.min(10, (p.form || 0) + 1); qlStrength(p); p.vd.pct = Math.min(85, p.vd.pct + 1); } else T.l++;
    if (T.w >= TQ_WIN) { p.cashOK = 1; fresh = true; }
    head = `<h2 class="h3-h">${fresh ? 'Ready for Cash Races!' : won ? 'Training win' : 'Not this time'}</h2>`;
    foot = `<p class="h3-n">All ${H3_V} votes counted</p><div class="h2w-dots">${[0, 1, 2].map(i => `<i class="${i < T.w ? 'w' : ''}"></i>`).join('')}</div><p class="h3-net">${fresh ? 'Finals ($2–$20) and cash head-to-heads are open' : T.l >= TQ_WIN ? `Training over at ${T.w}–${T.l} · start a fresh run` : `${T.w} of ${TQ_WIN} training wins`}</p>
      <button class="btn block nv-go" id="h2Ag">${fresh ? '🏁 Enter a Final' : `🏋️ Train again · ${TQ_COST} 🟡`}</button>`;
    if (T.l >= TQ_WIN && !fresh) p.tq = { w: 0, l: 0 }; }
  save(); try { paintWallet(); paintGems(); } catch (e) {}
  popOpen(h3Shell(p, o, oh, fee, A, B, `${cash ? `$${fee} head-to-head` : 'Training match'} · Final`, '', head, `${foot}<div style="text-align:center"><button class="link nv-later" id="h2Bk">Back to stable</button></div>`, won ? 'w' : 'l').replace('<h2 class="h3-h" id="h3H"></h2>', ''));
  if (won) setTimeout(() => { try { if (cash) cashExplosion(prize, { label: 'Head-to-head win' }); rvConfetti(document.querySelector('.h3'), 120); } catch (e) {} }, 300);
  document.querySelectorAll('[data-h3x]').forEach(b => b.onclick = () => { popClose(); finalsTab(); });
  $('#h2Ag').onclick = () => { if (fresh) { popClose(); qfStart(p); } else h2hOpen(p, fee); }; $('#h2Bk').onclick = () => { popClose(); finalsTab(); }; }
function fcNotify() {""", 1)
s = s.replace('</style>', """html body #coach:has(.h3) .ppop{background:radial-gradient(120% 60% at 50% 0%,#14224A 0%,#0B1530 60%,#08102A 100%)!important;color:#EEF1F8;border:0!important;box-shadow:none!important}
html body #coach:has(.h3) .ppop>.pp.h3{margin:0 auto!important}.h3{position:relative;text-align:center;color:#EEF1F8}
.h3-top{display:flex;align-items:center;justify-content:space-between;margin:0 0 14px}.h3-br{font:800 1.3rem Fraunces,Georgia,serif;color:#FBF3DC}.h3-x{border:0;background:none;color:#FBF3DC;font-size:1.6rem;line-height:1;cursor:pointer;padding:4px}
.h3-tag{display:flex;align-items:center;justify-content:center;gap:8px;margin:0 0 8px;font:900 .82rem Nunito,system-ui;letter-spacing:.14em;text-transform:uppercase;color:#EEF1F8}.h3-dot{width:10px;height:10px;border-radius:50%;background:#34C759;animation:qmPulse 1.2s ease-in-out infinite}
html body .h3 h2.h3-h{margin:0;font:900 2.6rem/1.05 Fraunces,Georgia,serif;color:#FBF3DC!important;-webkit-text-fill-color:#FBF3DC!important;min-height:2.2em;display:flex;align-items:center;justify-content:center}.h3.res h2.h3-h{min-height:0}
.h3-h.pop{animation:cdPop .45s ease-out}.h3-sub{margin:6px 0 16px;font:italic 600 1.3rem Fraunces,Georgia,serif;color:#F3D98B}
.h3-amt{margin:0 0 14px;font:900 4.2rem/1 Fraunces,Georgia,serif;background:linear-gradient(180deg,#FFE9A8,#E9B949 55%,#B8862E);-webkit-background-clip:text;background-clip:text;color:transparent;-webkit-text-fill-color:transparent;filter:drop-shadow(0 3px 10px rgba(233,185,73,.35));animation:cdPop .6s ease-out both}
.h3-vs{display:grid;grid-template-columns:1fr 34px 1fr;align-items:start;gap:4px;margin:4px 0 14px}.h3-c{display:flex;flex-direction:column;align-items:center;gap:4px;min-width:0;transition:transform .2s}.h3-c.hit{animation:qrHit .45s ease-out}
.h3-im{position:relative;width:100%}.h3-im img{display:block;width:100%;aspect-ratio:1;object-fit:cover;border-radius:6px;box-shadow:0 0 0 1px rgba(255,255,255,.25)}.h3-c.win .h3-im img{box-shadow:0 0 0 3px #E9B949,0 0 22px rgba(233,185,73,.45)}
.h3-rib{position:absolute;top:10px;left:10px;padding:4px 10px;background:linear-gradient(180deg,#F3D98B,#D9AE4F);color:#14213D;font:900 .76rem Nunito,system-ui;letter-spacing:.06em;font-style:normal;clip-path:polygon(0 0,100% 0,92% 50%,100% 100%,0 100%)}
.h3-c span{font:700 .95rem Nunito,system-ui;color:#EEF1F8;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.h3-c>b{font:900 3.4rem/1 Fraunces,Georgia,serif;color:#FBF3DC}.h3-c.me>b{color:#FBF3DC}
.h3-x2{align-self:center;margin-top:-40px;font:800 1.2rem Fraunces,Georgia,serif;color:#EEF1F8;font-style:normal}
.h3-bar{position:relative;height:26px;border-radius:13px;background:#2A3554;overflow:hidden}.h3-bar i{display:block;height:100%;border-radius:13px;background:linear-gradient(90deg,#2E9E46,#3FC25A);transition:width .5s ease-out}
.h3-bar span{position:absolute;left:0;right:0;top:0;line-height:26px;font:800 .85rem Nunito,system-ui;color:#fff}.h3-n{margin:8px 0 2px;font:700 1.05rem Fraunces,Georgia,serif;color:#EEF1F8}.h3-v{color:#B9C3DA}
.h3-net{margin:2px 0 14px;font:italic 600 1.1rem Fraunces,Georgia,serif;color:#F3D98B}.h3-sim{margin:18px 0 0;font:600 .8rem Nunito,system-ui;color:#B9C3DA}
html body .h3 .nv-go{min-height:56px!important;border-radius:999px!important;background:linear-gradient(180deg,#2E9E46,#1C7A33)!important;color:#fff!important;font:800 1.35rem Nunito,system-ui!important;box-shadow:0 6px 16px rgba(0,0,0,.35)!important;margin:4px 0 0!important}
html body .h3 .nv-later{margin-top:12px;color:#FBF3DC!important;font:700 1.05rem Nunito,system-ui;text-decoration:underline}
html body .h3>.qr-cd{position:absolute!important;inset:-12px -16px -28px!important;z-index:20!important;justify-content:center;padding:0 16px;background:radial-gradient(120% 70% at 50% 0%,#14224A,#0B1530)}html body .h3 .qr-cd .pp-k{color:#F3D98B!important;-webkit-text-fill-color:#F3D98B!important}html body .h3 .qr-num{color:#F3D98B}html body .h3 .qr-vs b{color:#FBF3DC}html body .h3 .qr-vs small,html body .h3 .qr-sub{color:#C9D3E6}
</style>""", 1)
open(d + 'yofi-real.html', 'w').write(s); print('rm v183 ok')
